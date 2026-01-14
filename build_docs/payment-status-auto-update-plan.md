# Payment Status Auto-Update Plan

## Goal
Ensure payment status updates automatically in the backend after a successful Stripe payment, without relying on a manual confirmation page refresh.

## Proposed approach
1. **Document the desired flow**
   - Keep Stripe Checkout metadata as the source of truth for `application_id` and `application_type`.
   - Rely on the Stripe webhook to update payment status whenever a `checkout.session.completed` (or async success) event is received.

2. **Update the Stripe session metadata**
   - Include an `application_type` value in the Checkout session metadata so the webhook can route to the correct model.

3. **Harden webhook handling**
   - Confirm the Stripe event type and session `payment_status` are successful before updating records.
   - Route updates via a shared helper that maps `application_type` to the proper model and updates `payment_status` and `status`.

4. **Validate and log the update**
   - Handle missing/invalid metadata safely (ignore without crashing the webhook).
   - Leave the confirmation page as a fallback, but ensure the webhook handles the primary update programmatically.

5. **Testing/verification**
   - Use Stripe CLI or webhook test fixtures to send a `checkout.session.completed` event with metadata and verify the database record is updated.
