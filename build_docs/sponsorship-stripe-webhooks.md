# Sponsorship Stripe Webhook Connection (BuildDocs)

## Overview
The sponsorship flow is **application first**, then **Stripe payment**. After a sponsor submits the Sponsorship Application, trigger a Stripe Checkout session with the sponsorship tier they selected. Stripe will call the webhook once the payment completes; use that webhook to confirm payment and finalize the sponsorship record.

This guide describes how to wire the sponsorship tiers to Stripe using the **existing tier labels and IDs** already defined in the app.

## Source of truth for sponsorship labels
The sponsorship tiers (labels and IDs) are defined in the sponsorship application form (`SponsorshipApplicationForm`) and used by the sponsor application page:

- **IDs (support_level values)**:
  - `wish_granter`
  - `wonders_wishes`
  - `food_truck_champion`
  - `dream_maker`
  - `wish_builder`
  - `hope_helper`
  - `joy_giver`

- **Labels (as shown to users)**:
  - Wish Granter ($10,000)
  - Wonders & Wishes Sponsor ($5,000)
  - Food Truck Champion ($3,500)
  - Dream Maker Sponsor ($2,500)
  - Wish Builder Sponsor ($1,000)
  - Hope Helper Sponsor ($500)
  - Joy Giver Sponsor ($250)

These values should be used consistently for Stripe line item metadata and for labeling completed sponsorships in internal views.

## Sponsorship tiers mapping (Stripe line item amounts)
Use the following mapping for Stripe Checkout line items (amounts in cents):

| support_level ID | Label | Amount (cents) | Description |
| --- | --- | --- | --- |
| `wish_granter` | Wish Granter Sponsor | 1000000 | Exclusive Presenting Sponsor. Grants one wish. |
| `wonders_wishes` | Wonders & Wishes Sponsor | 500000 | Exclusive Family Fun Zone sponsor. |
| `food_truck_champion` | Food Truck Champion | 350000 | Fueling the fun & flavor. Limited to 3. |
| `dream_maker` | Dream Maker Sponsor | 250000 | Logo on ads and volunteer shirts. |
| `wish_builder` | Wish Builder Sponsor | 100000 | Yard sign, table, and shirt logo. |
| `hope_helper` | Hope Helper Sponsor | 50000 | Yard sign, table, social recognition. |
| `joy_giver` | Joy Giver Sponsor | 25000 | Event table and social recognition. |

## Stripe API endpoints already available
The app exposes the Stripe endpoints below. Use them as-is for the sponsorship payment flow:

- **Create Checkout session**: `POST /api/stripe/checkout-session`
- **Stripe webhook**: `POST /api/stripe/webhook`

The service layer for Stripe lives in `app/services/stripe.py` and expects:
- `STRIPE_API_KEY` to create sessions
- `STRIPE_WEBHOOK_SECRET` to validate webhook signatures

## Recommended request payload for Checkout session
When a sponsorship application is submitted, construct the Checkout session payload using the selected `support_level` ID and label:

```json
{
  "mode": "payment",
  "success_url": "https://www.wishuponafoodtruck.com/sponsorship-confirmation",
  "cancel_url": "https://www.wishuponafoodtruck.com/sponsorship-application",
  "customer_email": "<applicant email>",
  "line_items": [
    {
      "price_data": {
        "currency": "usd",
        "unit_amount": 1000000,
        "product_data": {
          "name": "Wish Granter Sponsor",
          "description": "Exclusive Presenting Sponsor. Grants one wish."
        }
      },
      "quantity": 1
    }
  ],
  "metadata": {
    "support_level": "wish_granter",
    "support_label": "Wish Granter ($10,000)",
    "application_id": "<application record id>"
  }
}
```

> Use the support_level ID as the primary key and keep the human label (`support_label`) as metadata to preserve the exact label used in the application UI.

## Webhook handling expectations
Stripe should send `checkout.session.completed` events to the webhook endpoint.

On webhook receipt:
1. Verify signature (requires `STRIPE_WEBHOOK_SECRET`).
2. Read `event.type`, `event.id`, and the session metadata (`support_level`, `support_label`, `application_id`).
3. Mark the sponsorship application as paid (or create a sponsorship record if you keep them separate).
4. Optionally notify internal teams (Teams/email integration already exists in the app).

## Environment variables required
Set these environment variables in the runtime environment:

- `STRIPE_API_KEY`
- `STRIPE_WEBHOOK_SECRET`

Optional for notifications after payment:
- `TEAMS_WEBHOOK_URL`
- `DEFAULT_EMAIL_SENDER`

## Example `.env`
Use the following as a starting point for local or hosted configuration:

```bash
SECRET_KEY="replace-with-a-secure-secret"
STRIPE_API_KEY="sk_live_or_test_key_here"
STRIPE_WEBHOOK_SECRET="whsec_..."
TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..."
DEFAULT_EMAIL_SENDER="hello@wishuponafoodtruck.com"
```

## Implementation checklist
- [ ] Ensure the Sponsorship Application submission stores `support_level` and `support_label` (from the existing labels above).
- [ ] On submit, call `POST /api/stripe/checkout-session` using the mapping table.
- [ ] Configure Stripe to send webhooks to `POST /api/stripe/webhook`.
- [ ] On webhook success, update sponsorship status and trigger internal notifications if desired.
