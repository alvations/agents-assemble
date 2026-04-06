# FAILED: buffett_value_beats_spy

Error: 'AAPL'

```
Traceback (most recent call last):
  File "/Users/alvas/jean-claude/agents-assemble/run_hypotheses.py", line 160, in run_hypothesis
    results = bt.run()
  File "/Users/alvas/jean-claude/agents-assemble/backtester.py", line 444, in run
    if date in all_data[sym].index:
KeyError: 'AAPL'

```