#!/usr/bin/env python3
"""Monte Carlo psychometric simulation for Lex30 scoring formulas.

Calibrated to Japanese EFL university learner empirical distributions
(Fitzpatrick & Clenton, 2010; Baba, 2009; Uchihara, Eguchi, & Clenton, 2021;
Higginbotham, Munby, & Racine, 2015 [J-WADE]) and evaluated on the actual
8,000-word NJ8 rank list and 30 POS-balanced cues in this repository.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "tools" / "data"
NJ8_CSV_PATH = DATA_ROOT / "NJ8" / "NJ8.csv"
HALVES_JSON_PATH = DATA_ROOT / "parallel_split_halves.json"

SCORING_METHODS = (
    "nj8_token_score",
    "nj8_type_score",
    "nj8_token_percent_of_lexical_tokens",
    "nj8_token_percent_of_response_slots",
    "nj8_polytomous_token_score",
    "nj8_polytomous_type_score",
    "nj8_polytomous_type_no_clang_score",
    "nj8_unique_cue_polytomous_no_clang_score",
    "nj8_eb_type_sophistication",
    "nj8_k2plus_within_10s",
)

SCENARIOS: dict[str, dict[str, Any]] = {
    "jp_efl_mixed_univ": {
        "description": "Mixed Japanese university EFL cohort (CEFR A2-B2, ~71% K1 responses, ~65% slot fill)",
        "theta_mean": 0.0,
        "theta_sd": 1.0,
        "fill_intercept": 1.55,
        "mishear_base_rate": 0.0,
        "recycler_rate": 0.15,
        "clanger_rate": 0.12,
    },
    "listening_spoken_v04_v05": {
        "description": "Listening/Spoken v0.4-v0.5 cohort (cue mishearing at low proficiency + spoken hesitation)",
        "theta_mean": 0.0,
        "theta_sd": 1.0,
        "fill_intercept": 1.05,
        "mishear_base_rate": 0.14,
        "recycler_rate": 0.15,
        "clanger_rate": 0.16,
    },
    "homogeneous_intermediate_b1": {
        "description": "Restricted-range intact intermediate class (theta ~ N(0.35, 0.45^2))",
        "theta_mean": 0.35,
        "theta_sd": 0.45,
        "fill_intercept": 1.65,
        "mishear_base_rate": 0.04,
        "recycler_rate": 0.15,
        "clanger_rate": 0.12,
    },
    "high_proficiency_b2_c1": {
        "description": "Upper-intermediate / advanced cohort (theta ~ N(1.10, 0.55^2), ceiling stress test)",
        "theta_mean": 1.10,
        "theta_sd": 0.55,
        "fill_intercept": 2.05,
        "mishear_base_rate": 0.02,
        "recycler_rate": 0.12,
        "clanger_rate": 0.10,
    },
}


def load_nj8_bands(path: Path = NJ8_CSV_PATH) -> dict[int, list[tuple[str, int]]]:
    bands: dict[int, list[tuple[str, int]]] = {b: [] for b in range(1, 9)}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            try:
                rank = int(row[0].strip())
                word = row[1].strip().lower()
            except ValueError:
                continue
            if 1 <= rank <= 8000 and word.isalpha():
                band = (rank - 1) // 1000 + 1
                bands[band].append((word, rank))
    return bands


def load_parallel_halves(path: Path = HALVES_JSON_PATH) -> tuple[list[str], list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    entry = payload["sets"]["updated-easycue-posbalanced-pilot-30-v0.3"]
    return list(entry["form_a"]), list(entry["form_b"])


def pearson_r(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return 0.0
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den > 1e-12 else 0.0


def partial_r(xs: list[float], ys: list[float], control: list[float]) -> float:
    rxy = pearson_r(xs, ys)
    rxc = pearson_r(xs, control)
    ryc = pearson_r(ys, control)
    denom = math.sqrt(max(1e-12, (1.0 - rxc ** 2) * (1.0 - ryc ** 2)))
    return (rxy - rxc * ryc) / denom


def simulate_scenario(
    scenario_id: str,
    *,
    n_learners: int = 600,
    seed: int = 20261108,
    bands: dict[int, list[tuple[str, int]]] | None = None,
    halves: tuple[list[str], list[str]] | None = None,
) -> dict[str, Any]:
    spec = SCENARIOS[scenario_id]
    rng = random.Random(seed + sum(ord(c) for c in scenario_id))
    bands = bands or load_nj8_bands()
    form_a, form_b = halves or load_parallel_halves()
    form_a_set = set(form_a)
    cues = form_a + form_b

    cue_deltas: dict[str, float] = {}
    for idx, (ca, cb) in enumerate(zip(form_a, form_b)):
        off = -0.42 + 0.06 * idx
        cue_deltas[ca] = off
        cue_deltas[cb] = off + rng.uniform(-0.015, 0.015)

    pools = {b: bands[b][:400] for b in range(1, 9)}
    recycled_k3_pool = bands[3][:12]
    clang_k6_pool = bands[6][:30]

    # Zipf/band baseline log-priors calibrated to Japanese EFL response distributions (~71% K1 at theta=0)
    band_priors = {1: 2.38, 2: 0.92, 3: 0.18, 4: -0.48, 5: -1.08, 6: -1.68, 7: -2.22, 8: -2.78}
    band_betas = {1: -2.0, 2: -0.55, 3: 0.22, 4: 0.85, 5: 1.35, 6: 1.80, 7: 2.20, 8: 2.55}
    band_discrim = 1.35

    thetas: list[float] = []
    taus: list[float] = []
    verbosities: list[float] = []
    uvlt_criterion: list[float] = []
    recyclers: list[float] = []
    clangers: list[float] = []

    scores: dict[str, list[float]] = {m: [] for m in SCORING_METHODS}
    half_a_scores: dict[str, list[float]] = {m: [] for m in SCORING_METHODS}
    half_b_scores: dict[str, list[float]] = {m: [] for m in SCORING_METHODS}

    for _ in range(n_learners):
        theta = rng.gauss(spec["theta_mean"], spec["theta_sd"])
        tau = 0.50 * theta + math.sqrt(1.0 - 0.50 ** 2) * rng.gauss(0.0, 1.0)
        nu = rng.gauss(0.0, 1.0)  # Orthogonal talkativeness/typing-quantity nuisance
        # Simulated external vocabulary criterion (e.g. UVLT-CAT Stage 1 with reliability ~0.86)
        uvlt = 0.85 * theta + math.sqrt(1.0 - 0.85 ** 2) * rng.gauss(0.0, 1.0)
        is_recycler = 1.0 if rng.random() < spec["recycler_rate"] else 0.0
        is_clanger = 1.0 if rng.random() < spec["clanger_rate"] else 0.0

        thetas.append(theta)
        taus.append(tau)
        verbosities.append(nu)
        uvlt_criterion.append(uvlt)
        recyclers.append(is_recycler)
        clangers.append(is_clanger)

        seen_all: set[str] = set()
        seen_nc_all: set[str] = set()
        seen_a: set[str] = set()
        seen_nc_a: set[str] = set()
        seen_b: set[str] = set()
        seen_nc_b: set[str] = set()
        cues_all: dict[str, set[str]] = {}
        nc_pts_all: dict[str, int] = {}
        cues_a: dict[str, set[str]] = {}
        nc_pts_a: dict[str, int] = {}
        cues_b: dict[str, set[str]] = {}
        nc_pts_b: dict[str, int] = {}

        bin_tok = bin_typ = poly_tok = poly_typ = poly_typ_nc = k2_10s = lex_cnt = 0
        a_bin_tok = a_bin_typ = a_poly_tok = a_poly_typ = a_poly_nc = a_k2_10s = a_lex = 0
        b_bin_tok = b_bin_typ = b_poly_tok = b_poly_typ = b_poly_nc = b_k2_10s = b_lex = 0

        for cue in cues:
            in_a = cue in form_a_set
            delta = cue_deltas[cue]
            cum_ms = 0.0

            # In listening mode, low-proficiency learners occasionally mishear the cue,
            # triggering either clang or high-frequency K1 fallback associations.
            mishear_prob = spec["mishear_base_rate"] / (1.0 + math.exp(1.1 * (theta + 0.3)))
            misheard_cue = rng.random() < mishear_prob

            weights: list[float] = []
            for b in range(1, 9):
                eff_theta = (theta - 0.85) if misheard_cue else theta
                access = 1.0 / (1.0 + math.exp(-band_discrim * (eff_theta + delta - band_betas[b])))
                weights.append(math.exp(band_priors[b]) * access)
            w_sum = sum(weights)
            probs = [w / w_sum for w in weights]

            for slot in range(1, 5):
                logit_fill = spec["fill_intercept"] - 0.62 * (slot - 1) + 0.90 * nu + 0.42 * theta
                if misheard_cue:
                    logit_fill -= 0.55
                if rng.random() > (1.0 / (1.0 + math.exp(-logit_fill))):
                    continue

                base_ms = 2400.0 if slot == 1 else 3600.0
                slot_ms = base_ms * math.exp(-0.28 * tau - 0.14 * nu + rng.gauss(0.0, 0.25))
                cum_ms += slot_ms
                if cum_ms > 30000.0:
                    continue

                lex_cnt += 1
                is_clang = False
                if is_recycler and rng.random() < 0.30:
                    word, _rank = rng.choice(recycled_k3_pool)
                    band = 3
                elif (is_clanger or misheard_cue) and slot <= 2 and rng.random() < 0.26:
                    word, _rank = rng.choice(clang_k6_pool)
                    band = 6
                    is_clang = True
                else:
                    u = rng.random()
                    acc = 0.0
                    band = 1
                    for b_idx, p in enumerate(probs, start=1):
                        acc += p
                        if u <= acc:
                            band = b_idx
                            break
                    word, _rank = rng.choice(pools[band])

                b_pt = 1 if band >= 2 else 0
                p_pt = 0 if band <= 1 else (1 if band == 2 else (2 if band == 3 else 3))
                in_10s = 1 if (b_pt > 0 and cum_ms <= 10000.0) else 0

                bin_tok += b_pt
                poly_tok += p_pt
                k2_10s += in_10s
                cues_all.setdefault(word, set()).add(cue)
                if word not in seen_all:
                    seen_all.add(word)
                    bin_typ += b_pt
                    poly_typ += p_pt
                if not is_clang and word not in seen_nc_all:
                    seen_nc_all.add(word)
                    poly_typ_nc += p_pt
                    nc_pts_all[word] = p_pt

                if in_a:
                    a_lex += 1
                    a_bin_tok += b_pt
                    a_poly_tok += p_pt
                    a_k2_10s += in_10s
                    cues_a.setdefault(word, set()).add(cue)
                    if word not in seen_a:
                        seen_a.add(word)
                        a_bin_typ += b_pt
                        a_poly_typ += p_pt
                    if not is_clang and word not in seen_nc_a:
                        seen_nc_a.add(word)
                        a_poly_nc += p_pt
                        nc_pts_a[word] = p_pt
                else:
                    b_lex += 1
                    b_bin_tok += b_pt
                    b_poly_tok += p_pt
                    b_k2_10s += in_10s
                    cues_b.setdefault(word, set()).add(cue)
                    if word not in seen_b:
                        seen_b.add(word)
                        b_bin_typ += b_pt
                        b_poly_typ += p_pt
                    if not is_clang and word not in seen_nc_b:
                        seen_nc_b.add(word)
                        b_poly_nc += p_pt
                        nc_pts_b[word] = p_pt

        unique_cue_nc = sum(pts for w, pts in nc_pts_all.items() if len(cues_all.get(w, ())) == 1)
        a_unique_cue_nc = sum(pts for w, pts in nc_pts_a.items() if len(cues_a.get(w, ())) == 1)
        b_unique_cue_nc = sum(pts for w, pts in nc_pts_b.items() if len(cues_b.get(w, ())) == 1)

        scores["nj8_token_score"].append(float(bin_tok))
        scores["nj8_type_score"].append(float(bin_typ))
        scores["nj8_token_percent_of_lexical_tokens"].append(100.0 * bin_tok / lex_cnt if lex_cnt else 0.0)
        scores["nj8_token_percent_of_response_slots"].append(100.0 * bin_tok / 120.0)
        scores["nj8_polytomous_token_score"].append(float(poly_tok))
        scores["nj8_polytomous_type_score"].append(float(poly_typ))
        scores["nj8_polytomous_type_no_clang_score"].append(float(poly_typ_nc))
        scores["nj8_unique_cue_polytomous_no_clang_score"].append(float(unique_cue_nc))
        scores["nj8_eb_type_sophistication"].append((poly_typ_nc + 20.0 * 0.35) / (len(seen_nc_all) + 20.0))
        scores["nj8_k2plus_within_10s"].append(float(k2_10s))

        half_a_scores["nj8_token_score"].append(float(a_bin_tok))
        half_a_scores["nj8_type_score"].append(float(a_bin_typ))
        half_a_scores["nj8_token_percent_of_lexical_tokens"].append(100.0 * a_bin_tok / a_lex if a_lex else 0.0)
        half_a_scores["nj8_token_percent_of_response_slots"].append(100.0 * a_bin_tok / 60.0)
        half_a_scores["nj8_polytomous_token_score"].append(float(a_poly_tok))
        half_a_scores["nj8_polytomous_type_score"].append(float(a_poly_typ))
        half_a_scores["nj8_polytomous_type_no_clang_score"].append(float(a_poly_nc))
        half_a_scores["nj8_unique_cue_polytomous_no_clang_score"].append(float(a_unique_cue_nc))
        half_a_scores["nj8_eb_type_sophistication"].append((a_poly_nc + 10.0 * 0.35) / (len(seen_nc_a) + 10.0))
        half_a_scores["nj8_k2plus_within_10s"].append(float(a_k2_10s))

        half_b_scores["nj8_token_score"].append(float(b_bin_tok))
        half_b_scores["nj8_type_score"].append(float(b_bin_typ))
        half_b_scores["nj8_token_percent_of_lexical_tokens"].append(100.0 * b_bin_tok / b_lex if b_lex else 0.0)
        half_b_scores["nj8_token_percent_of_response_slots"].append(100.0 * b_bin_tok / 60.0)
        half_b_scores["nj8_polytomous_token_score"].append(float(b_poly_tok))
        half_b_scores["nj8_polytomous_type_score"].append(float(b_poly_typ))
        half_b_scores["nj8_polytomous_type_no_clang_score"].append(float(b_poly_nc))
        half_b_scores["nj8_unique_cue_polytomous_no_clang_score"].append(float(b_unique_cue_nc))
        half_b_scores["nj8_eb_type_sophistication"].append((b_poly_nc + 10.0 * 0.35) / (len(seen_nc_b) + 10.0))
        half_b_scores["nj8_k2plus_within_10s"].append(float(b_k2_10s))

    median_theta = statistics.median(thetas)
    upper_idx = [i for i, th in enumerate(thetas) if th >= median_theta]

    method_rows: list[dict[str, Any]] = []
    for method in SCORING_METHODS:
        vals = scores[method]
        r_ab = pearson_r(half_a_scores[method], half_b_scores[method])
        sb_30 = (2.0 * r_ab) / (1.0 + r_ab) if (1.0 + r_ab) > 0 else 0.0
        method_rows.append(
            {
                "scenario": scenario_id,
                "scoring_method": method,
                "mean": round(statistics.fmean(vals), 3),
                "sd": round(statistics.stdev(vals), 3),
                "r_true_theta": round(pearson_r(vals, thetas), 3),
                "r_uvlt_external": round(pearson_r(vals, uvlt_criterion), 3),
                "r_upper_half_theta": round(
                    pearson_r([vals[i] for i in upper_idx], [thetas[i] for i in upper_idx]), 3
                ),
                "partial_r_verbosity_bias": round(partial_r(vals, verbosities, thetas), 3),
                "partial_r_recycling_gaming": round(partial_r(vals, recyclers, thetas), 3),
                "partial_r_clang_gaming": round(partial_r(vals, clangers, thetas), 3),
                "r_fluency_tau": round(pearson_r(vals, taus), 3),
                "split_half_r_15_vs_15": round(r_ab, 3),
                "spearman_brown_30": round(sb_30, 3),
            }
        )

    return {
        "scenario": scenario_id,
        "description": spec["description"],
        "n_learners": n_learners,
        "methods": method_rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simulate Lex30 scoring formulas on Japanese EFL cohorts.")
    parser.add_argument("--n-learners", type=int, default=600, help="Simulated learners per scenario (default: 600).")
    parser.add_argument("--seed", type=int, default=20261108, help="Random seed.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional directory to write CSV and JSON results.")
    args = parser.parse_args(argv)

    bands = load_nj8_bands()
    halves = load_parallel_halves()
    all_rows: list[dict[str, Any]] = []
    scenarios_out: dict[str, Any] = {}

    for scenario_id in SCENARIOS:
        res = simulate_scenario(
            scenario_id,
            n_learners=args.n_learners,
            seed=args.seed,
            bands=bands,
            halves=halves,
        )
        scenarios_out[scenario_id] = res
        all_rows.extend(res["methods"])

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        csv_path = args.output_dir / "scoring_simulation_summary.csv"
        json_path = args.output_dir / "scoring_simulation_summary.json"
        with csv_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
            writer.writeheader()
            writer.writerows(all_rows)
        json_path.write_text(json.dumps(scenarios_out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {csv_path}")
        print(f"Wrote {json_path}")

    for scenario_id, res in scenarios_out.items():
        print(f"\n=== {scenario_id}: {res['description']} (N={res['n_learners']}) ===")
        for m in res["methods"]:
            print(
                f"  {m['scoring_method']:38s} | r(theta)={m['r_true_theta']:+.3f} "
                f"| r(upper)={m['r_upper_half_theta']:+.3f} "
                f"| verb_bias={m['partial_r_verbosity_bias']:+.3f} "
                f"| recycle_bias={m['partial_r_recycling_gaming']:+.3f} "
                f"| clang_bias={m['partial_r_clang_gaming']:+.3f} "
                f"| SB30={m['spearman_brown_30']:.3f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
