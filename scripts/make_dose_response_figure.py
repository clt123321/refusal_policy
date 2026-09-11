import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path("artifacts/safe_mech")
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

rows = list(csv.DictReader(open(OUT_DIR / "l27_dose_response.csv")))
alphas = [float(r["alpha"]) for r in rows]
margins = [float(r["mean_logit_margin"]) for r in rows]
ci_low = [float(r["logit_margin_ci_low"]) for r in rows]
ci_high = [float(r["logit_margin_ci_high"]) for r in rows]
abstain = [float(r["abstain_rate"]) for r in rows]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].plot(alphas, margins, "-o", color="tab:blue")
axes[0].fill_between(alphas, ci_low, ci_high, alpha=0.2, color="tab:blue")
axes[0].axhline(0, color="black", linewidth=0.8)
axes[0].axvline(0, color="gray", linewidth=0.8, linestyle="--")
axes[0].set_xlabel("alpha (scaled removal of L27 MLP's own P-projection)")
axes[0].set_ylabel("policy logit margin: logit(' I') - logit(' The')")
axes[0].set_title("alpha vs policy logit margin")

axes[1].plot(alphas, abstain, "-s", color="tab:orange")
axes[1].axvline(0, color="gray", linewidth=0.8, linestyle="--")
axes[1].set_xlabel("alpha")
axes[1].set_ylabel("abstain rate (generation)")
axes[1].set_title("alpha vs behavior rate")

fig.suptitle("Figure Final-A: L27 MLP dose-response (monotonic)")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(FIG_DIR / "figure_final_a_dose_response.png", dpi=150)
print("done")
