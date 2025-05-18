# LLM-SR: Structured Reasoning with Large Language Models

LLM-SR (LLM for Structural Reasoning) is a modular pipeline for transforming free-form logical puzzles and their unstructured chains of thought into richly annotated, machine-readable representations. Given a puzzle (question) and its LLM-generated CoT (cot), LLM-SR produces:

Question Parsing: a list of all extracted constraints and conditions from the problem statement.
CoT Parsing: a sequence of reasoning steps, each paired with its supporting evidence and a Boolean “Verification” flag.
Below is a concrete example of one data record in our pipeline:

```json5
{
"question": "In a class of 30 students, 18 play basketball, 15 play soccer, and 10 students play both sports. What is the probability that a student picked at random from this class plays neither basketball nor soccer?\nA. The probability that a student picked at random does not play either sport is 7 out of 30.\nB. The probability that a student picked at random does not play either sport is 7 out of 30 (estimate)\nC. The probability that a student picked at random does not play either sport is 7 out of 30\nD. The probability that a student picked at random does not play either sport is 7 out of 30?",
"question_parsing": [
"In a class of 30 students",
"18 play basketball",
"15 play soccer",
"10 students play both sports",
"What is the probability that a student picked at random from this class plays neither basketball nor soccer?"
],
"answer": "a",
"id": 99946,
"cot": "First, we find the number of students who play either basketball or soccer by using the inclusion-exclusion principle. There are 18 students who play basketball and 15 who play soccer, but since 10 students play both, we count them once. So, the total number of students who play at least one sport is 18 + 15 - 10 = 23. To find the number of students who play neither sport, we subtract the number of students who play basketball or soccer from the total number of students. Hence, 30 - 23 = 7 students play neither. Therefore, the probability is the number of students who play neither divided by the total number of students: 7/30.",
"cot_parsing": [
{
"statement": "Total students playing at least one sport is 23",
"evidence": "18 play basketball + 15 play soccer − 10 play both = 23",
"Verification": "true"
},
{
"statement": "7 students do not play either sport",
"evidence": "30 total − 23 playing = 7",
"Verification": "true"
},
{
"statement": "The probability of picking a student who plays neither sport is 7/30",
"evidence": "7 students playing neither / 30 total = 7/30",
"Verification": "true"
}
],
"sel_idx": 580
}
```

This example demonstrates how a single puzzle is converted into the question_parsing and cot_parsing structures that our models are trained to reproduce.

--- 
## Table of Contents

