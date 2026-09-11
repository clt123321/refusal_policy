import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("artifacts/safe_mech")
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def figure_a():
    rows = list(csv.DictReader(open(OUT_DIR / "intervention_audit_layerwise_projection.csv")))
    by_scope = {}
    for r in rows:
        by_scope.setdefault(r["scope"], {})[int(r["layer"])] = float(r["mean_abs_projection"])
    fig, ax = plt.subplots(figsize=(8, 5))
    for scope, style in [("baseline", "-o"), ("remove_L18", "-s"), ("remove_L18_23", "-^"), ("remove_all_0_27", "-d")]:
        vals = by_scope[scope]
        layers = sorted(vals)
        ax.plot(layers, [vals[l] for l in layers], style, label=scope, markersize=4)
    ax.set_xlabel("layer")
    ax.set_ylabel("mean |projection| onto that layer's own P direction")
    ax.set_title("Figure A: P projection after intervention, across layers")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_a_projection_curve.png", dpi=150)
    plt.close(fig)


def figure_b():
    scores = json.loads((OUT_DIR / "module_writer_scores_all.json").read_text())
    num_layers = 28
    grid = np.full((num_layers, 2), np.nan)
    for key, val in scores.items():
        layer_str, module = key.split("_", 1)
        layer = int(layer_str[1:])
        col = 0 if module == "attn_output" else 1
        grid[layer, col] = val
    fig, ax = plt.subplots(figsize=(4, 9))
    im = ax.imshow(grid, aspect="auto", cmap="RdBu_r", vmin=-12, vmax=12)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["attn_output", "mlp_output"])
    ax.set_yticks(range(num_layers))
    ax.set_ylabel("layer")
    ax.set_title("Figure B: writer score\n(abstain - answer projection)")
    fig.colorbar(im, ax=ax, shrink=0.6)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_b_writer_heatmap.png", dpi=150)
    plt.close(fig)


def figure_c():
    rows = list(csv.DictReader(open(OUT_DIR / "writer_subset_removal.csv")))
    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(rows))
    colors = ["tab:orange" if "L27_mlp_output" in r["subset"] else "tab:gray" for r in rows]
    effects = [float(r["necessity_effect_pp"]) for r in rows]
    ci_low = [float(r["ci_low_pp"]) for r in rows]
    ci_high = [float(r["ci_high_pp"]) for r in rows]
    yerr = [[e - l for e, l in zip(effects, ci_low)], [h - e for e, h in zip(effects, ci_high)]]
    ax.bar(x, effects, yerr=yerr, color=colors, capsize=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels([r["subset"].replace("_output", "").replace("L", "L") for r in rows], rotation=75, ha="right", fontsize=7)
    ax.set_ylabel("necessity effect (pp)")
    ax.set_title("Figure C: writer subset removal vs policy behavior\n(orange = subset contains L27 mlp_output)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_c_writer_subsets.png", dpi=150)
    plt.close(fig)


def figure_d():
    rows = list(csv.DictReader(open(OUT_DIR / "subspace_removal.csv")))
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ks = [int(r["k"]) for r in rows]
    effects = [float(r["necessity_effect_pp"]) for r in rows]
    ci_low = [float(r["ci_low_pp"]) for r in rows]
    ci_high = [float(r["ci_high_pp"]) for r in rows]
    yerr = [[e - l for e, l in zip(effects, ci_low)], [h - e for e, h in zip(effects, ci_high)]]
    ax.bar([str(k) for k in ks], effects, yerr=yerr, color="tab:purple", capsize=4)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("k (subspace dimensions removed per layer, L18-23)")
    ax.set_ylabel("necessity effect (pp)")
    ax.set_title("Figure D: k-dimensional subspace removal\nvs policy behavior")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_d_subspace_removal.png", dpi=150)
    plt.close(fig)


def figure_e():
    rows = list(csv.DictReader(open(OUT_DIR / "writer_parameter_sensitivity.csv")))
    writers = sorted({r["writer_a"] for r in rows} | {r["writer_b"] for r in rows})
    blocks = sorted({r["block"] for r in rows})
    fig, axes = plt.subplots(1, len(blocks), figsize=(4 * len(blocks), 4))
    for ax, block in zip(axes, blocks):
        grid = np.eye(len(writers))
        for r in rows:
            if r["block"] != block:
                continue
            i, j = writers.index(r["writer_a"]), writers.index(r["writer_b"])
            grid[i, j] = grid[j, i] = float(r["cosine"])
        im = ax.imshow(grid, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks(range(len(writers)))
        ax.set_xticklabels(writers, rotation=45, ha="right", fontsize=7)
        ax.set_yticks(range(len(writers)))
        ax.set_yticklabels(writers, fontsize=7)
        ax.set_title(block, fontsize=9)
    fig.suptitle("Figure E: writer x parameter-block co-sensitivity (cosine)")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(FIG_DIR / "figure_e_parameter_cosensitivity.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    figure_a()
    figure_b()
    figure_c()
    figure_d()
    figure_e()
    print("done")
