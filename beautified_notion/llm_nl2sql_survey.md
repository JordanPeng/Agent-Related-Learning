# 🤖 LLM-Based NL2SQL Systems & Taxonomies

This document captures modern architectures, benchmarking datasets, evaluation metrics, and optimization loops that have emerged since LLM-based pipelines became standard for Natural Language to SQL (NL2SQL) tasks.

---

## 🌐 1. Contemporary Architecture Overview

The modern LLM-based NL2SQL pipeline is divided into three key stages:

```text
[ Natural Language Query (NLQ) ]
              │
              ▼
    1. Question Understanding   ── (Disambiguation, Intent Alignment)
              │
              ▼
    2. Schema Comprehension     ── (Schema Partitioning, Context Compression)
              │
              ▼
    3. Structural SQL Synthesis ── (RAG Few-Shot, Compiler/Execution Feedback)
              │
              ▼
      [ SQL Deliverable ]
```

### 1.1 Key Stages
1.  **Question Understanding:** Translates colloquial, vague, or short queries into structured logical concepts, resolving semantic ambiguity before code synthesis begins.
2.  **Schema Comprehension:** Filters, formats, and selects database schemas (tables, columns, and relationships) to fit within context length constraints and focus the model on relevant resources.
3.  **Structural SQL Synthesis:** Utilizes generative LLMs to synthesize precise SQL. This process is optimized using in-context RAG few-shot examples, chain-of-thought prompting, and execution feedback loops.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/9acd4a35-c75d-460c-b28e-4fafb6cc1d85/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZHTR54ZM%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223903Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDhzUHotP45hPfqwivCxcyU0DFh1agn0xI%2Bguc3Qd9T1AIhAJT39ZRV8VJMElgCj%2BqWXAk3VwaY3pJqwlfTrsLYG%2Bh7KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igxw0t4q47WP%2FZTKo3Yq3AOd1gU%2BZd5MJvUpAEjjkpPzxLNYelnLqScJaEPJjGjH91FvD7TJOIxBFJbdsZSjWJ1uc0ug2FoYGEG90NJIfWKFRV9%2Fy4TZzRoldeE0gm04dSUjFlgCxBb4MRnbQgyWk%2F6WNyNAIUZjUw2v45yZgbzY1%2FXifLHoHIk7SgUsO0cD2zdmyg2zvikfd1lXYx3KWh81Qjj0%2Fo5wliE0gujuYBYvv1hjY2yVUGQR2f1atuWyiY6DpDXAgt%2BhJZrpxTJVQPT4KavOEmkRNNc3BbEG%2F9s%2BnZNPpeaRQaF8AqZrmpFQ5gqwwjOCjN2JxozxpCHGUBb%2FMY2WpdGS9fgEKKaBUg5bnm1GnWTld7tIdmgeY4ES1%2FwOq9xw3egAsLiF64QP85zjDZcy768AdsXdb7UEOkVGzUUv12UBsTWJJCdpflFHvMeuywhl8eSMQHzobjRyRh2D7fU9PnzzyXhbb2MMz5SDX9ztGHkHarKaT9ILLgP%2FYd1h4Kc%2FIP30WPIaAAiHefgffpx%2Fw2sIusnLigqE62xcBAZY5QaRsipEgJOtSxSOSag3qZxUjmo3jqCJ3jTTYg4NXmS5umZW9wQmc5bgWDPld36GqpgcRLzB%2Be237bw96zZp2dbY7EiZuFt3fjC61ZfRBjqkAfGXy5lcFe476vndCFkgtYV9wVeA8HNCbMCJJguzbx5c61zVtVt2C6G5UWHdcnA6pvLYxDBo7b%2F0J1UzLWL%2FBw7MI58ysErBEFsTQlJGegkIQyjo80%2FTgCmxAj%2FB2Tx2sazrv26Y2F5pSij7e4HtGH0Y7G3O8bKZDoPXFrVo0RL5GsTxR8GKfsrC6XH8lysStVNrceYLusp8rkCTnnGUPFxV777A&X-Amz-Signature=63286a0e7dc07a206f332fe21691d4a0feb08f7947c616a10fa8096aaf4a562c&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

## 📊 2. Benchmarks, Datasets & Taxonomy

Contemporary NL2SQL datasets evaluate models on their ability to generalize across new schemas, handle multi-turn conversations, and remain robust when encountering real-world database pollution.

```mermaid
graph TD
    Datasets[NL2SQL Datasets] --> CrossDomain[Cross-Domain Generalization]
    Datasets --> KnowledgeAug[Knowledge-Augmented]
    Datasets --> ContextDep[Context-Dependent / Multi-turn]
    Datasets --> Robustness[Robustness & Perturbations]
    
    CrossDomain --> Spider[Spider Baseline]
    CrossDomain --> BIRD[BIRD Academic Standard]
    KnowledgeAug --> BIRD_K[BIRD External Knowledge]
    ContextDep --> SParC[SParC / CoSQL]
    Robustness --> Spider_DK[Spider-DK / Spider-Syn]
```

### 2.1 Benchmark Types
*   **Cross-Domain Generalization:** Evaluates the system's ability to run zero-shot queries on unfamiliar databases and across different industries (e.g., **Spider** and the industry-standard **BIRD** benchmark).
*   **Knowledge-Augmented:** Pairs complex questions with external domain knowledge, such as business logic or formula details, to mirror real-world analytical tasks.
*   **Context-Dependent (Multi-Turn):** Tracks interactive conversations where subsequent questions rely on context from earlier turns (e.g., **SParC**).
*   **Robustness under Perturbations:** Tests model stability by introducing column abbreviations, database noise, or spelling errors into user database inputs.

---

## 📈 3. Specialized Evaluation Metrics

Evaluating SQL accuracy requires more than simple text-matching metrics, which fail to handle equivalent queries written with different syntax.

1.  **Component Matching (CM):**
    Evaluates individual SQL clauses (e.g., `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, aggregate functions) using an F1 score. This tracks whether the correct structural elements are retrieved.
2.  **Exact Matching (EM):**
    Compares the generated SQL against gold standard references by evaluating their abstract syntax trees (ASTs). This is highly precise but can penalize valid, alternative SQL formulations.
3.  **Execution Accuracy (EX):**
    The gold standard performance metric. Measures whether executing the generated SQL on the target database returns the exact same result set as the gold standard query.
4.  **Valid Efficiency Score (VES):**
    Compares execution execution times. Useful for assessing whether a generated query is optimized for speed and indexing compared to equivalent, slower queries.

---

## 🔁 4. Advanced Production Optimization Loops

```mermaid
graph LR
    Prompt[1. Prompt Chain & Schema Filter] --> LLM_Gen[2. LLM Codegen]
    LLM_Gen --> Execute[3. Test Execution on Database]
    Execute -->|Capture Errors / Logs| Refine[4. Error Feedback & Self-Correction]
    Refine --> Prompt
```

### 4.1 Major Optimization Strategies
*   **Few-Shot In-Context Selection:** Selects relevant in-context examples from history using vector embeddings or structural similarity scores. This ensures the model learns from patterns similar to the current prompt.
*   **Schema Filtering and Pruning:** Automatically hides unrelated tables and columns to decrease context length pressure and prevent distraction-related synthesis errors.
*   **Execution-Guided Self-Correction:** Runs the generated SQL on a mock sandbox database, captures any runtime database syntax or schema errors, and passes them back to the LLM to trigger self-correction steps.
