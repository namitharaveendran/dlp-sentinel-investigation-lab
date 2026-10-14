# DLP Sentinel â€” Incident Investigation Report

## 1. Project Overview

DLP Sentinel is a Python-based learning project that generates synthetic Data Loss Prevention (DLP) events, applies detection rules, and supports initial alert triage and investigation.

**Environment:** Python 3.10  
**Data source:** Synthetic DLP event dataset  
**Events analysed:** 30  
**Unique events selected for initial investigation:** 5

## 2. Investigation Objective

The objective is to identify potentially risky data-handling activities, assign initial priorities, recommend follow-up actions, and document investigation outcomes without prematurely declaring an incident confirmed.

## 3. Detection Rules

- **DLP-001:** Confidential or Restricted data sent to an unapproved destination â€” High severity.
- **DLP-002:** External sharing involving Confidential or Restricted information â€” High severity.
- **DLP-003:** Bulk downloads involving at least 100 files â€” Medium severity.
- **DLP-004:** Cloud uploads to the configured `unapproved_cloud` destination â€” High severity for Confidential or Restricted data; otherwise Medium severity.
- **DLP-005:** Copying files to a `usb_drive` destination without approval â€” Medium severity.

These rules use predefined conditions and severity assignments. An alert indicates activity requiring review; it does not, by itself, establish a confirmed data leak or malicious intent.

## 4. Initial Investigation Findings

| Event ID | Priority | Initial finding | Recommended action |
|---|---|---|---|
| DLP-001 | High | Confidential data associated with an unapproved external email destination | Escalate for review |
| DLP-002 | Medium | 250 files downloaded; business purpose requires verification | Validate business purpose and authorization |
| DLP-003 | High | Confidential data associated with an unapproved cloud destination | Escalate for review |
| DLP-004 | Medium | USB destination marked as unapproved | Review removable-media activity |
| DLP-007 | High | 180 restricted files downloaded without a stated business justification | Validate business purpose and authorization |

## 5. Evidence and Limitations

The initial triage uses fields from a synthetic dataset, including activity type, data sensitivity, destination approval, file count, and business justification.

No independent identity verification, endpoint evidence, actual file-transfer confirmation, or authorization records were reviewed. Therefore, these findings indicate activities requiring review, not confirmed data loss or malicious intent.

## 6. Investigation Disposition

All five selected events remain **Inconclusive** pending additional review.

Before reaching a final disposition, an analyst should validate the user's identity and role, confirm the business purpose, review applicable DLP policy and approval records, and correlate available endpoint, identity, and network logs.

## 7. Recommended Follow-up Actions

1. Validate the user's authorization and business justification.
2. Review destination approval and applicable data-handling policies.
3. Correlate relevant endpoint, identity, and network evidence.
4. Escalate suspicious activity according to the organization's incident-response procedure.
5. Document supporting evidence, analyst decisions, and final disposition.

## 8. Project Limitations and Future Improvements

- The dataset is synthetic and does not represent production telemetry.
- Detection thresholds and priorities are rule-based and require validation.
- Initial priority assignments do not prove policy violations.
- Future work could add analyst feedback, configurable rules, duplicate-alert handling, and metrics for alert volume, investigation outcomes, and false positives.

## 9. Conclusion

DLP Sentinel demonstrates a basic workflow for synthetic DLP event generation, rule-based detection, initial prioritization, and investigation documentation. The current results are suitable for a learning lab and require real evidence and validation before they could support operational incident decisions.
