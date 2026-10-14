# Enterprise DLP Concept Mapping



## Purpose



This document maps the custom detection conditions in DLP Sentinel to general enterprise Data Loss Prevention concepts.



This is a learning exercise. The Python rules are not native Microsoft Purview policies, and no production DLP platform integration is implemented.



## Rule Mapping



| Python Rule | Enterprise DLP Concept | Analyst Validation |

|---|---|---|

| DLP-001 | Sensitive data sent to an unapproved destination | Verify destination approval and business purpose |

| DLP-002 | Sensitive information shared externally | Review recipient, authorization and sharing context |

| DLP-003 | Bulk data download | Check volume, user context and legitimate business need |

| DLP-004 | Upload to an unapproved cloud destination | Validate destination and sensitivity of the data |

| DLP-005 | Unapproved removable-media transfer | Check device authorization and applicable policy |



## Policy Design Considerations



For an enterprise DLP policy, consider:



- Which sensitive information should be detected?

- Which users, devices, applications or locations are in scope?

- What conditions trigger an alert?

- Should the policy audit, notify, restrict or block activity?

- What exceptions are permitted for approved business activity?

- What evidence should an analyst review before escalating?

- How should false positives and policy exceptions be handled?



Available actions depend on the enterprise product, configuration, licensing and workload.



## Investigation Principles



1. Validate the alert against available event details.

2. Check authorization and legitimate business context.

3. Record the evidence reviewed and any missing information.

4. Escalate suspicious or unresolved cases according to procedure.

5. Do not classify an event as a confirmed data leak without sufficient supporting evidence.



## Limitations



This mapping describes concepts, not a tested enterprise configuration. It does not demonstrate hands-on Microsoft Purview administration or production DLP operations.



## Learning Resource



Microsoft Learn: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp
