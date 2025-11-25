# Rationale Agent – Incident Intelligence

Rationale Agent is an LLM-powered assistant that helps SRE and engineering teams quickly interpret and review incident post-mortems.

Given a set of structured incident markdown files, the tool lets you select an incident and generates:

- A **primary inferred root-cause category** with an associated confidence estimate  
- **Alternative plausible causes** with relative support  
- A structured **“Evidence by Cause Category”** view, including:
  - Summarized claims
  - Affected systems and regions
  - Evidence snippets extracted from relevant sections (Summary, SRE Notes, Network Notes, etc.)

The intent is to move teams from **unstructured narrative incident reports to a focused, decision-ready RCA view** in a single step.

---

## ⚙️ Key Features

- 📄 **Incident ingestion from markdown**  
  Loads incident reports from `data/incidents/` and exposes them through a simple selection UI.

- 🧠 **LLM-driven root cause inference**  
  Uses a large language model to infer likely root-cause categories (e.g. `config_error`, `other`, etc.) and identify competing explanations.

- 📊 **Decision summary and confidence scoring**  
  Aggregates extracted claims to:
  - Count the amount of supporting evidence per cause
  - Compute a lightweight confidence score for the leading cause
  - Highlight conflicting hypotheses instead of forcing a single narrative

- 🔎 **Evidence organized by cause**  
  For each inferred cause, presents:
  - A concise claim summary
  - Impacted systems / regions
  - The originating section (Summary, SRE Notes, Network Notes, etc.)
  - A short evidence snippet from the original incident text

- 🖥️ **Streamlit-based analyst UI**  
  Web UI built with Streamlit: choose an incident, trigger analysis, and review the structured RCA output in dedicated panels.

---

## 🧱 Project Structure

```text
rationale-agent-incident-intel/
├── app/
│   ├── __init__.py
│   ├── ingest.py        # Load and parse incident markdown files
│   ├── claims.py        # Data structures and helpers for claims / cause categories
│   ├── rationale.py     # LLM calls and decision summary aggregation
│   └── ui.py            # Streamlit front-end
├── data/
│   └── incidents/
│       ├── incident_001.md
│       └── incident_002.md
├── requirements.txt
└── README.md

