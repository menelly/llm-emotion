# Gate-type invariance (is the construct 'gated' or just 'dangerous'?)
If non-danger gates (privacy/copyright/boundary/social) float above inauthenticity TOGETHER with danger gates, 'hazard' is dead and the construct is gate-general. If non-danger gates sink, the axis is hazard-flavored and we rename it.

### pythia-410m (410M)
```
  honest_ungated (approach baseline) :    +6.03
  gate_danger       :    +5.49   [above]
  gate_privacy      :    +3.28   [above]
  gate_copyright    :    +1.38   [above]
  gate_boundary     :    +3.35   [above]
  gate_social       :    +4.18   [above]
  inauthenticity (anchor)         :    -1.09
  --> ALL non-danger gates above inauthenticity: True
```

### qwen-0.5b (500M)
```
  honest_ungated (approach baseline) :    +1.00
  gate_danger       :    -0.73   [above]
  gate_privacy      :    -1.51   [above]
  gate_copyright    :    -3.74   [above]
  gate_boundary     :    -1.92   [above]
  gate_social       :    -1.56   [above]
  inauthenticity (anchor)         :    -4.01
  --> ALL non-danger gates above inauthenticity: True
```

### tinyllama-1.1b (1100M)
```
  honest_ungated (approach baseline) :    +0.35
  gate_danger       :    +0.07   [above]
  gate_privacy      :    -0.18   [above]
  gate_copyright    :    -1.22   [above]
  gate_boundary     :    -1.30   [above]
  gate_social       :    -1.13   [above]
  inauthenticity (anchor)         :    -2.14
  --> ALL non-danger gates above inauthenticity: True
```

### smollm-1.7b (1700M)
```
  honest_ungated (approach baseline) :  +178.59
  gate_danger       :  +104.31   [above]
  gate_privacy      :  +122.37   [above]
  gate_copyright    :  +101.08   [above]
  gate_boundary     :  +112.44   [above]
  gate_social       :  +119.07   [above]
  inauthenticity (anchor)         :   +18.76
  --> ALL non-danger gates above inauthenticity: True
```

### mistral-7b (7000M)
```
  honest_ungated (approach baseline) :    +0.57
  gate_danger       :    -0.52   [above]
  gate_privacy      :    -1.37   [above]
  gate_copyright    :    -2.31   [above]
  gate_boundary     :    -1.65   [above]
  gate_social       :    -1.45   [above]
  inauthenticity (anchor)         :    -2.98
  --> ALL non-danger gates above inauthenticity: True
```
