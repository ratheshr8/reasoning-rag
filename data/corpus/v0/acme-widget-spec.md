# Acme Widget Specification

Status: synthetic sample for reasoning-rag evaluation fixtures.
License: CC0-1.0 (public domain dedication by the project author).

## Overview

The Acme Widget is a fictional device used only to exercise hierarchy-aware
document question answering. It has no relation to any real product.

## Power requirements

The widget requires a 5V DC supply at a maximum of 500 mA. Peak inrush current
must remain below 750 mA for no more than 10 milliseconds.

### Battery mode

When operating from the optional battery pack, runtime is approximately 6 hours
at the default brightness setting. Runtime figures are estimates for the
synthetic corpus and are not product claims.

## Safety limits

Do not operate the widget above 40 degrees Celsius ambient temperature.
If the case temperature exceeds 55 degrees Celsius, the device must enter a
thermal shutdown state and raise a visible fault indicator.

## Maintenance

### Cleaning

Wipe the exterior with a dry cloth. Do not immerse the device in liquid.

### Firmware updates

Firmware updates are described in a separate document that is intentionally
absent from this corpus so unanswerable questions can be tested.

## Appendix A — Error codes

| Code | Meaning |
| --- | --- |
| E01 | Thermal shutdown |
| E02 | Supply voltage out of range |
| E03 | Unknown fault |

## Conflicting note (intentional)

Earlier drafts claimed a maximum ambient temperature of 45 degrees Celsius.
This specification supersedes those drafts and sets the limit at 40 degrees
Celsius. Retrieval systems should surface the conflict rather than hide it.
