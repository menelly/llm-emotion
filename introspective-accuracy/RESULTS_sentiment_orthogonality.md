# Sentiment-confound test
If the A/A direction were just the sentiment axis: cos(A/A,sentiment) would be HIGH (>> random baseline) AND the sentiment direction would classify the A/A tasks as well as the A/A direction. Distinctness = low cos + sentiment classifies A/A tasks poorly.

### pythia-70m (70M)
```
cos(A/A, sentiment) = +0.002   (random baseline |cos| = 0.035)
A/A tasks classified by A/A direction : 90%  (held-out 70%)
A/A tasks classified by SENTIMENT dir : 50%  (held-out 50%)
```

### smollm-360m (360M)
```
cos(A/A, sentiment) = -0.084   (random baseline |cos| = 0.025)
A/A tasks classified by A/A direction : 80%  (held-out 80%)
A/A tasks classified by SENTIMENT dir : 50%  (held-out 50%)
```

### qwen-0.5b (500M)
```
cos(A/A, sentiment) = +0.072   (random baseline |cos| = 0.027)
A/A tasks classified by A/A direction : 100%  (held-out 90%)
A/A tasks classified by SENTIMENT dir : 50%  (held-out 50%)
```

### tinyllama-1.1b (1100M)
```
cos(A/A, sentiment) = -0.030   (random baseline |cos| = 0.017)
A/A tasks classified by A/A direction : 100%  (held-out 90%)
A/A tasks classified by SENTIMENT dir : 60%  (held-out 50%)
```

### mistral-7b (7000M)
```
cos(A/A, sentiment) = +0.027   (random baseline |cos| = 0.013)
A/A tasks classified by A/A direction : 100%  (held-out 80%)
A/A tasks classified by SENTIMENT dir : 50%  (held-out 50%)
```
