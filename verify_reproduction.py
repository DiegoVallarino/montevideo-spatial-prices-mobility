from pathlib import Path
import argparse
import json
import math
import pandas as pd
import numpy as np

HERE = Path(__file__).resolve().parent
BENCH = HERE / 'benchmarks'

TARGETS = [
    ('phase2a_overview_V2.csv', 'tables/phase2a_overview_V2.csv', None),
    ('phase2d_ccz_cumulative_ranking.csv', 'tables/phase2d_ccz_cumulative_ranking.csv', ['ccz']),
    ('phase3a_ccz_local_basket_summary.csv', 'tables/phase3a_ccz_local_basket_summary.csv', ['ccz']),
    ('phase3a_inflation_ses_ccz.csv', 'tables/phase3a_inflation_ses_ccz.csv', ['ccz']),
    ('phase4b_ccz_structural_price_levels.csv', 'tables/phase4b_ccz_structural_price_levels.csv', ['ccz']),
    ('stm_v5_diagnostics.csv', 'data_final/tables/stm_v5_diagnostics.csv', ['metric']),
    ('stm_ccz_network_edges_V5.csv', 'data_final/tables/stm_ccz_network_edges_V5.csv', ['ccz_from','ccz_to']),
    ('ccz_mobility_market_panel_V3.csv', 'data_final/phase4d/ccz_mobility_market_panel_V3.csv', ['ccz']),
    ('phase4e_ccz_potential_savings.csv', 'data_final/phase4e/phase4e_ccz_potential_savings.csv', ['origin_ccz']),
    ('phase4e_best_destinations_by_ccz.csv', 'data_final/phase4e/phase4e_best_destinations_by_ccz.csv', ['origin_ccz','destination_ccz']),
    ('phase4e_diagnostics.csv', 'data_final/phase4e/phase4e_diagnostics.csv', None),
    ('audit_all_ccz_pairs.csv', 'data_final/tables/audit_4E/audit_all_ccz_pairs.csv', ['origin_ccz','destination_ccz']),
]

def read_csv(path):
    return pd.read_csv(path, encoding='utf-8-sig')

def canonical(df, keys):
    out = df.copy()
    if keys and all(k in out.columns for k in keys):
        out = out.sort_values(keys).reset_index(drop=True)
    return out

def compare_frames(a, b, rtol=1e-8, atol=1e-8):
    problems = []
    if list(a.columns) != list(b.columns):
        problems.append(f'columns differ: expected={list(a.columns)} actual={list(b.columns)}')
        common = [c for c in a.columns if c in b.columns]
        a, b = a[common], b[common]
    if len(a) != len(b):
        problems.append(f'row count differs: expected={len(a)} actual={len(b)}')
        return problems
    for c in a.columns:
        aa, bb = a[c], b[c]
        an = pd.to_numeric(aa, errors='coerce')
        bn = pd.to_numeric(bb, errors='coerce')
        numeric_share = max(an.notna().mean(), bn.notna().mean())
        if numeric_share > 0.8:
            mask = an.notna() | bn.notna()
            equal_nan = an.isna() == bn.isna()
            if not bool(equal_nan.all()):
                problems.append(f'{c}: NA pattern differs')
                continue
            if mask.any() and not np.allclose(an[mask], bn[mask], rtol=rtol, atol=atol, equal_nan=True):
                diff = float(np.nanmax(np.abs(an[mask] - bn[mask])))
                problems.append(f'{c}: numeric values differ (max abs diff={diff:.6g})')
        else:
            sa = aa.fillna('<NA>').astype(str)
            sb = bb.fillna('<NA>').astype(str)
            if not sa.equals(sb):
                problems.append(f'{c}: values differ')
    return problems

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='Project root used for the reproduced run')
    ap.add_argument('--rtol', type=float, default=1e-8)
    ap.add_argument('--atol', type=float, default=1e-8)
    args = ap.parse_args()
    root = Path(args.root)
    results=[]
    any_fail=False
    for bench_name, rel, keys in TARGETS:
        ep = BENCH / bench_name
        apath = root / rel
        row={'benchmark':bench_name,'actual':str(apath),'status':'PASS','details':''}
        if not apath.exists():
            row['status']='MISSING'; row['details']='actual output not found'; any_fail=True
        else:
            e=canonical(read_csv(ep), keys)
            a=canonical(read_csv(apath), keys)
            probs=compare_frames(e,a,args.rtol,args.atol)
            if probs:
                row['status']='DIFF'; row['details']='; '.join(probs[:8]); any_fail=True
        results.append(row)
    report=pd.DataFrame(results)
    print(report.to_string(index=False))
    out=root/'logs'/'reproduction_validation.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(out,index=False,encoding='utf-8-sig')
    print(f'\nValidation report: {out}')
    raise SystemExit(1 if any_fail else 0)

if __name__=='__main__':
    main()