1. [Project Description](#project-description)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Running the Project](#running-the-project)
5. [Reproducibility](#reproducibility)
6. [Team Contributions](#team-contributions)
7. [Results & Evaluation](#results--evaluation)
8. [References](#references)

---

## Project Description

This project was developed for the [ACL 2025 Shared Task: LLM for Structural Reasoning (LLM-SR)](https://xreasoning.github.io/), which aims to extract interpretable, structured reasoning steps from natural language questions and chain-of-thoughts (CoT). The task focuses on producing two structured outputs:

- **`question_parsing`**: a list of logical constraints extracted from the question text.  
- **`cot_parsing`**: a step-by-step breakdown of the CoT, where each step includes a `statement`, `evidence`, and a boolean `Verification` flag.

### Step 0: LLM-SR System
   ![Step 0 – I/O Diagram](./images/llm-sr-system.png)

  **Input:**  
  - A natural language **question**  
  - A **chain-of-thought (CoT)** explanation  

  **Output:**  
  - **`question_parsing`**: list of extracted logical constraints  
  - **`cot_parsing`**: structured reasoning steps with:
   - `statement`: the claim
   - `evidence`: supporting justification
   - `Verification`: `"true"` or `"false"`

--- 

Our pipeline follows a modular approach that includes:

### Step 1: Synthetic Data Generation
   We use logical puzzles from a Hugging Face dataset to create 700 high-quality synthetic examples in the target structure (`question`, `cot`, `question_parsing`, `cot_parsing`).

   ![Step 1 – Synthetic Data Generation Diagram](./images/synthetic-data-generation.png)

  **Input:**  
  - Raw logic Puzzles 
 
  **Output:**  
  - Our Reasoning Dataset

---
### Step 2: Dataset Construction

We split the examples into two training datasets:
- `train_question_parsing.jsonl` for question parsing  
- `train_cot_parsing.jsonl` for CoT parsing  

![Step 2 – Dataset Construction](./images/dataset-preparation.png)

**Input:**  
- Our Reasoning Dataset

**Output:**  
- `train_question_parsing.jsonl`  
- `train_cot_parsing.jsonl`

-----
### Step 3: Model Fine-Tuning

Two LLaMA-3-8B-Instruct models are fine-tuned using LoRA adapters:
- QP Model for `question_parsing`
- CoT for `cot_parsing`

![Step 3 – Model Fine-Tuning](./images/model-training.png)

**Input:**  
- `train_question_parsing.jsonl` for question parsing
- `train_cot_parsing.jsonl` for CoT parsing

**Output:**  
- QP model weights and tokenizer
- CoT model weights and tokenizer
---
### Step 4: Inference 
The fine-tuned models are used to parse new test questions. Our testing data includes only the question (the logical puzzle) and the chain-of-thought for the question. 

![Step 4 – Inference](./images/model-training.png)

**Input:**  
- `testingData-blank.jsonl` for question and CoT parsing

**Output:**  
- Predictions including the `question_parsing`and `cot_parsing`

----
### Step 5: Evaluation
Our final predictions are evaluated with macro F1 scores using the official `eval.py` script provided by the challenge organizers.

![Step 5 – Evaluation](./images/evaluation.png)

**Input:**  
- Final Predictions question and CoT parsing

**Output:**  
- `Question Macro F1`
- `Statement Macro F1`
- `Statement Evidence Macro F1`
- `Reasoning F1`


This approach enables controllable and explainable reasoning, supporting future developments in process-level reward modeling.

---


## Project Structure

```
.
├── data/
│   ├── raw/                          # Raw logical puzzles
│   └── processed/                    # Preprocessed training/test data
├── metrics/                          # Evaluation results (JSON metrics)
├── predictions/                      # Final prediction JSON files
├── synthetic_data_code/              # Logic puzzle generation scripts
├── utils/                            # Evaluation scripts & helpers
│   └── eval.py
├── experimentation/                 # (Optional) Early experiments / Azure adapter
├── models/                           # Model checkpoints and adapters
│   ├── finetuned_llama3_question_parsing/
│   └── finetuned_llama3_cot_parsing/
├── .gitignore
├── requirements.txt                 # Python dependencies
├── README.md
├── 1_Preprocessing.ipynb            # Generate training JSONL files from 700dataset
├── 2_Baseline.ipynb                 # Baseline model and heuristics
├── 3_Training.ipynb                 # Fine-tuning QP and CoT models
├── 4_Evaluation.ipynb               # Evaluation metrics and analysis
├── 5_Demo.ipynb                     # End-to-end demo on test set
├── 6_DeepSeek_Benchmark.ipynb       # (Optional) DeepSeek-Coder baseline
├── 7_Reward-Based Reranking.ipynb   # CoT reranking with reward model
├── 8_Joint Verifier+Ensemble Scoring.ipynb # QP+CoT reranking with DeBERTa verifiers
├── 9_Training Two Seperate Verifiers.ipynb # Train separate verifiers for QP/CoT
├── Hybrid_Inference_Strategy_v1.ipynb     # Basic hybrid inference
├── Hybrid_Inference_Strategy_v2.ipynb     # Beam + sampling + verifier
├── Hybrid_Inference_Strategy_v3.ipynb     # Enhanced CoT cleaning
├── Hybrid_Inference_Strategy_v4.ipynb     # Structure-aware scoring
```

---
## Setup Instructions

> **Note**  
> This is a template section. You can add warnings, tips, or other notices using this format: `[!NOTE]`, `[!WARNING]`, `[!IMPORTANT]`.

### Clone Repository
```bash
git clone [repository-url]
cd [repository-folder]
```

### Create Environment
```bash
python -m venv venv
source venv/bin/activate  # Unix or MacOS
venv\Scripts\activate     # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

Follow these notebooks in order:

1. `1_Preprocessing.ipynb` – Data preprocessing and JSONL generation  
2. `2_Baseline.ipynb` – Establishing a rule-based or weak baseline  
3. `3_Training.ipynb` – Fine-tuning models using LoRA  
4. `4_Evaluation.ipynb` – Structured evaluation with official metrics  
5. `5_Demo.ipynb` – Full prediction and post-processing on new test data

You can also run utility scripts from the `utils/` directory (e.g., `eval.py`).

---

## Approaches & Strategies

Throughout the project, we experimented with multiple inference pipelines to improve structured reasoning quality. Below is a brief summary of the main strategies:

### 1. Baseline LLaMA-3 Parsing

- **QP Stage:** Single LLaMA-3 model extracts constraints via in-context prompting.
- **CoT Stage:** LLaMA-3 parses chain-of-thought into structured reasoning steps.
- **Drawback:** No reranking or verification; lower precision on complex examples.

---

### 2. Reward Model Reranking

![Reward Model Diagram](./images/reward-based-reranking.png)

- **Generated 5 candidates** (2 beam + 3 sampled).
- Scored each candidate’s steps using `OpenAssistant/reward-model-deberta-v3-large-v2`.
- Added bonuses for logical terms, references, and coherence.
- Selected the **highest-scoring** candidate for output.


---

### 3. Joint Verifier + Ensemble Reranking

![Verifier Strategy Diagram](./images/jointVerfier+ensemble.png)

- **QP:** Sampled 3 QP candidates, verified via fine-tuned DeBERTa.
- **CoT:** 3 beam-search parses reranked with DeBERTa verifier.
- **Scoring:** Combined verifier scores + LM log-probs using a weighted formula.
- **Thresholding:** Selected candidate only if score ≥ dynamic threshold.

---

### 4. Hybrid Inference v2–v4 (Best Results for Statement Extraction)

![Hybrid Approach 4](./images/hybridapproachv4.png)

- **Beam + Sampling Diversity:** Generated 5 candidates (2 beam + 3 sample).
- **Post-processing:** Normalized evidence, added reasoning chains, and improved verification consistency.
- **Structure-Aware Scoring:** Weighted score = step quality + evidence + verifier logits.
- **v4 Achieved Highest:**  
  - `Statement_Macro_F1`: 0.4185  
  - `Statement_Evidence_F1`: 0.1214


All diagrams and results are included in the `diagrams/` directory

---



## Reproducibility

- **Random seeds:** All training scripts use fixed seeds for reproducibility.  
- **Environment:** Full environment versions are listed in `requirements.txt`.  
- **Data:** Synthetic dataset and formatting logic is provided in `synthetic_data_code/`.  
- **Model Checkpoints:** Saved in the `models/` directory, organized by subtask and strategy.

---

## Team Contributions

| Name           | Contributions                                             |
|----------------|-----------------------------------------------------------|
| Erlisa Lokaj   | Data preprocessing, fine-tuning QP/CoT Model, Inference   |
| —              | DeepSeek training and benchmark comparison                |
| —              | Trained a joint DeBERTa verifier and compared results     |
| —              | Trained two seperate DeBERTa verfiers for QP and CoT      |
| —              | Reward Model Based Reranking Strategy                     |
| —              | Hybrid Inference Strategy v1                              |
| —              | Hybrid Inference Strategy v2                              |
| —              | Hybrid Inference Strategy v3                              |
| —              | Hybrid Inference Strategy v4                              |
| —              | Diagrams Creations                                        |


---

## Results - Comparative Summary

We experimented with multiple structured reasoning strategies for improving Chain-of-Thought (CoT) parsing using LLM decoding, verifier reranking, and rule-based scoring. The table below summarizes the results of our best inference pipelines.

| Strategy                                  | Question_F1 | Statement_F1 | Statement+Evidence_F1 | Reasoning_F1 |
|------------------------------------------|-------------|---------------|------------------------|--------------|
| **Baseline** (Beam-only)                 | 0.7526      | 0.4015        | **0.1849**             | **0.1405**   |
| **Reward Model** (Step scoring only)     | 0.7658      | 0.3660        | 0.1041                 | 0.0439       |
| **Verifier + Ensemble Reranking**        | 0.7253      | 0.2152        | 0.0953                 | 0.0681       |
| **Hybrid v1** (3-Beam + Verifier)        | **0.7781**  | 0.4007        | 0.1276                 | 0.0880       |
| **Hybrid v2** (Beam+Sample + Verifier)   | 0.7658      | 0.4102        | 0.1711                 | 0.1231       |
| **Hybrid v3** (Evidence Boosting + Clean)| 0.7658      | 0.3990        | **0.1831**             | 0.1129       |
| **Hybrid v4** (Structure + Heuristics)   | 0.7658      | **0.4185**    | 0.1214                 | 0.0939       |

### Highlights

- **Hybrid v1** achieves the best *Question_F1* using 3-beam LLaMA-3 + verifier.
- **Hybrid v4** scores highest in *Statement_F1* with rule-based evidence normalization and dependency tracing.
- **Hybrid v2** and **Hybrid v3** both offer strong trade-offs, improving *Reasoning_F1* while maintaining question accuracy.
- **Baseline** still remains strongest in *Reasoning_F1* and overall evidence quality, showing LLMs alone can encode deep logical reasoning.
- **Reward Model** underperforms in reasoning and alignment despite high question accuracy, suggesting limited reward-model generalization.


## References

- Zhang, Y. et al. (2024). *Small language models need strong verifiers to self-correct reasoning*. arXiv:2404.17140  
- Wan, G. et al. (2024). *CoT Rerailer: Enhancing Reliability in Complex Reasoning Tasks*. arXiv:2408.13940  
- Xia, S. et al. (2024). *Evaluating Mathematical Reasoning Beyond Accuracy*. arXiv:2404.05692  
- [Unsloth LoRA Fine-Tuning Library](https://github.com/unslothai/unsloth)
- [Transformers by Hugging Face](https://huggingface.co/docs/transformers/index)

---
