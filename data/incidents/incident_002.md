# Incident 002 – Authentication Timeouts

Incident ID: INC-002
Date: 2025-10-15
Services: auth-service
Region: Global

## Summary

Authentication requests timed out globally for ~15 minutes. Only new logins were impacted; existing sessions continued to work.

## Timeline

- 14:01 – Network team performs planned change on edge load balancer.
- 14:03 – auth-service latency increases sharply.
- 14:06 – Multiple 504 errors returned to clients.
- 14:16 – Network change rolled back.
- 14:17 – Latency and error rates return to normal.

## SRE Notes

SREs state the misconfigured load balancer health checks caused all auth instances to be marked as unhealthy, routing traffic incorrectly.

## Network Team Notes

Network team acknowledges an incorrect health check path but points out that auth-service did not have proper readiness checks, which worsened the impact.

## Fixes

- Corrected health check path on load balancer.
- Added readiness checks to auth-service.
- Documented rollback procedure for similar changes.

