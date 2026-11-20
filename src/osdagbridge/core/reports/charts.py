"""Render numeric report data using a non-interactive Matplotlib canvas."""
from math import isfinite
from pathlib import Path

from matplotlib.figure import Figure

from .report_utils import _fig_embed
from .styles import CHART_COLOR, FAIL_COLOR


def bar_chart(directory, name, caption, values, unit, *, limit=None):
    labels, heights = [], []
    for label, value in values.items():
        try:
            number = float(value)
        except (ValueError, TypeError):
            continue
        if isfinite(number):
            labels.append(label)
            heights.append(number)
    if not heights:
        return ""

    figure = Figure(figsize=(8, 3.8), layout="constrained")
    axes = figure.subplots()
    colors = [FAIL_COLOR if limit is not None and value > limit else CHART_COLOR
              for value in heights]
    bars = axes.bar(range(len(labels)), heights, color=colors)
    axes.set_xticks(range(len(labels)), labels, fontsize=8)
    axes.set_ylabel(unit)
    axes.bar_label(bars, fmt="%.2f", padding=2, fontsize=8)
    if limit is not None:
        axes.axhline(limit, color=FAIL_COLOR, linestyle="--", label="UR = 1.0")
        axes.legend(loc="upper right")
    axes.set_ylim(0, max(max(heights), limit or 0, 0.01) * 1.2)
    path = Path(directory) / (name + ".png")
    figure.savefig(path, dpi=150)
    return _fig_embed(path.parent.name + "/" + path.name, caption)


def utilization_charts(directory, ratios):
    for group in ("Girder", "Deck", "Cross Bracing", "End Diaphragm"):
        values = ratios.get(group, {})
        if values:
            yield bar_chart(directory, group.replace(" ", "_"), group + " utilization ratios",
                            values, "Utilization ratio", limit=1.0)
        else:
            yield r"\par\noindent " + group + " utilization ratios unavailable." + r"\par"


def material_charts(directory, quantities):
    """The bill of materials reports structural and reinforcement steel in MT."""
    steel = {"Girders": quantities.get("steel_girders_wt_total"),
             "Top chord": quantities.get("bracing_top_wt_total"),
             "Bottom chord": quantities.get("bracing_bot_wt_total"),
             "Diagonal": quantities.get("bracing_diag_wt_total")}
    yield bar_chart(directory, "steel", "Structural steel quantities",
                    steel, "Weight (MT)")
    yield bar_chart(directory, "concrete", "Concrete volume",
                    {"Deck": quantities.get("concrete_deck_vol_total")}, "Volume (m\u00b3)")
    yield bar_chart(directory, "rebar", "Reinforcement steel weight",
                    {"Reinforcement": quantities.get("rebar_deck_wt_total")}, "Weight (MT)")
