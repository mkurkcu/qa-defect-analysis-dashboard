import argparse
from pathlib import Path

from tkinter import Tk
from tkinter.filedialog import askopenfilename


import pandas as pd
import plotly.io as pio

from src.io import load_csv
from src.metrics import (
    kpis,
    status_category_breakdown,
    
    throughput_by_week,
    aging_open_items,
    bugs_per_assignee,
    team_throughput_over_time
)
from src.charts import (
    bar_status_category,
    line_throughput_weekly,
    hist_aging,
    bar_bugs_per_assignee,
    line_team_trend
)

def _kpi_cards(m: dict) -> str:
    def card(title: str, value: str) -> str:
        return f"""
        <div class="card">
          <div class="card-title">{title}</div>
          <div class="card-value">{value}</div>
        </div>
        """
    return f"""
    <div class="cards">
      {card("Total", str(m["total"]))}
      {card("To Do", str(m["todo"]))}
      {card("In Progress", str(m["in_progress"]))}
      {card("Done", str(m["done"]))}
      {card("Avg Cycle (days)", f'{m["avg_cycle_days"]:.2f}')}
    </div>
    """

def build_report(df: pd.DataFrame, title: str = "QA Dashboard Report") -> str:
    m = kpis(df)

    status_df = status_category_breakdown(df)
    
    thr_df = throughput_by_week(df)
    aging_df = aging_open_items(df)
    assignee_df = bugs_per_assignee(df)
    team_trend_df = team_throughput_over_time(df)
    

    figs = [
        ("Status Category Breakdown", bar_status_category(status_df)),
        
        ("Weekly Throughput (Done)", line_throughput_weekly(thr_df)),
        ("Aging (Open Items)", hist_aging(aging_df)),
        ("Bugs per Assignee", bar_bugs_per_assignee(assignee_df)),
        ("Team Throughput Over Time", line_team_trend(team_trend_df)),
    ]

    charts_html = ""
    first = True
    for _, fig in figs:
        charts_html += "<div class='chart'>"
        charts_html += pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs=("inline" if first else False),
            config={"displaylogo": False},
        )
        charts_html += "</div>"
        first = False

    html = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; background: #fafafa; color: #111; }}
    header {{ padding: 20px 24px; background: white; border-bottom: 1px solid #eee; }}
    header h1 {{ margin: 0; font-size: 20px; }}
    header .sub {{ margin-top: 6px; color: #666; font-size: 13px; }}
    main {{ padding: 18px 24px; max-width: 1200px; margin: 0 auto; }}
    .cards {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; margin-bottom: 14px; }}
    .card {{ background: white; border: 1px solid #eee; border-radius: 12px; padding: 12px; }}
    .card-title {{ color: #666; font-size: 12px; }}
    .card-value {{ font-size: 22px; font-weight: 700; margin-top: 6px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    .panel {{ background: white; border: 1px solid #eee; border-radius: 12px; padding: 14px; }}
    .panel h2 {{ margin: 0 0 10px 0; font-size: 15px; }}
    .muted {{ color: #666; font-size: 13px; }}
    .chart {{ width: 100%; }}
    .table {{ width: 100%; border-collapse: collapse; }}
    .table th, .table td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #eee; font-size: 13px; }}
    .table th {{ background: #fcfcfc; }}
    @media (max-width: 1000px) {{
      .cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <div class="sub">Static HTML export (no server). Generated from CSV using the same metrics functions.</div>
  </header>
  <main>
    {_kpi_cards(m)}
    <div class="grid">
      <section class="panel">
        <h2>Charts</h2>
        {charts_html}
      </section>
      <section class="panel">
        <h2>Breakdowns</h2>
        <p class="muted">Top counts based on the full dataset used to generate this report.</p>
        {status_df.to_html(index=False, classes="table", border=0)}

      </section>
    </div>

    <div style="height:14px"></div>
    <section class="panel">
      <h2>Data Preview (first 50 rows)</h2>
      {df.head(50).to_html(index=False, classes="table", border=0) if not df.empty else "<p class='muted'>No rows.</p>"}
    </section>
  </main>
</body>
</html>
"""
    return html

def pick_csv() -> str:
    root = Tk()
    root.withdraw()  # pencereyi gizle
    path = askopenfilename(
        title="Select QA CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return path





def main():
    p = argparse.ArgumentParser(description="Generate a static QA dashboard HTML report from a CSV.")
    p.add_argument("--input", "-i", required=False, help="Path to input CSV (if omitted, a file picker opens)")
    p.add_argument("--output", "-o", default="report.html", help="Path to output HTML file")
    p.add_argument("--title", default="QA Dashboard Report", help="Report title")
    args = p.parse_args()

    if not args.input:
        picked = pick_csv()
        if not picked:
            print("No file selected. Exiting.")
            return
        args.input = picked




    inp = Path(args.input)
    out = Path(args.output)

    with inp.open("rb") as f:
        df = load_csv(f)

    html = build_report(df, title=args.title)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote: {out.resolve()}")

if __name__ == "__main__":
    main()
