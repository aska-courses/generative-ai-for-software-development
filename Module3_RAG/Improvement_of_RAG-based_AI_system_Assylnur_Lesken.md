# Improvement of RAG-based AI system – InsureLLM

This report focuses on **evaluation and improvement** of the RAG subsystem for the InsureLLM project.  
The overall system architecture, data description, and UI details are documented in [Module3_RAG/README.md](https://github.com/aska-courses/generative-ai-for-software-development/blob/main/Module3_RAG/README.md).

To improve the system, I focused on two techniques that are repeatedly mentioned in the course materials and are relatively cheap to implement:  
1) **better chunking** (markdown-aware, overlapping chunks) and  
2) **cross-encoder reranking** on top of FAISS retrieval.  


Both methods target retrieval quality without changing the core LLM or the dataset.


---

## 1. Evaluation setup

### 1.1 Evaluation dataset

I prepared an evaluation set of **31 “hard” questions** about InsureLLM, stored in `eval_queries.jsonl`.  
Characteristics:

- Questions span **4 doc types**: `company`, `contracts`, `employees`, `products`.
- Many are **cross-document** and **indirect**:
  - compare multiple contracts (Homellm / Carllm / Rellm),
  - join product docs with contracts,
  - use HR records plus company overview (e.g., CEO background, team growth),
  - detect naming inconsistencies (Markellm vs Marketllm, product lists, etc.).
- For each question I store:
  - `expected_doc_type`
  - `expected_source_basenames` – list of filenames that contain the ground-truth information.

This set is intentionally difficult: the system must **retrieve the right doc type and the right file**, sometimes among several plausible candidates.

### 1.2 Automation scripts

Two main scripts drive evaluation:

- **Index builder** (not detailed here; see code):
  - Baseline index: simple character splitting.
    ```bash
    python build_index.py --mode baseline
    ```
  - Overlap index: markdown-aware, overlapping chunks.

    ```bash
    python build_index.py --mode overlap  
    ```

- **Evaluation script** `eval_retrieval.py`:
  - Loads FAISS index + OpenAI embeddings.
  - Reads `eval_queries.jsonl`.
  - Optional cross-encoder reranker (`--rerank` flag).
  - Writes metrics to stdout and appends a section into  
    `Improvement_of_RAG-based_AI_system_Assylnur_Lesken.md`.

---

## 2. Metrics

I chose two retrieval-focused metrics that are directly tied to user experience in this RAG setup.

### 2.1 Hit@k (doc_type)

> **Definition:** fraction of questions where *any* of the top-k retrieved chunks has the **correct `doc_type`** (`company`, `contracts`, `employees`, `products`).

Intuition:

- Measures whether the system is at least searching in the **right area of the knowledge base**.
- Example:  
  - Question asks about a contract fee → expected `contracts`.  
  - If top-3 results are `[contracts, contracts, employees]` → Hit@3 = 1 for this query.  
  - If all top-3 are `employees` → Hit@3 = 0.

In this project I use **Hit@3**, because in the real system I pass a small top-k context to the LLM.

### 2.2 Avg RankScore@k (file-level, primary metric)

> **Definition:** measures how high in the top-k list the **correct file(s)** appear, averaged over all questions.

For each query:

1. Look at the top-k retrieved chunks.
2. Compare their `source` filenames (basename) with `expected_source_basenames` (list).
3. If any match:
   - let `r` be the **best (lowest) rank** among matches (0-based),
   - compute  
     \[
     \text{rank\_score} = \frac{k - r}{k}
     \]
     - correct file at rank 0 → 1.0  
     - rank 1 → 2/3  
     - rank 2 → 1/3 (for k = 3)
4. If no correct file in top-k → rank_score = 0.0.

Then I average this over all queries → **Avg RankScore@3**.

Intuition:

- Direct proxy for “does the right contract/employee/product doc show up **near the top** where the LLM will actually see it?”
- More informative than just Hit@k: it distinguishes **rank 1 vs rank 3**.

For the assignment, **Avg RankScore@3** is my **primary metric**, and **Hit@3** is secondary.

---

<h2 style="color:red">3. Results</h2>

### Evaluation Run – 2025-12-21 16:45 (baseline_k3)
`!python eval_retrieval.py --db-dir vector_db --label baseline_k3 --k 3`


**Vector DB directory:** `vector_db`  
**Eval file:** `eval_queries.jsonl`  
**Top-K (k):** `3`  
**Rerank:** `False`  

**Hit@3 (doc_type):** `0.633`  
**Avg RankScore@3 (file-level):** `0.484`  


---

### Evaluation Run – 2025-12-21 16:45 (overlap_k3)
`python eval_retrieval.py --db-dir vector_db_overlap --label overlap_k3 --k 3`

**Vector DB directory:** `vector_db_overlap`  
**Eval file:** `eval_queries.jsonl`  
**Top-K (k):** `3`  
**Rerank:** `False`  

**Hit@3 (doc_type):** `0.742`  
**Avg RankScore@3 (file-level):** `0.581`  


---

### Evaluation Run – 2025-12-21 16:46 (overlap_rerank_k3)
`python eval_retrieval.py --db-dir vector_db_overlap --label overlap_rerank_k3 --k 3 --rerank --pre-k 30`

**Vector DB directory:** `vector_db_overlap`  
**Eval file:** `eval_queries.jsonl`  
**Top-K (k):** `3`  
**Rerank:** `True`  
**Top-pre-K (before rerank):** `30`  

**Hit@3 (doc_type):** `0.936`  
**Avg RankScore@3 (file-level):** `0.817`  

---

## 4. Analysis

### 4.1 Effect of overlap chunking

Comparing `baseline_k3` vs `overlap_k3`:

- **Hit@3 (doc_type):** 0.633 → 0.742 (**≈+11%**)
- **Avg RankScore@3:** 0.484 → 0.581 (**≈+10%**)

Interpretation:

- Markdown-aware, overlapping chunks keep full clauses (“Term and Renewal”, “Fees”, “Feature Enhancements”, HR responsibilities) inside the same chunk.
- Retrieval is more precise: the system more often lands on the correct *type* of document and the correct *file*, but the improvement is still moderate.

### 4.2 Effect of reranking (on top of overlap index)

Comparing `overlap_k3` vs `overlap_rerank_k3`:

- **Hit@3 (doc_type):** 0.742 → 0.936 (**≈+20%**)
- **Avg RankScore@3:** 0.581 → 0.817 (**≈+24%**)

Cross-encoder reranking uses the full `(question, chunk)` pair, not just embeddings.  
This helps especially for:

- Contract questions with similar wording across clients.
- Analytics / telematics / roadmap questions where multiple chunks mention similar terms.
- Multi-document questions that require picking the **most relevant** contract or HR profile.

Combining both enhancements vs baseline:

- **Hit@3:** 0.633 → 0.936 (**≈+30%** relative to baseline)
- **Avg RankScore@3 (primary metric):** 0.484 → 0.817 (**≈+33%** relative to baseline)

### 4.3 Relation to assignment criteria

Chosen metrics:

- **Primary:** Avg RankScore@3 (file-level)
- **Secondary:** Hit@3 (doc_type)

For the 31-question evaluation set:

- The primary metric improved from **0.484** to **0.817**, which is **well above the required +30%** threshold.
- The secondary metric improved from **0.633** to **0.936**, confirming that the system is now usually:
  1. Searching in the correct part of the knowledge base.
  2. Surfacing the correct files near the top of the retrieved context.

Overall, the combination of **better chunking** + **cross-encoder reranking** gives a clear, measurable quality jump for the InsureLLM RAG subsystem.

