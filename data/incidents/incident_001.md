# Incident 001 – Checkout Failures in EU

Incident ID: INC-001
Date: 2025-10-09
Services: checkout-api, payments-service
Region: EU

## Summary

Users in EU experienced checkout failures for ~27 minutes. The incident primarily impacted checkout flows for logged-in customers.

## Timeline

- 10:02 – Deployment of checkout-api v2.18.
- 10:05 – Error rate spikes on checkout-api (HTTP 500).
- 10:08 – Database CPU hits 95%.
- 10:29 – Rollback to v2.17.
- 10:31 – Error rate returns to baseline.

## SRE Notes

SRE team believes a misconfigured connection pool in checkout-api overloaded the primary database. After rollback, DB CPU dropped to 60%, which suggests the application was the main driver.

## Database Team Notes

DB team argues the database was already close to capacity and had been warning about this. They claim the deployment simply exposed underlying infra capacity issues.

## Fixes

- Rolled back checkout-api to v2.17.
- Reduced connection pool size.
- Planned DB capacity upgrade.
