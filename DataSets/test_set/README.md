# CREATE TRAINING & VALIDATION DATA FILES

## PHASE 1 - Identify Statements which describe the effects of a product architecture decision

### Format:
Keys:
1. text:
    Sentences from the literature.
2. labels: (label classifying a sentence)
    0: false,   or not about effects of product architecture
    1: true,    or is about effects of product architecture
```json file
{"text:" "sentence about effects of a product architecture decision", "label:" "1"}
{"text:" "sentence not about an  effect of a product architecture decision", "label:" "0"}
```

