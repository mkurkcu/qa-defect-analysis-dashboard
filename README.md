# QA Defect Analysis Dashboard

A Python/Streamlit dashboard for analyzing Jira-style QA defect exports.

This repository is a portfolio-safe version of an academic capstone dashboard. It contains no employer/client production data, credentials, or internal exports. Use your own compatible CSV or the included synthetic sample data.

## Features

- Upload and validate Jira-style CSV exports
- Filter by project, assignee, priority, status category, and created-date range
- KPI cards for total, To Do, In Progress, Done, and average cycle time
- Status and priority breakdowns
- Created/resolved throughput trends
- Open-item aging analysis
- Bugs per assignee and project
- Resolution-time analysis by assignee
- Priority trends over time
- Export a static HTML report

## Project Structure

```text
qa-defect-analysis-dashboard/
├── streamlit_app.py
├── generate_report.py
├── requirements.txt
├── sample_data/
│   └── sample_jira.csv
└── src/
    ├── __init__.py
    ├── io.py
    ├── metrics.py
    └── charts.py
```

## Run

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Upload `sample_data/sample_jira.csv` to try the dashboard.

## Expected CSV Columns

- Issue key
- Project key
- Created
- Resolved
- Priority
- Status
- Status Category
- Issue Type
- Assignee
- Custom field (Requirement-Type)
- Custom field (Business Process)

## Privacy

Do not commit confidential Jira exports, internal ticket descriptions, employee information, credentials, or other proprietary data. The included sample dataset is synthetic.
