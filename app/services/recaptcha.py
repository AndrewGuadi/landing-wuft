from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from flask import Request


@dataclass(frozen=True)
class RecaptchaAssessment:
    passed: bool
    score: float
    reasons: tuple[str, ...]
    payload: Mapping[str, Any]


def assess_request(
    request: Request,
    *,
    is_privileged: bool = False,
    minimum_score: float = 0.6,
    privileged_minimum: float = 0.35,
) -> RecaptchaAssessment:
    payload = _parse_payload(request.form.get("recaptcha_payload", ""))
    honeypot = (request.form.get("company_website") or "").strip()
    if honeypot:
        return RecaptchaAssessment(
            passed=False,
            score=0.0,
            reasons=("honeypot_filled",),
            payload=payload,
        )

    score, reasons = _score_payload(payload, request)
    threshold = privileged_minimum if is_privileged else minimum_score
    return RecaptchaAssessment(
        passed=score >= threshold,
        score=score,
        reasons=tuple(reasons),
        payload=payload,
    )


def _parse_payload(raw_payload: str) -> Mapping[str, Any]:
    if not raw_payload:
        return {}
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _score_payload(payload: Mapping[str, Any], request: Request) -> tuple[float, list[str]]:
    reasons: list[str] = []
    score = 0.5

    if not payload:
        return 0.1, ["missing_payload"]

    if payload.get("version") != "self-contained-v3":
        reasons.append("unexpected_version")
        score -= 0.1

    duration_ms = _as_int(payload.get("duration_ms"))
    if duration_ms < 300:
        score -= 0.35
        reasons.append("instant_submit")
    elif duration_ms < 800:
        score -= 0.2
        reasons.append("fast_submit")
    elif duration_ms >= 3000:
        score += 0.1
    if duration_ms >= 15000:
        score += 0.05

    events = payload.get("events") or {}
    total_events = _as_int(payload.get("total_events"))
    if not total_events:
        total_events = sum(_as_int(value) for value in events.values())

    if total_events == 0:
        score -= 0.35
        reasons.append("no_interaction")
    elif total_events >= 3:
        score += 0.1
    if total_events >= 10:
        score += 0.05

    if _as_int(events.get("click")) > 0:
        score += 0.05
    if _as_int(events.get("keydown")) > 0:
        score += 0.05
    if _as_int(events.get("pointermove")) > 0:
        score += 0.05
    if _as_int(events.get("scroll")) > 0:
        score += 0.03
    if _as_int(events.get("touchstart")) > 0:
        score += 0.03
    if _as_int(events.get("paste")) > 0:
        score += 0.02

    trusted_ratio = _as_float(payload.get("trusted_event_ratio"), default=1.0)
    if total_events > 0 and trusted_ratio < 0.6:
        score -= 0.1
        reasons.append("low_trusted_events")

    if payload.get("webdriver") is True:
        score = 0.0
        reasons.append("webdriver_detected")

    user_agent = payload.get("user_agent") or request.user_agent.string
    if not user_agent:
        score -= 0.25
        reasons.append("missing_user_agent")

    language = payload.get("language") or request.headers.get("Accept-Language")
    if not language:
        score -= 0.05
        reasons.append("missing_language")

    if payload.get("timezone_offset") is None:
        score -= 0.05
        reasons.append("missing_timezone")
    else:
        score += 0.02

    screen = payload.get("screen") or {}
    screen_width = _as_int(screen.get("width"))
    screen_height = _as_int(screen.get("height"))
    if screen_width and screen_height:
        if screen_width < 320 or screen_height < 320:
            score -= 0.05
            reasons.append("tiny_screen")
        else:
            score += 0.02

    if payload.get("cookies_enabled") is False:
        score -= 0.05
        reasons.append("cookies_disabled")

    visibility_changes = _as_int(payload.get("visibility_changes"))
    if visibility_changes == 0:
        score += 0.02
    elif visibility_changes > 2:
        score -= 0.05
        reasons.append("visibility_flips")

    focus_changes = _as_int(payload.get("focus_changes"))
    if focus_changes > 0:
        score += 0.02
    elif duration_ms > 5000:
        score -= 0.03

    first_interaction = payload.get("first_interaction_ms")
    if isinstance(first_interaction, int) and first_interaction >= 0 and first_interaction < 200:
        score -= 0.05
        reasons.append("instant_interaction")

    page_url = payload.get("page_url")
    if not page_url:
        score -= 0.02
        reasons.append("missing_page_url")

    return _clamp(score, 0.0, 1.0), reasons


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _as_float(value: Any, *, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))
