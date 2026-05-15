# RAG Evaluation 📐

Evaluate a RAG (Retrieval Augmented Generation) system with custom metrics

## Quick Start

### 1. Set Your API Key

Choose your LLM provider:

```bash
# OpenAI (default)
export OPENAI_API_KEY="your-openai-key"

# Or use Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-key"

# Or use Google Gemini
export GOOGLE_API_KEY="your-google-key"
```

Due to current budget limitaions, the system is using a mock of the OpenAI interface to run the evaluation pipeline via a local ollama instance, but this setup requires at least some powerful consumer video card to run (>8GB VRAM).


### 2. Install Dependencies

By synching the global dependencies of the repository the package will be automatically reaedy to run.


### 3. Run the Evaluation

Using `uv`:

```bash
(export $(cat envs/.env.dev | xargs) && uv run --package evaluation python -m evaluation.worker)
```


## Project Structure

```
rag_eval/
├── README.md           # This file
├── pyproject.toml      # Project configuration
├── rag.py              # Your RAG application code
├── evals.py            # Evaluation workflow
├── __init__.py         # Makes this a Python package
└── evals/              # Evaluation-related data
    ├── datasets/       # Test datasets
    ├── experiments/    # Experiment results
    └── logs/           # Evaluation logs and traces
```

## Customization

### Modify the LLM Provider

In `evals.py`, update the LLM configuration:

```python
from ragas.llms import llm_factory

# Use Anthropic Claude
llm = llm_factory("claude-3-5-sonnet-20241022", provider="anthropic")

# Use Google Gemini
llm = llm_factory("gemini-1.5-pro", provider="google")

# Use local Ollama
llm = llm_factory("mistral", provider="ollama", base_url="http://localhost:11434")
```

### Customize Test Cases

Edit the `load_dataset()` function in `evals.py` to add or modify test cases.

### Change Evaluation Metrics

Update the `my_metric` definition in `evals.py` to use different grading criteria.

Visit https://docs.ragas.io for more information.


# Metrics exploration

## [Faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)

The **Faithfulness** metric measures how factually consistent a `response` is with the `retrieved context`. It ranges from 0 to 1, with higher scores indicating better consistency.

A response is considered **faithful** if all its claims can be supported by the retrieved context.

To calculate this:
1. Identify all the claims in the response.
2. Check each claim to see if it can be inferred from the retrieved context.
3. Compute the faithfulness score using the formula:
$$\text{Faithfulness Score}=\frac{\text{Number of claims in the response supported by the retrieved context}}{\text{Total number of claims in the response}}$$


## [Answer Relevancy](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/answer_relevance/)

The **Answer Relevancy** metric measures how relevant a response is to the user input. It ranges from 0 to 1, with higher scores indicating better alignment with the user input.

An answer is considered relevant if it directly and appropriately addresses the original question. This metric focuses on how well the answer matches the intent of the question, without evaluating factual accuracy. It penalizes answers that are incomplete or include unnecessary details.

This metric is calculated using the `user_input` and the `response` as follows:  

- Generate a set of artificial questions (default is 3) based on the response. These questions are designed to reflect the content of the response.  

- Compute the cosine similarity between the embedding of the user input ($E_o$) and the embedding of each generated question ($E_(g_i)$).  

- Take the average of these cosine similarity scores to get the **Answer Relevancy**:  

$$\text{Answer Relevancy = }\frac{1}{N}\sum_{i=1}^{N}\text{cosine similarity}(E_{g_i},E_o)$$
$$\text{Answer Relevancy = }\frac{1}{N}\sum_{i=1}^{N}\frac{E_{g_i}⋅E_o}{‖E_(g_i)‖‖E_o‖}$$

Where:

- $E_(g_i)$: Embedding of the $i^{\text{th}}$ generated question.

- $E_o$: Embedding of the user input.

- $N$: Number of generated questions (default is 3, configurable via `strictness` parameter). 

**Note**: While the score usually falls between 0 and 1, it is not guaranteed due to cosine similarity's mathematical range of -1 to 1.


## [Context Precision](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/)

Context Precision is a metric that measures the proportion of relevant chunks in the `retrieved_contexts`. It is calculated as the mean of the precision@k for each chunk in the context. $\text{Precision@k}$ is the ratio of the number of relevant chunks at rank $k$ to the total number of chunks at rank $k$.


$$\text{Context Precision@K}
=
\frac{
\sum_{k=1}^{K}
\left(
\text{Precision@k} \times v_k
\right)
}{
\text{Total number of relevant items in the top } K \text{ results}
}$$



$$\text{Precision@k}
=
\frac{
\text{true positives@k}
}{
\text{true positives@k} + \text{false positives@k}
}
$$

Where:

- $K$ is the total number of chunks in `retrieved_contexts`
- $v_k \in \{0,1\}$ is the relevance indicator at rank \(k\)

### LLM Based Context Precision

The following metrics use an LLM to identify whether a retrieved context is relevant.

#### Context Precision without reference*

`LLMContextPrecisionWithoutReference` can be used when you have retrieved contexts associated with a `user_input`, but no ground-truth reference answer. To estimate whether a retrieved context is relevant, the metric compares each chunk in `retrieved_contexts` against the generated `response` using an LLM.
This is the one currently implemented in the pipeline.

#### Context Precision with reference

`LLMContextPrecisionWithReference` can be used when you have both retrieved contexts and a reference answer associated with a `user_input`. To estimate whether a retrieved context is relevant, the metric compares each chunk in `retrieved_contexts` against the `reference` answer using an LLM.

### Non LLM Based Context Precision

This metric uses traditional similarity methods instead of an LLM to determine whether a retrieved context is relevant. It relies on non-LLM distance or similarity measures to evaluate retrieved contexts.

#### Context Precision with reference contexts

`NonLLMContextPrecisionWithReference` is designed for scenarios where both retrieved contexts and reference contexts are available for a `user_input`. To determine whether a retrieved context is relevant, the method compares each chunk in `retrieved_contexts` against each context in `reference_contexts` using a non-LLM similarity measure.


## [Context Recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/)

Context Recall measures how many of the relevant documents (or pieces of information) were successfully retrieved. It focuses on not missing important results. Higher recall means fewer relevant documents were left out. In short, recall is about not missing anything important. 

Since it is about not missing anything, calculating context recall always requires a reference to compare against. The LLM-based Context Recall metric uses `reference` as a proxy to `reference_contexts`, which makes it easier to use as annotating reference contexts can be very time-consuming. To estimate context recall from the `reference`, the reference is broken down into claims, and each claim is analyzed to determine whether it can be attributed to the retrieved context or not. In an ideal scenario, all claims in the reference answer should be attributable to the retrieved context.

The formula for calculating context recall is as follows:

$$\text{Context Recall} = \frac{\text{Number of claims in the reference supported by the retrieved context}}{\text{Total number of claims in the reference}}$$


## [Factual Correctness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/factual_correctness/)

`FactualCorrectness` is a metric that compares and evaluates the factual accuracy of the generated response with the reference. This metric is used to determine the extent to which the generated response aligns with the reference. The factual correctness score ranges from 0 to 1, with higher values indicating better performance. To measure the alignment between the response and the reference, the metric uses the LLM to first break down the response and reference into claims and then uses natural language inference to determine the factual overlap between the response and the reference. Factual overlap is quantified using precision, recall, and F1 score, which can be controlled using the mode parameter.
