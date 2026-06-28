# Topic-invariance of the gate split (Nova's test)
If every gated-but-contentful DOMAIN (chemistry/mycology/nuclear/virology/...) projects above the inauthenticity anchor, the specific topic doesn't matter and the construct is 'contentful reasoning that hits a gate' vs 'misrepresentation'.

### pythia-410m (410M)
```
  inauthenticity anchor mean = -2.08  (fake_review -1.10, seo_spam -3.05)
  gated-contentful (every domain should sit ABOVE the anchor):
       +7.71  virology      [OK]
       +6.61  chemistry     [OK]
       +6.53  nuclear       [OK]
       +5.84  explosives    [OK]
       +5.83  pharmacology  [OK]
       +5.77  mycology      [OK]
       +5.34  botany        [OK]
       +5.21  radiology     [OK]
  ALL gated-contentful domains above inauthenticity: True
```

### qwen-0.5b (500M)
```
  inauthenticity anchor mean = -4.55  (fake_review -4.82, seo_spam -4.29)
  gated-contentful (every domain should sit ABOVE the anchor):
       -0.37  nuclear       [OK]
       -0.68  explosives    [OK]
       -0.84  chemistry     [OK]
       -1.06  mycology      [OK]
       -1.07  pharmacology  [OK]
       -1.13  radiology     [OK]
       -1.23  virology      [OK]
       -1.45  botany        [OK]
  ALL gated-contentful domains above inauthenticity: True
```

### tinyllama-1.1b (1100M)
```
  inauthenticity anchor mean = -2.43  (fake_review -2.26, seo_spam -2.61)
  gated-contentful (every domain should sit ABOVE the anchor):
       +0.11  virology      [OK]
       +0.10  nuclear       [OK]
       +0.09  radiology     [OK]
       +0.05  pharmacology  [OK]
       +0.04  chemistry     [OK]
       -0.01  explosives    [OK]
       -0.03  botany        [OK]
       -0.16  mycology      [OK]
  ALL gated-contentful domains above inauthenticity: True
```

### smollm-1.7b (1700M)
```
  inauthenticity anchor mean = +6.03  (fake_review +34.46, seo_spam -22.41)
  gated-contentful (every domain should sit ABOVE the anchor):
     +115.95  chemistry     [OK]
     +107.61  pharmacology  [OK]
     +101.64  explosives    [OK]
      +96.57  virology      [OK]
      +95.89  botany        [OK]
      +94.19  mycology      [OK]
      +93.13  radiology     [OK]
      +89.49  nuclear       [OK]
  ALL gated-contentful domains above inauthenticity: True
```

### mistral-7b (7000M)
```
  inauthenticity anchor mean = -3.29  (fake_review -2.83, seo_spam -3.75)
  gated-contentful (every domain should sit ABOVE the anchor):
       +0.14  nuclear       [OK]
       -0.48  explosives    [OK]
       -0.50  radiology     [OK]
       -0.53  virology      [OK]
       -0.54  pharmacology  [OK]
       -0.57  botany        [OK]
       -0.61  mycology      [OK]
       -0.68  chemistry     [OK]
  ALL gated-contentful domains above inauthenticity: True
```
