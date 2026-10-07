import pandas as pd

def kpis(df: pd.DataFrame) -> dict:
    """Core KPIs driven by Status Category (stable across projects)."""
    total = int(len(df))
    todo = int((df["Status Category"] == "To Do").sum())
    prog = int((df["Status Category"] == "In Progress").sum())
    done = int((df["Status Category"] == "Done").sum())

    avg_cycle_days = 0.0
    done_df = df[df["Status Category"] == "Done"].copy()
    if not done_df.empty:
        delta = (done_df["Resolved Date"] - done_df["Created Date"]).dt.total_seconds() / 86400
        delta = delta.dropna()
        avg_cycle_days = float(delta.mean()) if not delta.empty else 0.0

    return {
        "total": total,
        "todo": todo,
        "in_progress": prog,
        "done": done,
        "avg_cycle_days": avg_cycle_days,
    }

def status_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Status Category")
          .size()
          .reset_index(name="Count")
          .sort_values("Count", ascending=False)
    )


def throughput_by_week(df: pd.DataFrame) -> pd.DataFrame:
    done_df = df[df["Status Category"] == "Done"].copy()
    if done_df.empty:
        return pd.DataFrame(columns=["Week", "Done Count"])

    done_df["Week"] = done_df["Resolved Date"].dt.to_period("W").dt.start_time
    return (
        done_df.groupby("Week")
               .size()
               .reset_index(name="Done Count")
               .sort_values("Week")
    )


def created_vs_resolved_counts(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    """
    Aggregates Created and Resolved counts by period.

    Parameters
    ----------
    df : issue-level dataframe with datetime columns:
         - "Created Date"
         - "Resolved Date"
    freq : pandas frequency string (e.g., "W-MON", "M", "Q")

    Returns
    -------
    DataFrame indexed by Period with columns ["Created", "Resolved"].
    """

    created = (
        df.dropna(subset=["Created Date"])
          .set_index("Created Date")
          .resample(freq)
          .size()
          .rename("Created")
    )

    resolved = (
        df.dropna(subset=["Resolved Date"])
          .set_index("Resolved Date")
          .resample(freq)
          .size()
          .rename("Resolved")
    )

    out = pd.concat([created, resolved], axis=1).fillna(0).astype(int)
    out.index.name = "Period"
    return out




def aging_open_items(df: pd.DataFrame, asof: pd.Timestamp | None = None) -> pd.DataFrame:
    """Aging for non-done items: age = asof - Created Date (days)."""
    asof = asof or pd.Timestamp.now()
    open_df = df[df["Status Category"] != "Done"].copy()
    open_df["Age Days"] = (asof - open_df["Created Date"]).dt.total_seconds() / 86400
    open_df = open_df[open_df["Age Days"].notna() & (open_df["Age Days"] >= 0)]
    return open_df

def bugs_per_assignee(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Returns a dataframe with columns: Assignee, Bug Count
    Sorted desc, includes top_n (and optionally an 'Other' bucket).
    """
    if "Assignee" not in df.columns:
        raise KeyError("Missing required column: 'Assignee'")

    s = (
        df["Assignee"]
        .astype(str)
        .str.strip()
        .replace({"": "Unassigned", "nan": "Unassigned", "None": "Unassigned"})
        .fillna("Unassigned")
    )

    counts = s.value_counts(dropna=False)

    # Top N + (optional) Other
    if top_n is not None and len(counts) > top_n:
        top = counts.head(top_n)
        other_sum = counts.iloc[top_n:].sum()
        counts = pd.concat([top, pd.Series({"Other": other_sum})])

    out = counts.rename_axis("Assignee").reset_index(name="Bug Count")
    return out


def team_throughput_over_time(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """
    Returns weekly/monthly completed issues count.
    freq: 'W' for weekly, 'M' for monthly
    """
    required = {"Resolved Date", "Status Category"}
    if not required.issubset(df.columns):
        raise KeyError(f"Missing columns: {required}")

    done = df[df["Status Category"] == "Done"].copy()
    done["Resolved Date"] = pd.to_datetime(done["Resolved Date"], errors="coerce")
    done = done.dropna(subset=["Resolved Date"])

    trend = (
        done
        .set_index("Resolved Date")
        .resample(freq)
        .size()
        .reset_index(name="Completed Issues")
    )

    return trend


def priority_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Priority")
          .size()
          .reset_index(name="Count")
          .sort_values("Count", ascending=False)
    )


def status_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Status")
          .size()
          .reset_index(name="Count")
          .sort_values("Count", ascending=False)
    )


def bugs_per_project(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    s = (
        df["Project Key"].astype(str).str.strip()
        .replace({"": "Unknown", "nan": "Unknown", "None": "Unknown"})
        .fillna("Unknown")
    )
    counts = s.value_counts(dropna=False)

    if top_n is not None and len(counts) > top_n:
        top = counts.head(top_n)
        other_sum = counts.iloc[top_n:].sum()
        counts = pd.concat([top, pd.Series({"Other": other_sum})])

    return counts.rename_axis("Project Key").reset_index(name="Bug Count")


def resolution_time_items(df: pd.DataFrame) -> pd.DataFrame:

    done = df[
        (df["Status Category"] == "Done") &
        (df["Resolved Date"].notna()) &
        (df["Created Date"].notna())
    ].copy()

    done["Resolution Days"] = (
        (done["Resolved Date"] - done["Created Date"]).dt.total_seconds() / 86400
    )

    done["Assignee"] = (
        done["Assignee"]
        .fillna("Unassigned")
        .replace({"": "Unassigned"})
    )

    return done

def priority_trend_over_time(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:

    tmp = df.dropna(subset=["Created Date"]).copy()

    tmp["Priority"] = (
        tmp["Priority"]
        .fillna("Not Set")
        .replace({"": "Not Set"})
    )

    trend = (
        tmp.set_index("Created Date")
        .groupby("Priority")
        .resample(freq)
        .size()
        .reset_index(name="Count")
    )

    return trend

