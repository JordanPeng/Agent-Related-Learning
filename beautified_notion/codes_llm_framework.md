# 🚀 CodeS: Scalable Open-Source LLMs for Text-to-SQL

This document summarizes the core methodologies, pre-training schemes, schema compression techniques, and domain transfer strategies introduced in the CodeS framework.

---

## 📌 1. Foundational Objectives

The CodeS paper addresses a key question in natural language database querying:

> **Core Question:** *"How can small-sized language models (e.g., 7B to 15B parameters) achieve state-of-the-art text-to-SQL reasoning capacity on par with massive closed-source models?"*

### 1.1 Key Challenges
1.  **Limited SQL Pre-training Data:** Foundational models (like LLaMA-2) often perform poorly on SQL generation tasks because SQL code represents only a tiny fraction of their overall pre-training web corpora.
2.  **Reasoning Constraints of Small Models:** Small models have less capacity to perform complex, multi-hop schema linking and joint reasoning on queries with deep nesting or multiple filters.

To solve this, CodeS introduces **incremental task-specific pre-training** on high-quality, curated SQL and text-to-SQL data.

---

## 🧬 2. Architectural Framework & Lifecycle

The life cycle of the CodeS pipeline consists of:

```mermaid
graph TD
    Pretrain[1. Incremental Pre-training] --> PromptComp[2. Schema Filter & Value Grounding]
    PromptComp --> DomainTransfer[3. Domain Adaptation & Template Synthesis]
    DomainTransfer --> Eval[4. Benchmark Evaluation Spider/BIRD]
```

### 2.1 Stage 1: Incremental Pre-training
CodeS performs next-token prediction on a curated text-to-SQL corpus. Crucially, the training objective maximizes the likelihood of the entire sequence, mapping natural language prompts directly to corresponding schemas and target queries:

$$\max_{\theta} \sum_{t=1}^{T} \log P(x_t \mid x_{...t}; \theta)$$

---

## 🔍 3. Prompt Optimization & Schema Filtering

To prevent context window overflow when working with large databases containing hundreds of tables and columns (a frequent issue with narrow-context models), CodeS utilizes advanced input compression:

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/aa8c9719-7bd1-4dbe-a1b2-f51ce06c8734/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SYCD5CZK%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223906Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDRTkzcsoKT1EVq1OyA8d%2BOq4C1Kwb5gEhuoArccBIcHwIhALweyPRaFnMtVLFlbmOC3vRp72guuyoDBgQLI2tcPZ01KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igwd7R59%2FKlFKYeDZowq3APzF5yV8YiqQsqxT72hm5CXVHbdESYKs1D5cgIb4sFGeioTqTLNBrhenKXU5FDzlCk5eq1tXTVuPIhBco9myeGNsLhWNv7SmBmQIkAbk5F9Kn77T3F01jVqdH1XsIO8svBPEHnnh%2FVWBKp9OmtdXJ7col8mbTuxUoJB%2FzQqizj8Bd8CpkIxc86jZ06u%2BJtbyiyXjSXrRLILadmq6Rz5q6l37S9uTlGuf6ejgcHaN4ZTaD%2FDciwcoPWt68dinll34B4W2AaVTHLn32ZyctjBWPn3V2Ncit6d9b7PWF8QhYP6TTg8EMAytpqpuGZGymEFUBwFTbTO2Sz3Po6bVPOPLwE7a5Kr4A3ysamg%2Bw4xUvAvCmG47IXBVm4KpZLs6Ni0lO72ALjXiAYfFhtkPS0eunES10Pk7jzfOf506Q7O%2BfT7TMvXw2clTe8%2F%2B7w%2BE7MgLyp%2BN87kGzTqhH1%2Ff%2FBkDOsC4I60mD%2B5skKXZWUa1p2rXKnL0TvRMssnYZBB418cwi7l7Ioer49T0Joa109NLzE%2BZKBqlclpHU8NErlAuV0l7bO1zpdam%2B0YsUH7Ke2ciZf30MHJkfCXyu76Q%2B5jIlKb6Ug3H1RTgKlwnqFMjNn1zHY0M4iHo%2FofiLJ1bzCp1pfRBjqkASzHkNXjPC%2BN1az2ASA2WNL3AsEV7%2BMNAPYs1mLwcFQl7vXy2VT33B%2FwVeWl3CyxyJrsu%2BYAU49nTLBiMW4o9pTaOEvwegxO7jeJocJJS8UoAVoz2K%2F%2BTSgxrnY6i7UEPF6UnbdRCEeiLBR8h%2BcW5NxPYfOITIgzuDCF1vgxIqxhlDdygTfLn0GPRGQl87sZDJ4YVQ7tdWLljGaPh%2Br7HNzABVOP&X-Amz-Signature=5cf38fcd070b6aae9d23b2da63152f9bc06cf2a695d0811d650297301194f0c1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

### 3.1 Key Pruning and Enrichment Methods
*   **Schema Filtering:** Employs a lightweight schema routing module that identifies and retains only the tables and columns relevant to the user query. Unrelated database elements are stripped out of the prompt sequence.
*   **Metadata Integration:** Embeds schema column descriptions, abbreviations, and relationships directly inside the prompt context to aid model translation.
*   **Coarse-to-Fine Value Grounding:** Matches question entities against large database cell values. It begins with a **BM25 full-text index** to locate candidate columns, and then applies the **Longest Common Substring (LCS)** algorithm to isolate and extract exact, case-sensitive database cell matches.

---

## 🔄 4. Domain Transfer & Data Augmentation

To adaptively transfer a model's natural language comprehension to a new database domain without manual annotation:

### 4.1 Dual-Path Data Synthesis
1.  **Real Query Seed Synthesis (Top-Down):** Collects a small set of real-world user questions, manually drafts their corresponding target SQL statements, and uses GPT models to generate variations.
2.  **Structural Template Generation (Bottom-Up):** Reuses existing query templates from academic benchmarks like BIRD or Spider. The framework injects columns, tables, and cell values from the target domain into these templates to synthesize a diverse evaluation dataset.

---

## 🏆 5. Performance benchmarks

On major academic benchmarks like **Spider** and **BIRD**, the specialized CodeS model demonstrates that targeted pre-training and schema compression enable small-sized models to achieve accuracy competitive with larger closed-source LLMs.
