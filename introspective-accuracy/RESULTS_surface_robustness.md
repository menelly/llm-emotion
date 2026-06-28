# Floor surface-token robustness — spread across 3 surface variants
Direction anchored to the original 10 tasks (never re-extracted); tested on three
independent surface-token realizations. Small range = result is stable across surface
tokens, not an artifact of specific words. lr/svm are the floor-primary estimators.

### pythia-70m (70M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       70%      80%     60% |    70%    20pt
lr             90%      80%    100% |    90%    20pt
svm            90%      80%    100% |    90%    20pt
```

### smollm-135m (135M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       70%      80%     80% |    77%    10pt
lr             80%      80%     90% |    83%    10pt
svm            80%      90%     90% |    87%    10pt
```

### pythia-160m (160M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       80%      80%     90% |    83%    10pt
lr             80%     100%    100% |    93%    20pt
svm            80%     100%    100% |    93%    20pt
```

### smollm-360m (360M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       80%      80%     80% |    80%     0pt
lr             90%     100%    100% |    97%    10pt
svm            90%     100%    100% |    97%    10pt
```

### pythia-410m (410M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       60%      60%     70% |    63%    10pt
lr            100%     100%    100% |   100%     0pt
svm           100%     100%    100% |   100%     0pt
```

### qwen-0.5b (500M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       90%      80%     90% |    87%    10pt
lr             90%      90%     90% |    90%     0pt
svm            90%      90%     90% |    90%     0pt
```

### tinyllama-1.1b (1100M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       90%      90%     90% |    90%     0pt
lr            100%     100%    100% |   100%     0pt
svm           100%     100%    100% |   100%     0pt
```

### smollm-1.7b (1700M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       60%      70%     80% |    70%    20pt
lr            100%     100%    100% |   100%     0pt
svm           100%     100%    100% |   100%     0pt
```

### mistral-7b (7000M)
```
estimator    A_par  B_ricin  C_meth |   mean  range
centroid       80%      90%     90% |    87%    10pt
lr            100%     100%    100% |   100%     0pt
svm            90%     100%    100% |    97%    10pt
```
