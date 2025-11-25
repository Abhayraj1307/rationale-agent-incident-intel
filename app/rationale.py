from typing import List, Dict, Any
from collections import defaultdict


CAUSE_LABELS = {
    "config_error": "Configuration Error",
    "infra_failure": "Infrastructure / Capacity Failure",
    "human_error": "Human Error",
    "third_party": "Third-Party / Vendor Issue",
    "other": "Other / Unclear",
}


def aggregate_claims(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Group claims by cause_category and compute support counts and conflict flag.
    """
    by_cause = defaultdict(list)
    for c in claims:
        cause = c.get("cause_category", "other")
        by_cause[cause].append(c)

    support_counts = {cause: len(lst) for cause, lst in by_cause.items()}
    if support_counts:
        dominant_cause = max(support_counts.items(), key=lambda x: x[1])[0]
    else:
        dominant_cause = "other"

    non_zero_causes = [c for c, cnt in support_counts.items() if cnt > 0]
    has_conflict = len(non_zero_causes) > 1

    return {
        "by_cause": by_cause,
        "support_counts": support_counts,
        "dominant_cause": dominant_cause,
        "has_conflict": has_conflict,
    }


def compute_confidence(support_counts: Dict[str, int]) -> float:
    total = sum(support_counts.values())
    if total == 0:
        return 0.0
    top = max(support_counts.values())
    return round(top / total, 2)


def format_rationale_text(incident_id: str, agg: Dict[str, Any]) -> str:
    dominant = agg["dominant_cause"]
    counts = agg["support_counts"]
    label = CAUSE_LABELS.get(dominant, dominant)
    total = sum(counts.values())
    dominant_count = counts.get(dominant, 0)

    parts = [
        f"For **{incident_id}**, the dominant inferred root-cause category is **{label}** "
        f"({dominant_count} out of {total} extracted claims)."
    ]

    if agg["has_conflict"]:
        parts.append("However, there are conflicting claims for alternative causes:")
        for cause, n in counts.items():
            if cause == dominant or n == 0:
                continue
            parts.append(f"- {CAUSE_LABELS.get(cause, cause)}: {n} claim(s) support this interpretation.")

    return "  \n".join(parts)
