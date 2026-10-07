import pandas as pd

REQUIRED_COLS = [
    "Issue key",
    "Project key",
    "Created",
    "Resolved",
    "Priority",
    "Status",
    "Status Category",
    "Issue Type",
    "Assignee",
    "Custom field (Requirement-Type)",
    "Custom field (Business Process)",
]

STRING_COLS = [
    "Issue key",
    "Project key",
    "Priority",
    "Status",
    "Status Category",
    "Issue Type",
    "Assignee",
    "Custom field (Requirement-Type)",
    "Custom field (Business Process)",
]

def load_csv(file_obj) -> pd.DataFrame:
    """Read and validate the QA defect CSV. Returns a cleaned DataFrame."""
    df = pd.read_csv(file_obj, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    for col in ["Created", "Resolved"]:
        df[col] = pd.to_datetime(
            df[col].astype(str).str.replace(r"\s+", " ", regex=True).str.strip(),
            errors="coerce"
            )


    for c in STRING_COLS:
        df[c] = df[c].fillna("").astype(str).str.strip()

    
    RENAME = {
    "Issue key": "Issue Key",
    "Project key": "Project Key",
    "Created": "Created Date",
    "Resolved": "Resolved Date",
    "Custom field (Requirement-Type)": "Requirement Type",
    "Custom field (Business Process)": "Business Process",
    }
    df = df.rename(columns=RENAME)
    

    return df
