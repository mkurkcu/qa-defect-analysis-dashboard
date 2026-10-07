import pandas as pd
import plotly.express as px

def bar_status_category(status_df: pd.DataFrame):
    fig = px.bar(
    status_df,
    x="Status Category",
    y="Count",
    title="Status Category Breakdown",
    text_auto=True
    )
    
    fig.update_traces(
        textfont_size=14,
        textfont_color="orange"
    )
    
    fig.update_layout(bargap=0.2)
    
    return fig


def line_throughput_weekly(thr_df: pd.DataFrame):
    return px.line(thr_df, x="Week", y="Done Count", title="Weekly Throughput (Done)")


def fig_created_vs_resolved_stacked(counts: pd.DataFrame, title: str):
    """
    Builds a stacked bar chart from a counts dataframe.

    counts: index = Period, columns = ["Created", "Resolved"]
    """

    plot_df = counts.reset_index().melt(
        id_vars="Period",
        value_vars=["Created", "Resolved"],
        var_name="Type",
        value_name="Count",
    )

    # Force categorical x-axis to avoid datetime-axis quirks
    plot_df["Period"] = plot_df["Period"].astype(str)

    fig = px.bar(
        plot_df,
        x="Period",
        y="Count",
        color="Type",
        title=title
    )

    # Force stacked mode even if something else overrides defaults
    fig.update_layout(barmode="stack")

    return fig



def hist_aging(aging_df: pd.DataFrame):
    if aging_df.empty:
        return px.histogram(pd.DataFrame({"Age Days": []}), x="Age Days", title="Aging (Open Items)")
    fig = px.histogram(
    aging_df,
    x="Age Days",
    nbins=20,
    title="Aging (Open Items)",
    text_auto=True
    )
    
    fig.update_traces(
        textfont_size=14,
        textfont_color="orange"
    )
    
    fig.update_layout(bargap=0.05)
    
    return fig



def bar_bugs_per_assignee(assignee_df: pd.DataFrame):
    """
    Expects columns: Assignee, Bug Count
    Returns a Plotly figure.
    """
    required = {"Assignee", "Bug Count"}
    if not required.issubset(set(assignee_df.columns)):
        raise KeyError(f"assignee_df must have columns {required}")

    fig = px.bar(
        assignee_df,
        x="Assignee",
        y="Bug Count",
        title="Bugs per Assignee",
    )
    fig.update_layout(xaxis_tickangle=-35)
    return fig

def line_team_trend(trend_df: pd.DataFrame):
    """
    Expects columns: Resolved Date, Completed Issues
    """
    fig = px.line(
        trend_df,
        x="Resolved Date",
        y="Completed Issues",
        markers=True,
        title="Team Throughput Over Time"
    )
    return fig



def bar_priority_breakdown(priority_df: pd.DataFrame):
    fig = px.bar(
        priority_df,
        x="Priority",
        y="Count",
        title="Priority Breakdown",
        text_auto=True
    )
    fig.update_traces(textfont_size=14, textfont_color="orange")
    fig.update_layout(bargap=0.2)
    return fig


def bar_status_breakdown(status_df: pd.DataFrame):
    fig = px.bar(
        status_df,
        x="Status",
        y="Count",
        title="Status Breakdown",
        text_auto=True
    )
    fig.update_traces(textfont_size=14, textfont_color="orange")
    fig.update_layout(bargap=0.2)
    return fig


def bar_bugs_per_project(project_df: pd.DataFrame):
    required = {"Project Key", "Bug Count"}
    if not required.issubset(set(project_df.columns)):
        raise KeyError(f"project_df must have columns {required}")

    fig = px.bar(
        project_df,
        x="Project Key",
        y="Bug Count",
        title="Bugs per Project",
        text_auto=True
    )
    fig.update_traces(textfont_size=14, textfont_color="orange")
    fig.update_layout(bargap=0.2)
    fig.update_layout(xaxis_tickangle=-35)
    return fig


def box_resolution_time_by_assignee(res_df: pd.DataFrame):

    fig = px.box(
        res_df,
        x="Assignee",
        y="Resolution Days",
        points="outliers",
        title="Resolution Time by Assignee (Days)"
    )

    fig.update_layout(xaxis_tickangle=-35)

    return fig

def area_priority_trend(trend_df: pd.DataFrame):

    fig = px.area(
        trend_df,
        x="Created Date",
        y="Count",
        color="Priority",
        title="Priority Trend Over Time"
    )

    return fig


