# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 17:19:20 2026

@author: Owner
"""

import streamlit as st
import pandas as pd

from src.metrics import kpis, status_category_breakdown, team_throughput_over_time,aging_open_items, priority_breakdown, status_breakdown, bugs_per_assignee, bugs_per_project, resolution_time_items, priority_trend_over_time
from src.charts import bar_status_category, line_team_trend, hist_aging, bar_priority_breakdown, bar_status_breakdown, bar_bugs_per_assignee, bar_bugs_per_project, box_resolution_time_by_assignee, area_priority_trend

from src.io import load_csv
from generate_report import build_report


st.set_page_config(layout="wide")

st.title("QA Dashboard")

uploaded = st.file_uploader("Upload Jira CSV", type=["csv"])

if uploaded:

    df = load_csv(uploaded)

    st.sidebar.header("Filters")

    project = st.sidebar.multiselect(
        "Project Key",
        sorted(df["Project Key"].dropna().unique())
    )

    assignee = st.sidebar.multiselect(
        "Assignee",
        sorted(df["Assignee"].dropna().unique())
    )

    priority = st.sidebar.multiselect(
        "Priority",
        sorted(df["Priority"].dropna().unique())
    )

    status_cat = st.sidebar.multiselect(
        "Status Category",
        sorted(df["Status Category"].dropna().unique())
    )

    start_date = st.sidebar.date_input(
        "Created Date From",
        value=df["Created Date"].min().date()
    )

    end_date = st.sidebar.date_input(
        "Created Date To",
        value=df["Created Date"].max().date()
    )

    dff = df.copy()

    if project:
        dff = dff[dff["Project Key"].isin(project)]

    if assignee:
        dff = dff[dff["Assignee"].isin(assignee)]

    if priority:
        dff = dff[dff["Priority"].isin(priority)]

    if status_cat:
        dff = dff[dff["Status Category"].isin(status_cat)]

    dff = dff[
        (dff["Created Date"].dt.date >= start_date) &
        (dff["Created Date"].dt.date <= end_date)
    ]

    st.write("Filtered Rows:", len(dff))

    st.dataframe(dff.head(50))
    
    
    
    
    # --- KPI Cards ---
    m = kpis(dff)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", m["total"])
    c2.metric("To Do", m["todo"])
    c3.metric("In Progress", m["in_progress"])
    c4.metric("Done", m["done"])
    c5.metric("Avg Cycle (days)", f'{m["avg_cycle_days"]:.2f}')



    ##########################NEW HEADER
    st.header("By Status")

    # --- Status Category Breakdown ---
    status_df = status_category_breakdown(dff)
    fig_status = bar_status_category(status_df)
    
    st.subheader("Status Category Breakdown")
    st.plotly_chart(fig_status, use_container_width=True)
    
    with st.expander("See breakdown table"):
        st.dataframe(status_df, use_container_width=True)    


    #Status Breakdown (Not Status Category Breakdown)
    st.subheader("Status Breakdown")

    st_df = status_breakdown(dff)
    fig_st = bar_status_breakdown(st_df)
    
    st.plotly_chart(fig_st, use_container_width=True)
    
    with st.expander("See status table"):
        st.dataframe(st_df, use_container_width=True)
        
    
    
    
    #######################NEW HEADER
    st.header("By Creation & Resolution")
    
    #weekly or monthly thorughput depending on selection
    freq_label = st.sidebar.selectbox("Throughput Granularity", ["Weekly", "Monthly"])
    freq = "W" if freq_label == "Weekly" else "M"
    
    st.subheader(f"Throughput Over Time ({freq_label})")

    trend_df = team_throughput_over_time(dff, freq=freq)
    fig_thr = line_team_trend(trend_df)
    
    st.plotly_chart(fig_thr, use_container_width=True)
        
    with st.expander("Show resolved (Done) issues"):
        resolved_done = dff[
            (dff["Status Category"] == "Done") &
            (dff["Resolved Date"].notna())
        ][["Issue Key", "Project Key", "Assignee", "Resolved Date"]]

        st.dataframe(resolved_done, use_container_width=True)


    st.divider()
    
    #aging plot
    st.subheader("Aging (Open Items)")

    aging_df = aging_open_items(dff)
    fig_aging = hist_aging(aging_df)
    
    st.plotly_chart(fig_aging, use_container_width=True)
    
    with st.expander("Show open issues aging list"):
        st.dataframe(
            aging_df[["Issue Key", "Project Key", "Assignee", "Age Days"]],
            use_container_width=True
        )
    
    
    
    
    ############################NEW HEADER
    st.header("By Priority")
    
    #priority breakdown
    st.subheader("Priority Breakdown")

    pri_df = priority_breakdown(dff)
    fig_pri = bar_priority_breakdown(pri_df)
    
    st.plotly_chart(fig_pri, use_container_width=True)
    
    with st.expander("See priority table"):
        st.dataframe(pri_df, use_container_width=True)
        

    #priority trend
    st.subheader("Priority Trend Over Time")

    prio_df = priority_trend_over_time(dff, freq=freq)
    fig_prio = area_priority_trend(prio_df)
    
    st.plotly_chart(fig_prio, use_container_width=True)
    
    with st.expander("See priority trend table"):
        st.dataframe(prio_df, use_container_width=True)

    
    
    
    ############################NEW HEADER
    
    
    
    st.header("Per Assignee/Team")
    
    #bugs per assignee
    st.subheader("Bugs per Assignee")

    assignee_df = bugs_per_assignee(dff)
    fig_assignee = bar_bugs_per_assignee(assignee_df)
    
    st.plotly_chart(fig_assignee, use_container_width=True)
    
    with st.expander("See bugs per assignee table", expanded=False):
        st.dataframe(assignee_df, use_container_width=True)
    
    
    
    #bugs per team
    st.subheader("Bugs per Project")

    proj_df = bugs_per_project(dff)
    fig_proj = bar_bugs_per_project(proj_df)
    
    st.plotly_chart(fig_proj, use_container_width=True)
    
    with st.expander("See bugs per project table", expanded=False):
        st.dataframe(proj_df, use_container_width=True)
    
    
    
    
    #resolution time per assigne box plot
    
    #sidebar for choosing top number of assignees  for box plot
    top_n_assignee = st.sidebar.slider(
        "Top Assignees (by bug volume)",
        5, 25, 10
    )
    
    st.subheader(f"Resolution Time by Top {top_n_assignee} Assignees")

    res_items = resolution_time_items(dff)
    
    top_assignees = (
        res_items["Assignee"]
        .value_counts()
        .head(top_n_assignee)
        .index
    )
    
    res_items = res_items[res_items["Assignee"].isin(top_assignees)]
    
    fig_box = box_resolution_time_by_assignee(res_items)
    
    st.plotly_chart(fig_box, use_container_width=True)
    
    with st.expander("See resolution rows"):
        st.dataframe(res_items, use_container_width=True)
    
    
    
    
    
    
    st.header("By Defect Types - To be included")
    
    st.header("Per Requirement Type - To be included")
    
    st.header("By Business Process - To be included")
    
    
    
    

    
    st.divider()

    html = build_report(dff, title="QA Dashboard Report (Filtered)")

    st.download_button(
        "Export HTML Report",
        data=html.encode("utf-8"),
        file_name="qa_dashboard_report.html",
        mime="text/html"
    )
