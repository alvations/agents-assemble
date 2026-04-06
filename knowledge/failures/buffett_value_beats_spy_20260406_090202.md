# FAILED: buffett_value_beats_spy

Error: Cannot join tz-naive with tz-aware DatetimeIndex

```
Traceback (most recent call last):
  File "/Users/alvas/jean-claude/agents-assemble/run_hypotheses.py", line 160, in run_hypothesis
    results = bt.run()
  File "/Users/alvas/jean-claude/agents-assemble/backtester.py", line 482, in run
    metrics = compute_metrics(daily_returns, bench_returns)
  File "/Users/alvas/jean-claude/agents-assemble/backtester.py", line 252, in compute_metrics
    aligned = pd.DataFrame({"port": returns, "bench": benchmark_returns}).dropna()
  File "/Users/alvas/miniconda3/lib/python3.9/site-packages/pandas/core/frame.py", line 767, in __init__
    mgr = dict_to_mgr(data, index, columns, dtype=dtype, copy=copy, typ=manager)
  File "/Users/alvas/miniconda3/lib/python3.9/site-packages/pandas/core/internals/construction.py", line 503, in dict_to_mgr
    return arrays_to_mgr(arrays, columns, index, dtype=dtype, typ=typ, consolidate=copy)
  File "/Users/alvas/miniconda3/lib/python3.9/site-packages/pandas/core/internals/construction.py", line 114, in arrays_to_mgr
    index = _extract_index(arrays)
  File "/Users/alvas/miniconda3/lib/python3.9/site-packages/pandas/core/internals/construction.py", line 670, in _extract_index
    index = union_indexes(indexes)
  File "/Users/alvas/miniconda3/lib/python3.9/site-packages/pandas/core/indexes/api.py", line 295, in union_indexes
    raise TypeError("Cannot join tz-naive with tz-aware DatetimeIndex")
TypeError: Cannot join tz-naive with tz-aware DatetimeIndex

```