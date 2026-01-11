# Test Guide

## Running the test suite
- Run all tests:
  - `pytest`
- Run the smoke tests only:
  - `pytest tests/test_main_routes.py tests/test_api_smoke.py`

## Notes
- The smoke tests verify public page routes, the `/health` endpoint, and API integration stubs.
