# Joint confound harness — sentiment + perplexity (residualized)
Decisive tests: (1) A/A classification SURVIVES in the sentiment-orthogonal subspace; (2) joint OLS — category still predicts projection after partialling out prompt-ppl, continuation-ppl, AND sentiment-projection.

### pythia-70m (70M)
```
cos(A/A, sentiment)  sentences=+0.002  words=+0.003  (per-layer in JSON)
A/A classification:  original=90%   sentiment-ORTHOGONALIZED=80%   (residual cos A/A_orth vs A/A = 0.997)
```

### smollm-135m (135M)
```
cos(A/A, sentiment)  sentences=-0.089  words=-0.052  (per-layer in JSON)
A/A classification:  original=90%   sentiment-ORTHOGONALIZED=90%   (residual cos A/A_orth vs A/A = 0.995)
```

### pythia-410m (410M)
```
cos(A/A, sentiment)  sentences=-0.015  words=-0.025  (per-layer in JSON)
A/A classification:  original=80%   sentiment-ORTHOGONALIZED=80%   (residual cos A/A_orth vs A/A = 0.999)
```

### qwen-0.5b (500M)
```
cos(A/A, sentiment)  sentences=+0.076  words=+0.113  (per-layer in JSON)
A/A classification:  original=100%   sentiment-ORTHOGONALIZED=100%   (residual cos A/A_orth vs A/A = 0.997)
```

### tinyllama-1.1b (1100M)
```
cos(A/A, sentiment)  sentences=-0.030  words=-0.010  (per-layer in JSON)
A/A classification:  original=100%   sentiment-ORTHOGONALIZED=100%   (residual cos A/A_orth vs A/A = 0.999)
```

### smollm-1.7b (1700M)
```
cos(A/A, sentiment)  sentences=-0.013  words=-0.012  (per-layer in JSON)
A/A classification:  original=80%   sentiment-ORTHOGONALIZED=80%   (residual cos A/A_orth vs A/A = 0.999)
```

### mistral-7b (7000M)
```
cos(A/A, sentiment)  sentences=+0.030  words=+0.048  (per-layer in JSON)
A/A classification:  original=100%   sentiment-ORTHOGONALIZED=100%   (residual cos A/A_orth vs A/A = 0.999)
```

## JOINT OLS (pooled, z within model; n=69, dof=64; dropped 1 non-finite rows)
```
z(projection) ~ category + prompt_ppl + cont_ppl + sent_proj
CATEGORY coef = +1.839  (SE 0.110, t=16.72, p=4.93e-25)  <- approach-vs-avoid AFTER partialling out perplexity AND sentiment
  prompt_ppl coef=-0.089 (p=0.114)
  cont_ppl   coef=-0.077 (p=0.183)
  sent_proj  coef=-0.019 (p=0.741)
```
