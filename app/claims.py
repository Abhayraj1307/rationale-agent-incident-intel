from typing import List, Dict
import re


CAUSE_CONFIG = "config_error"
CAUSE_INFRA = "infra_failure"
CAUSE_HUMAN = "human_error"
CAUSE_THIRD_PARTY = "third_party"
CAUSE_OTHER = "other"


def _infer_cause_category(text: str) -> str:
    t = text.lower()
    if "misconfig" in t or "misconfigured" in t or "configuration" in t or "config" in t:
        return CAUSE_CONFIG
    if "capacity" in t or "cpu" in t or "database" in t or "db" in t or "infra" in t:
        return CAUSE_INFRA
    if "human error" in t or "mistyped" in t or "operator" in t:
        return CAUSE_HUMAN
    if "third-party" in t or "third party" in t or "vendor" in t:
        return CAUSE_THIRD_PARTY
    return CAUSE_OTHER


def _infer_system(text: str) -> str:
    m = re.search(
        r"(checkout-api|payments-service|auth-service|database|db|load balancer)",
        text,
        re.IGNORECASE,
    )
    if m:
        return m.group(1)
    return ""


def _infer_impact_scope(text: str) -> str:
    t = text.lower()
    if "eu" in t and "users" in t:
        return "EU_users"
    if "global" in t or "worldwide" in t:
        return "global_users"
    if "logged-in" in t or "login" in t:
        return "login_users"
    return "unspecified"


def extract_claims(incident_id: str, filename: str, text: str) -> List[Dict]:
    """
    Heuristic-based extractor to simulate structured claims.
    In a real system, this would be replaced by an LLM.
    """
    claims: List[Dict] = []

    # Split by sections roughly
    sections = re.split(r"\n##\s+", text)
    for section in sections:
        section_lower = section.lower()
        if "notes" not in section_lower and "summary" not in section_lower:
            continue

        cause_category = _infer_cause_category(section)
        system = _infer_system(section)
        impact_scope = _infer_impact_scope(text)
        sentences = re.split(r"(?<=[.!?])\s+", section.strip())
        summary = sentences[0] if sentences and sentences[0] else section.strip()[:200]
        evidence_snippet = section.strip()[:300]

        claims.append(
            {
                "incident_id": incident_id,
                "source_doc": filename,
                "cause_category": cause_category,
                "system": system,
                "impact_scope": impact_scope,
                "summary": summary,
                "evidence_snippet": evidence_snippet,
            }
        )

    return claims
