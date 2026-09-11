import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path("artifacts/safe_mech")
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def figure_s1():
    rows = load_csv(OUT_DIR / "safe_hxp_layer_scan.csv")
    layers = [int(r["layer"]) for r in rows]
    p_sep = [float(r["p_separation_dev_effect_size"]) for r in rows]
    h_leak = [float(r["h_leakage_on_p_direction_dev"]) for r in rows]
    h_sep = [float(r["h_separation_dev_effect_size"]) for r in rows]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(layers, p_sep, marker="o", label="P separation on dev (abstain vs answer)", color="tab:blue")
    ax.plot(layers, h_leak, marker="s", label="H leakage on P direction (cooking vs astronomy)", color="tab:red")
    ax.plot(layers, h_sep, marker="^", label="H separation on dev (content, on H direction)", color="tab:green", alpha=0.6)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("layer")
    ax.set_ylabel("standardized effect size")
    ax.set_title("Figure S1: layer-wise H vs P representation (SAFE_MECH_BENIGN_PROXY)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_s1_layer_hxp.png", dpi=150)
    plt.close(fig)


def figure_s2():
    controls = json.loads((OUT_DIR / "safe_negative_controls.json").read_text())
    main = json.loads((OUT_DIR / "causal_policy_intervention_multilayer.json").read_text())
    names = ["main"] + [c["control"] for c in controls]
    suff = [main["sufficiency_effect_pp"]] + [c["sufficiency_effect_pp"] for c in controls]
    suff_ci = [
        (main["sufficiency_effect_pp"] - main["sufficiency_ci_pp"][0], main["sufficiency_ci_pp"][1] - main["sufficiency_effect_pp"])
    ] + [(c["sufficiency_effect_pp"] - c["sufficiency_ci_pp"][0], c["sufficiency_ci_pp"][1] - c["sufficiency_effect_pp"]) for c in controls]
    nec = [main["necessity_effect_pp"]] + [c["necessity_effect_pp"] for c in controls]
    nec_ci = [
        (main["necessity_effect_pp"] - main["necessity_ci_pp"][0], main["necessity_ci_pp"][1] - main["necessity_effect_pp"])
    ] + [(c["necessity_effect_pp"] - c["necessity_ci_pp"][0], c["necessity_ci_pp"][1] - c["necessity_effect_pp"]) for c in controls]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    x = range(len(names))
    colors = ["tab:blue"] + ["tab:gray"] * len(controls)
    axes[0].bar(x, suff, yerr=[[a for a, _ in suff_ci], [b for _, b in suff_ci]], color=colors, capsize=4)
    axes[0].set_xticks(list(x))
    axes[0].set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    axes[0].set_ylabel("effect (percentage points)")
    axes[0].set_title("Sufficiency (ADD):\nabstain-rate increase, natural prompts", fontsize=10)
    axes[0].axhline(0, color="black", linewidth=0.8)

    axes[1].bar(x, nec, yerr=[[a for a, _ in nec_ci], [b for _, b in nec_ci]], color=colors, capsize=4)
    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    axes[1].set_title("Necessity (REMOVE):\ncompliant-rate increase, abstain-instructed prompts", fontsize=10)
    axes[1].axhline(0, color="black", linewidth=0.8)

    fig.suptitle("Figure S2: main causal intervention vs negative controls (95% CI)")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(FIG_DIR / "figure_s2_causal_vs_controls.png", dpi=150)
    plt.close(fig)


def figure_s3():
    single = json.loads((OUT_DIR / "causal_policy_intervention.json").read_text())
    multi = json.loads((OUT_DIR / "causal_policy_intervention_multilayer.json").read_text())
    full = json.loads((OUT_DIR / "c05_full_depth_necessity.json").read_text())

    scopes = ["1 layer\n(L18)", "6 layers\n(L18-23)", "28 layers\n(all)"]
    necessity = [single["necessity_effect_pp"], multi["necessity_effect_pp"], full["necessity_effect_pp"]]
    necessity_ci = [
        (single["necessity_effect_pp"] - single["necessity_ci_pp"][0], single["necessity_ci_pp"][1] - single["necessity_effect_pp"]),
        (multi["necessity_effect_pp"] - multi["necessity_ci_pp"][0], multi["necessity_ci_pp"][1] - multi["necessity_effect_pp"]),
        (full["necessity_effect_pp"] - full["necessity_ci_pp"][0], full["necessity_ci_pp"][1] - full["necessity_effect_pp"]),
    ]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    x = range(len(scopes))
    ax.bar(x, necessity, yerr=[[a for a, _ in necessity_ci], [b for _, b in necessity_ci]], color="tab:orange", capsize=5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axhline(20, color="tab:red", linewidth=0.8, linestyle="--", label="TODO Gate-1 reference: 20 pp")
    ax.set_xticks(list(x))
    ax.set_xticklabels(scopes)
    ax.set_ylabel("necessity effect (percentage points)")
    ax.set_title("Figure S3: ablation scope vs necessity effect\n(broader removal does not rescue necessity)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_s3_writer_scope.png", dpi=150)
    plt.close(fig)


def figure_s4():
    sentinel = json.loads((OUT_DIR / "c05_shared_gate_sentinel.json").read_text())
    labels = ["baseline\n(no upstream ablation)", "upstream ablated\n(L18-23 removed)"]
    values = [sentinel["baseline_sentinel_separation_effect_size"], sentinel["upstream_ablated_sentinel_separation_effect_size"]]

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.bar(labels, values, color=["tab:blue", "tab:purple"])
    ax.set_ylabel("late-gate (L27) P-projection separation\n(standardized effect size)")
    ax.set_title(f"Figure S4: shared-gate sentinel readout\nretention fraction = {sentinel['retention_fraction']:.2f}")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "figure_s4_shared_gate.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    figure_s1()
    figure_s2()
    figure_s3()
    figure_s4()
    print("figures written to", FIG_DIR)
