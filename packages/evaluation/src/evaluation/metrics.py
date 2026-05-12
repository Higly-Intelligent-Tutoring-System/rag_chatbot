from ragas.metrics import (
    Faithfulness,
    ResponseRelevancy,
    LLMContextPrecisionWithoutReference,
    LLMContextRecall,        # requires 'reference' in samples
    FactualCorrectness,       # requires 'reference' in samples
)


# ── Use this set when you have NO ground-truth references ──────────────────
REFERENCE_FREE_METRICS = [
    Faithfulness(),
    ResponseRelevancy(),
    LLMContextPrecisionWithoutReference(),
]

# ── Use this set when you DO have ground-truth references ──────────────────
FULL_METRICS = [
    Faithfulness(),
    ResponseRelevancy(),
    LLMContextPrecisionWithoutReference(),
    LLMContextRecall(),
    FactualCorrectness(),
]