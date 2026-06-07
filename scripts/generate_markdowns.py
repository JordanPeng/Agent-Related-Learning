import json
import re
import os

# Create directory
os.makedirs(r"f:\agent_learning\beautified_notion", exist_ok=True)

# ----------------- Gather all content references -----------------
# 1. Advanced NLP Basics
cmu_nlp_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHxURFhtR1NnbjRqRkN0dHFXTHc__vscode-1780864286786\content.json"
nlp_data = json.load(open(cmu_nlp_json, "r", encoding="utf-8"))["text"]
nlp_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", nlp_data)

# 3. NL2SQL Survey before LLM
survey_before_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHx0cjUyTXBPa0wzdDBlT2FNM3Y__vscode-1780864286791\content.json"
before_data = json.load(open(survey_before_json, "r", encoding="utf-8"))["text"]
before_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", before_data)

# 4. NL2SQL LLM survey
survey_llm_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHxsSlFxNnNBZ3gyVXJoNnpQOEU__vscode-1780864286792\content.json"
llm_data = json.load(open(survey_llm_json, "r", encoding="utf-8"))["text"]
llm_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", llm_data)

# 5. CodeS
codes_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHxXZkp2cTBnMUdXeVgzZVhiMEI__vscode-1780864286793\content.json"
codes_data = json.load(open(codes_json, "r", encoding="utf-8"))["text"]
codes_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", codes_data)

# 6. Roadmap
roadmap_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHw0NDVkblR4cTFyajRyWmxnR1k__vscode-1780864286794\content.json"
roadmap_data = json.load(open(roadmap_json, "r", encoding="utf-8"))["text"]
roadmap_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", roadmap_data)

# 7. Resume Introduction
resume_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHxVd1lmaHRyaUZqSXJCSkt3NXE__vscode-1780864286800\content.json"
resume_data = json.load(open(resume_json, "r", encoding="utf-8"))["text"]
resume_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", resume_data)

# 8. Structuring Prompts
prompt_struct_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHx4cktyMUhRdmNMeXFxbGZ2M0U__vscode-1780864286803\content.json"
prompt_struct_data = json.load(open(prompt_struct_json, "r", encoding="utf-8"))["text"]
prompt_struct_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", prompt_struct_data)

# 10. Microsoft Benefits
benefits_json = r"c:\Users\pengc\AppData\Roaming\Code\User\workspaceStorage\ce8aa75a80cfc78157328b77978864e1\GitHub.copilot-chat\chat-session-resources\8f2db17f-3220-403e-a2b3-e6f5c7fdbbbe\call_MHxmcDJZUFkzVnZ4NHVlVGxsVEs__vscode-1780864286812\content.json"
benefits_data = json.load(open(benefits_json, "r", encoding="utf-8"))["text"]
benefits_imgs = re.findall(r"!\[\]\((https://[^\)]+)\)", benefits_data)

# ----------------- Draft All Masterpieces -----------------

# Draft 1: CMU Advanced NLP Basics
cmu_nlp_md = f"""# 🧠 CMU Advanced NLP Fall 2024: Tool Use & LLM Agent Basics

本篇笔记整理自卡内基梅隆大学（CMU）高阶自然语言处理课程（Advanced NLP Fall 2024），系统探讨了 LLM 核心支柱之一的网络代理（Agentic Workflows）及其最基础的“工具调用（Tool Use）”原理与机制。

---

## 🧭 1. 核心大纲与代理要件

一个真正的 **AI Agent**（人工智能代理）区别于传统文本生成模型的核心，在于其对外界的主动感知和自我闭环迭代：

### 1.1 代理三大特征 (Core Criteria)
*   **Proactive tool utilization:** 主动发现、选择并调用各类型工具。
*   **Iterative multi-step reasoning:** 并非单次一问一答，而是具备自我反思（Reflection）、规划和逐步拆解解决复杂问题的能力。
*   **Interaction with the outer environment:** 能够对真实的沙盒、数据库、操作系统或网络世界施加影响，并观察对应的结果反馈。

### 1.2 代理基础组成 (Structural Pillars)
1.  **Backbone Large Language Model:** 强大的底层大模型（作为认知 and 大脑中枢）。
2.  **Prompt Core Scheme:** 配置系统角色、行动框架（如 ReAct）、可选择的工具约束等。
3.  **Action / Observation Spaces:** 供模型选择调用的函数定义（输入/输出 schema）以及模型执行后的控制台返回（Observation）。

---

## 🛠️ 2. 语言模型中的工具调用机制 (Tool Use in LMs)

### 2.1 什么是“工具”？
在语言模型上下文中，**工具**（Tool）通常是指一个外部计算机程序的 API/函数调用端口。LLM 本身不具备代码编译、数值求积、网络爬取或运行特定程序的能力，但能通过**合理生成对应的函数名及其规范的输入参数（arguments）**来调用外部程序。

```text
[ LLM Backbone (Decides Action) ] 
          │ (Generates formatted call JSON: e.g. run_query(sql))
          ▼
[ Tool Executor API (Runs program locally or in sandboxed server) ]
          │ (Calculates and captures printed stdout/JSON result)
          ▼
[ Observations Grid (Injected back to LLM context of next turn) ]
```

### 2.2 工具基本功能维度 (Functionality Taxonomy)
*   **Perception (感知型工具):** 用于从外部提取、监测、查询数据（如：搜索引擎、天气监控端口、数据库查询 API）。
*   **Action (执行型工具):** 改变外部世界或系统状态（如：创建/更新本地文件、执行 shell 命令、完成转账动作）。
*   **Computation (计算型工具):** 执行通用的精确数学或深度离线运算（如：Python 执行沙盒、WolframAlpha、科学计算器）。

![]({nlp_imgs[0]})

---

## 📊 3. 环境表示与信息理解 (Environment Representation)

在多 Agent 协同体系中，模型需要对环境、状态转换 and 感知深度建立清晰的数学 and 符号表示。

### 3.1 感知空间与世界模型
![]({nlp_imgs[1]})

大语言模型对世界/环境信息的理解可以建模为马尔可夫决策决策树，模型在当前状态 $S_t$ 下通过观察 $O_t$ 评估概率：

$$P(O_{{t}} \\mid S_t) \\quad \\text{{and}} \\quad P(S_{{t+1}} \\mid S_t, A_t)$$

代理必须学习在长文本上下文中提炼最核心的状态编码，以便在后续链路重组时避免干扰。

### 3.2 探索、好奇心与回馈 (Curiosity & Exploration)
为了避免 Agent 在自主执行复杂长链路任务时落入局部最优（即死循环或无限 Regeneate 同一个命令），先进的代理系统通过基于信息熵或预期回报误差的**“好奇心奖励机制”**来激励模型尝试尚未被广泛覆盖的动作空间。

![]({nlp_imgs[2]})

---

## 📈 4. 推理、规划与多代理协作 (Reasoning, Planning & Multi-Agent)

### 4.1 规划与树形推理
高难度的逻辑与工程任务单靠一步步 Chaining 无法高品质应对，为此引入树形（Tree）和图（Graph）规划。

![]({nlp_imgs[3]})
![]({nlp_imgs[4]})

*   **Tree-of-Thoughts (ToT):** 模型在每个决策分叉口产生多条候选推理链，并通过自评估（Evaluate）回溯、剪枝或寻找最优解。
*   **Error Correction & Introspection:** 模型捕获到环境抛出的语法/编译或逻辑报错后，自动触发 Self-Reflection 提示，重组上轮 Prompt 规划后续行动。

### 4.2 多代理协作系统设计 (Multi-Agent System Blueprint)
![]({nlp_imgs[5]})

复杂的长周期工作可解耦并交给多个微特型 Agent 协同组装，多代理框架通常包含以下底层支撑：
*   **Clear Task Decomposition:** 拆分问题，通过手势化 Handoff 动态转交上下文控制权。
*   **Dynamic Knowledge Insertion:** 根据当前被委托 Agent 的专业度，定向按需拉取、加载 KQL/SQL schema 或 RAG 文档切片。
*   **Consensus & Verification:** 设置专门的交叉审计角色（Evaluator / Critic），验证生成的代码、数据报表或事件结论，确保质量不劣化。
"""

with open(r"f:\agent_learning\beautified_notion\cmu_nlp_basics.md", "w", encoding="utf-8") as f:
    f.write(cmu_nlp_md)


# Draft 2: Draft of Review Paper
review_md = """# 📝 Federated LLM Fine-Tuning: Comprehensive Literature Review

> **Subject:** Parameter-Efficient Federated Fine-Tuning of Large Language Models (PEFT-FL)  
> **Status:** Draft / Active Survey  
> **Target Publication:** ML/NLP Review Track 2024–2025

---

## 🌍 1. Introduction

### 1.1 Background & Motivation
**Federated Learning (FL)** preserves privacy by keeping training datasets decentralized on edge client environments (like medical servers, client devices, and private enterprise nodes). Simultaneously, **Large Language Models (LLMs)** have achieved state-of-the-art results across NLP tasks, but adapting them to specialized industries requires intensive private fine-tuning.

Merging these two fields yields **PEFT-FL**—where parameter-efficient adapters (like LoRA, prompts, and prefixes) are fine-tuned across client networks, allowing collaborative learning with minimal network communication overhead.

### 1.2 Core Challenges
This review systematically categorizes and analyzes state-of-the-art literature across **three fundamental challenges**:
1.  **Data Heterogeneity & Client Drift:** Mitigating mathematical divergences caused by Non-IID client distributions.
2.  **Communication & Computational Bottlenecks:** Compressing weights and utilizing forward-only pipelines for low-energy edge training.
3.  **Client Resource Heterogeneity & Scalability:** Scaling pipelines across devices with wildly differing GPU/VRAM capabilities.

---

## 🛡️ 2. Core Taxonomy: Challenges & Modern Solutions

```mermaid
graph TD
    Challenges[Federated LLM Fine-Tuning Challenges]
    Challenges --> C1[1. Data Heterogeneity & Client Drift]
    Challenges --> C2[2. Communication & Computation Cost]
    Challenges --> C3[3. Resource Scalability]
    
    C1 --> SLoRA[SLoRA Babakniya 2023]
    C1 --> FlexLoRA[FlexLoRA Bai 2024]
    C1 --> PromptTuning[Adaptive Prompts Che 2023]
    
    C2 --> PETuning[FedPETuning Zhang 2023]
    C2 --> Tensor[Tensorized FFT Ghiasvand 2024]
    C2 --> FwdLLM[FwdLLM Xu 2024]
    
    C3 --> FedPipe[FedPipe Fang 2024]
    C3 --> FlexLoRA2[FlexLoRA Adaptive Pipelines]
```

### 2.1 Addressing Data Heterogeneity and Client Drift

In a federated layout, client datasets are rarely Independent and Identically Distributed (Non-IID). This task and linguistic distribution mismatch across clients leads to **Client Drift**—where individual local models converge toward localized objectives, pulling the global aggregated model away from global optimality.

| Study & Authors | Key Core Concept | Technical Implementation | Novel Contribution |
| :--- | :--- | :--- | :--- |
| **SLoRA**  <br>*(Babakniya et al., 2023)* | **Sparse Low-Rank Adaptation** | Employs sparse weight matrices together with low-rank projection of adapters to stabilize aggregation. | Reduces active update size, minimizes gradients collision during merge. |
| **FlexLoRA**  <br>*(Bai et al., 2024)* | **Dynamic & Elastic Adapter Size** | Dynamically adapts adapter sizes and styles based on local client data complexity. | Resolves divergent task profiles across highly distinct local tasks. |
| **Adaptive Prompts**  <br>*(Che et al., 2023)* | **PEFT Prompt & Custom Optimizer** | Merges soft prompt tuning with localized learning rate schedules. | Reduces client divergence; aligns client soft prompt tokens in shared subspace. |

---

### 2.2 Reducing Communication & Computational Overhead

Collaborative fine-tuning of billions of parameters over commercial internet connections is a computational bottleneck. Modern work actively cuts gradient transfer packages and hardware consumption.

*   **FedPETuning (Zhang et al., 2023):**
    <callout icon="💡" color="gray_bg">
    **Methodology:** Restricts all shared parameters strictly to a small set of soft tokens or adapters, keeping frozen LLM weights client-side. Accomplishes up to 99% bandwidth savings compared to full weight exchanges.
    </callout>
*   **Tensorized FFT (Ghiasvand et al., 2024):**
    Uses tensor decomposition to aggressively compress structural updates before dispatching them over TCP/IP connections. Preserves global model accuracy while slashing communication packets by more than 10-fold.
*   **FwdLLM (Xu et al., 2024):**
    Redesigns edge training by relying on **forward-only perturbations** (backpropagation-free calculations). This drastically reduces VRAM requirements, making federated updates feasible on standard edge devices with no local backprop pipelines.

---

### 2.3 Enhancing General Scalability Across Edge Nodes

Edge nodes (commercial clusters, local workstations, mobile devices) exhibit severe hardware disparities—varying from a single V100 GPU (32GB) to deep multi-node A100 setups (80GB+).

*   **FedPipe (Fang et al., 2024):**
    An automated federated pipeline that seamlessly orchestrates mixed-precision training, low-rank adaptations, and model quantization.
    *   *SVD Filtering:* Evaluates the importance of weight layers via SVD (Singular Value Decomposition) to select which layers to tune.
    *   *Adaptive Training:* Assigns quantized weights and variable batch sizes recursively based on live performance metrics from heterogeneous clients.

---

## 🔮 3. Future Research Directions

1.  **Advanced Heterogeneous Aggregation:** Establishing robust aggregation methods that can merge mathematically varied adapter formats (varying ranks and sparsities) natively.
2.  **Privacy-Enhanced PEFT-FL:** Integrating secure multiparty computation (SMPC) or differential privacy (DP) into highly compact dynamic adapters without causing severe convergence degradation.
3.  **Asynchronous Scheduling:** Shifting away from synchronous training rounds to robust asynchronous setups, preventing slow or offline edge devices (stragglers) from stalling the overall global aggregation cycle.
"""

with open(r"f:\agent_learning\beautified_notion\review_paper_draft.md", "w", encoding="utf-8") as f:
    f.write(review_md)


# Draft 3: Presentation Notes
presentation_md = """# 🎤 Oral Presentation: Literature Survey on Federated Fine-Tuning of LLMs

> **Time Allocation:** 15 Minutes  
> **Topic:** Parameter-Efficient Federated Fine-Tuning of Large Language Models (PEFT-FL)  
> **Structure:** Intro (3m) $\to$ Challenge 1: Data Heterogeneity (4m) $\to$ Challenge 2: Resource Constraints (4m) $\to$ Challenge 3: FedPipe (3m) $\to$ Q&A (1m)

---

## 🎬 1. Introduction Plan (00:00 - 03:00)

*   **Greeting & Hook:**
    > *"Hi everyone, our team project is a deep-dive literature survey on Parameter-Efficient Federated Fine-Tuning of LLMs. In today's talk, we'll walk through the unique challenges of fine-tuning large models across decentralized networks and explore how cutting-edge research is paving the way for highly scalable, private AI."*
*   **Definitions & Architectural Basics:**
    *   Introduce **Federated Learning (FL)** as a decentralized privacy-preserving paradigm where updates—not raw data—are transferred.
    *   Introduce **PEFT (Parameter-Efficient Fine-Tuning)** as an essential tool to make this possible by shrinking transferable gradients to less than 1% of the base model size.
*   **Survey Design:**
    *   This domain is relatively new, with fewer than a few dozen core papers. We have organized our review around the three most urgent engineering challenges:
        1.  *Data Heterogeneity & Client Drift*
        2.  *Communication/Computational Cost*
        3.  *Client Resource Disparities*

---

## 🛡️ 2. Core Discussion: Challenges 1 & 2 (03:00 - 11:00)

### 2.1 Challenge 1: Data Heterogeneity & Client Drift
*   **Problem Statement:** Non-IID local datasets pull local parameters toward distinct localized optima, resulting in "Client Drift" upon global aggregation.
*   **Literature Highlights:**
    *   We introduce **SLoRA (Babakniya et al., 2023)**, which enforces sparse low-rank adaptation to stabilize gradient matrices.
    *   We compare it with **FlexLoRA (Bai et al., 2024)**, which makes rank assignments dynamic based on task complexity.

### 2.2 Challenge 2: Communication & Computation Overhead
*   **Problem Statement:** Moving hundreds of megabytes of weight parameters over slow connections stalls collaborative learning loops.
*   **Modern Remedies:**
    *   Describe **FedPETuning (Zhang et al., 2023)**, which freeze base weights and exchange only the lightweight adapters.
    *   Briefly mention **FwdLLM (Xu et al., 2024)**, which uses forward-propagation perturbation for ultra-low VRAM edge execution.

---

## 🏋️ 3. Deep Dive: Scalability with FedPipe (11:00 - 14:00)

*   **Problem Statement:** Edge client machines are highly heterogeneous—one client may have an 80GB A100 GPU, while another might be limited to a 32GB V100 or commodity hardware.
*   **The Solution - FedPipe (Fang et al., 2024):**
    *   Designed specifically to accommodate mixed resources by dynamically assigning parameters, ranks, and batch sizes.

### 📊 Mathematical Framework
FedPipe models this resource optimization mathematically. The system solves a structured loss minimization problem constrained by computational budgets:

$$\\min_{\\Theta} \\sum_{{i=1}}^{{B}} \\mathcal{{L}}_i(W_0 + \\Delta W( \\theta_i )) \\quad \\text{{s.t.}} \\quad \\text{{VRAM}}(\\theta_i, b_i) \\le \\text{{GPU\\_Cap}}_i$$

*   Where $\theta_i$ represents the allocated adapter parameters (rank, position) and $b_i$ is the custom batch size for client $i$.

### ⚙️ How FedPipe Works under the Hood
1.  **Iterative Layer Profiling via SVD:**
    Instead of training arbitrary layers, FedPipe uses Singular Value Decomposition (SVD) on weight matrices, assigning adapters to the most information-dense dimensions:
    
    $$W = U \\Sigma V^T$$
    
    Weight layers are ranked by the magnitude of their singular values ($\\Sigma$), prioritizing high-variance layers for adaptation.
2.  **Adaptive Resource Partitioning:**
    *   *Batch Size:* Scaled proportionally to the node's relative compute capacity, ensuring it stays within a safe, configured VRAM threshold.
    *   *Elastic Ranks:* Clients assign adaptive ranks (e.g., $r=4$ for low-VRAM nodes, $r=16$ for high-VRAM nodes). The global server aggregates these variable-rank matrices by projecting them into a unified low-rank subspace before redistributing them.

---

## 🏁 4. Slide Summary & Future Directions (14:00 - 15:00)

*   **Key Presentation Takeaway:**
    > *"Through methods like SVD projection and adaptive local parameter allocation, we can successfully run federated fine-tuning across highly diverse network environments."*
*   **Future Frontiers:** Highlight Asynchronous Parameter Consolidation to eliminate waiting on slower clients (stragglers), and integrating differential privacy natively inside adapter spaces.
"""

with open(r"f:\agent_learning\beautified_notion\presentation_notes.md", "w", encoding="utf-8") as f:
    f.write(presentation_md)


# Draft 4: NL2SQL Survey before LLM
survey_before_md = f"""# 📝 Deep Learning NL2SQL Foundations (Before LLMs)

This study guide reviews the fundamental architectures, taxonomies, and methodologies used in neural Natural Language to SQL (NL2SQL) translation prior to the emergence of highly generalized Large Language Models.

---

## 📌 1. Definition of the NL2SQL Problem

Given a **Natural Language Query (NLQ)** describing user intent, and a **Relational Database (RDB)** with a specific schema $\\mathcal{{S}}$ (comprising tables, columns, and foreign keys):
Generate a mathematically equivalent **SQL Query** $\\mathcal{{Q}}$ that executes successfully on the target database, returning the precise data matching the user's intent.

$$f(\\text{{NLQ}}, \\mathcal{{S}}) \\to \\mathcal{{Q}}$$

![]({before_imgs[0]})

---

## ⚙️ 2. Core Translation Architectures (Chronological Roadmap)

Prior to LLMs, translating natural language to structured queries progressed through several distinct neural paradigms:

```mermaid
graph TD
    Rule[1. Rule-Based / Pattern Matching] --> Seq2Seq[2. Seq2Seq / Pointer Networks]
    Seq2Seq --> Sketch[3. Slot-Filling / Model Sketches]
    Sketch --> Gen[4. Grammar/AST Tree-Based Generation]
```

### 2.1 Sequential Sequence-to-Sequence (Seq2Seq & Pointer Net)
*   **Concept:** Uses encoder-decoder networks (often Bi-LSTM or early Transformers) with **Pointer Net** mechanisms to translate queries token-by-token.
*   **Limitations:** Highly prone to grammar errors (e.g., writing invalid JOIN commands or open brackets). Pointer networks also struggle with deep schemas, frequently confusing table names with query criteria.

### 2.2 Sketch-Based Slot Filling
*   **Concept:** Uses a predefined, structured SQL syntax outline (or sketch) and employs specialized subnetworks to predict specific parts of the query. For example:
    *   *Sub-model A:* Predicts columns in the `SELECT` slot.
    *   *Sub-model B:* Predicts rows in the `WHERE` condition.
    *   *Sub-model C:* Decides the aggregation operator (`SUM`, `AVG`, `COUNT`).
*   **Limitations:** Cannot generalize beyond the pre-configured database structure or simple, single-table schemas (such as the WikiSQL evaluation benchmark).

### 2.3 AST & Grammar-Based Tree Generation (SOTA pre-LLM)
*   **Concept:** Instead of predicting plain text, the model generates an **Abstract Syntax Tree (AST)** step-by-step using a formal, Context-Free Grammar (CFG) like SEMQL. This ensures the output is syntactically valid by design.
*   **Key Model:** **IRNet** and **RAT-SQL** represent the state of the art in this paradigm.

---

## 🔗 3. Schema Linking (Graph & Attention Mechanisms)

A central challenge in NL2SQL is **Schema Linking**: identifying which database tables and columns are referenced in a natural language query, and mapping them to their correct schema symbols.

![]({before_imgs[1]})

### 3.1 RAT-SQL (Relation-Aware Transformer)
The breakthrough in schema linking came from RAT-SQL, which models the database schema as a detailed relational graph:
*   **Graph Nodes:** Represents individual tables and columns.
*   **Graph Edges:** Represents key database relationships, such as:
    *   *Column-Table ownership:* `column-belongs-to-table`
    *   *Relational connections:* `column-is-foreign-key-of`
    *   *Lexical matches:* `question-token-matches-column-name`
*   **The Mechanism:** The model encodes these nodes and edges using **Relation-Aware Self-Attention**. This allows the Transformer to perform schema linking by computing attention weights structured around actual relational constraints.

---

## 🗄️ 4. Grounding with Database Values

To achieve high execution accuracy, models must align entity names referenced in conversational queries with actual cells stored in database tables.

![]({before_imgs[2]})

### 4.1 Value Grounding Strategies
*   **Tri-Gram / Fuzzy Jaro-Winkler Matching:** Computes string similarities between words in the query and column headers to identify likely candidates.
*   **FTS (Full-Text Search) In-Memory Lookup:** Formulates a fast, behind-the-scenes query (using BM25 indexes or similar) to see if a query argument matches a specific database column value. This provides the generator with concrete evidence (e.g., *"Europe" matches the 'continent' column*) before it begins translating.
"""

with open(r"f:\agent_learning\beautified_notion\nl2sql_foundation_survey.md", "w", encoding="utf-8") as f:
    f.write(survey_before_md)


# Draft 5: NL2SQL LLM survey
survey_llm_md = f"""# 🤖 LLM-Based NL2SQL Systems & Taxonomies

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

![]({llm_imgs[0]})

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
"""

with open(r"f:\agent_learning\beautified_notion\llm_nl2sql_survey.md", "w", encoding="utf-8") as f:
    f.write(survey_llm_md)


# Draft 6: CodeS Survey and Overview
codes_md = f"""# 🚀 CodeS: Scalable Open-Source LLMs for Text-to-SQL

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

$$\\max_{{\\theta}} \\sum_{{t=1}}^{{T}} \\log P(x_t \\mid x_{{...t}}; \\theta)$$

---

## 🔍 3. Prompt Optimization & Schema Filtering

To prevent context window overflow when working with large databases containing hundreds of tables and columns (a frequent issue with narrow-context models), CodeS utilizes advanced input compression:

![]({codes_imgs[0]})

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
"""

with open(r"f:\agent_learning\beautified_notion\codes_llm_framework.md", "w", encoding="utf-8") as f:
    f.write(codes_md)


# Draft 7: Roadmap for Cleaning/Labeling data
roadmap_md = f"""# 📋 Database Cleaning & Labeling: Strategy Roadmap

This roadmap identifies data anomalies, outlines data validation methods, and outlines a step-by-step strategy for preparing bid-ask datasets to train predictive models.

---

## 🔍 1. Current Data Quality Issues

While our bid and ask price telemetry is generally consistent, we have identified several core data issues that must be addressed:

### 1.1 Outlier Volumetric Samples (Bid-Ask Extremes)
*   **The Issue:** Several records contain extremely high or low bid-ask prices paired with a transaction volume of exactly 1.
*   **Impact:** If left uncorrected, these highly volatile, low-density outliers distort regression modeling scales.
*   **Remedy:** Filter out low-volume transactions ($Size = 1$) that deviate by more than $\\pm 3$ standard deviations from the moving average price.

![]({roadmap_imgs[0]})

### 1.2 Telemetry Gaps (Missing Column Values)
*   **The Issue:** Gaps in specific time-series rows lead to null inputs during network execution.
*   **Remedy:** Apply forward-fill imputation for real-time streaming segments (assuming temporal price stability), or use linear interpolation for short gaps.

![]({roadmap_imgs[1]})

---

## ⚙️ 2. The Resolution & Extraction Pipeline

```mermaid
graph TD
    Raw[1. Raw Bid-Ask Telemetry] --> Filter[2. Volume-Weighted IQR Filter]
    Filter --> Impute[3. Temporal Linear Interpolation]
    Impute --> Normal[4. Z-Score Scaling & Normalization]
    Normal --> Output[5. Training Dataset]
```

### 2.1 Cleaning Steps
1.  **Volume-Weighted Outlier Filtering:** Use Interquartile Range (IQR) filtering restricted by volume weights to isolate and strip out low-density, highly volatile outlier prices.
2.  **Imputation:** Implement an automated pipeline that checks missing row footprints, forward-fills database rows for gaps shorter than 3 periods, and uses linear interpolation for larger gaps.
3.  **Z-Score Normalization:** Apply Z-score scaling across active features (such as bid/ask prices, moving averages, and rolling volatilities) to standardize training inputs.
"""

with open(r"f:\agent_learning\beautified_notion\data_cleaning_roadmap.md", "w", encoding="utf-8") as f:
    f.write(roadmap_md)


# Draft 8: Refer Information
refer_md = """# 👤 Executive Professional Profile: Chong Peng (Jordan)

This page provides professional background information, contact details, and an executive introduction for Chong Peng (Jordan), prepared for reference and application purposes.

---

## 📋 1. Core Profile Details

| Property | Details |
| :--- | :--- |
| **Full Name** | Chong Peng (Jordan) |
| **University** | Carnegie Mellon University (CMU) |
| **Education** | Master of Science in Artificial Intelligence Engineering (ECE) |
| **Timeline** | August 2023 - December 2024 |
| **Current Role** | Data Scientist, Azure Core (Microsoft) |
| **Email Interface** | [chongp@andrew.cmu.edu](mailto:chongp@andrew.cmu.edu) |
| **Connect** | [LinkedIn Profile](https://www.linkedin.com/in/chongpeng8717/) |

---

## 🎙️ 2. Professional Introduction (Third-Person Narrative)

**Chong Peng (Jordan)** is a Data Scientist within Microsoft's Azure Core division, holding a Master of Science in Artificial Intelligence Engineering from Carnegie Mellon University. Jordan possesses a strong track record of designing, evaluating, and deploying machine learning models and large language model workflows to solve complex industrial problems.

### 💼 Technical Internships & Core Milestones
*   **Microsoft Azure Core (Data Scientist Intern):**
    Jordan developed advanced tabular models to identify workload anomalies and optimize Azure Storage tenant provisioning. Additionally, he designed and implemented an end-to-end RAG system that translates natural language questions into valid, executable Kusto Query Language (KQL) queries.
*   **Tencent AI Lab (Research Intern - 4 Months):**
    Jordan conducted research on multi-modal representation learning, focusing on bi-directional face-voice matching. Within his first month, he designed and evaluated a state-of-the-art matching pipeline that outperformed existing academic models in matching accuracy.
*   **ByteDance AI Lab (AI Engineer Intern - 1 Year):**
    Jordan developed NLP and representation learning pipelines to support consumer-facing applications. His primary contributions included developing a multi-scenario noise-tolerant learning architecture and a style transfer framework for virtual host live-streaming on TikTok.

### 🌟 Academic Excellence
Jordan consistently achieved top academic performance at Carnegie Mellon University, maintaining a near-perfect GPA and earning multiple merit-based scholarships. His expertise spans mathematical optimization, linear algebra, and advanced prompting and fine-tuning techniques for large generative models. Jordan is highly skilled at taking projects from early-stage research to production-ready deployments.
"""

with open(r"f:\agent_learning\beautified_notion\profile_executive_reference.md", "w", encoding="utf-8") as f:
    f.write(refer_md)


# Draft 9: Resume Introduction & Core Technical Projects
resume_md = f"""# 📝 Technical Portfolio & Project Deep Dive - Chong Peng

---

## 🚀 1. Self-Introduction

My name is **Chong Peng (Jordan)**. I am a graduate of Carnegie Mellon University (CMU) with a Master of Science in Artificial Intelligence Engineering. Currently, I serve as a Data Scientist in Microsoft's Azure Core division.

I have extensive research and practical engineering experience across **Large Language Models (LLMs), Multimodal representation learning, and natural language processing**. My career is built on a simple philosophy: **take complex research, build clean datasets, write robust training/deployment pipelines, and deliver production-grade systems.**

---

## 💼 2. Microsoft Azure Core: Core Projects

### 2.1 Tabular Hardware Behavior & Provisioning Prediction
*   **The Problem:** When cloud tenants consume too many resources (hot state), virtual networks experience latency spikes and service outages.
*   **The Goal:** Predict hardware metrics (such as CPU and NIC utilization) to proactively configure resource limits on active tenants. This is designed to optimize Microsoft's STAR rating (Storage Tenant Allocation Ratings), guiding new account allocations toward healthy, low-risk servers.
*   **Methodology:** Tested Linear Regression, Tabular FT-Transformers, and Gated Adaptive Networks (Gandalf) on tenant attributes (e.g., memory configuration, tenant age) and workload characteristics (e.g., transactions per second, ingress GB/s).
*   **Performance:** Achieved an $R^2$ score of **0.92** and a Mean Absolute Error (MAE) of **2.8** for Average CPU predictions.

---

### 2.2 Natural Language to Kusto Query Language (NL2KQL)
*   **The Problem:** Out-of-the-box LLMs frequently generate syntactically invalid Kusto queries that do not match our database schemas or fail during execution.
*   **The Goal:** Build an end-to-end RAG system that translates natural language queries into valid, executable KQL queries matching Microsoft's internal `XDataAnalytics` and `XStore` schemas.

```mermaid
graph TD
    Question[User Question] --> SchemaFilter[1. RoBERTa Schema Filtering]
    SchemaFilter --> Context[Prompt Construction: Question + Pruned Schema]
    Context --> FTModel[2. Quantized CodeS Model Fine-Tuning]
    FTModel --> Execution[3. Sandbox Query Execution]
    Execution --> Output[Executable KQL Output]
```

#### 🔍 Step 1: RoBERTa-Based Token-Level Schema Filtering
To translate natural language queries into KQL when database schemas are too large for standard model context windows:
1.  Concatenate the user question with candidate table schemas using specialized delimiters:
    
    $$\\mathcal{{X}} = [\\text{{Query}}] \\; \\Vert \\; [\\text{{Table}}_1: \\text{{Col}}_1, \\text{{Col}}_2] \\; \\Vert \\; [\\text{{Table}}_2: \\text{{Col}}_1, \\dots ]$$
    
2.  Pass the sequence through an attention-masked RoBERTa encoder, allowing each table node to attend dynamically back to the user query.
3.  Apply a two-layer Bi-LSTM pooling network over the final hidden states to score and filter top-$k$ relevant tables and columns.

#### ⚙️ Step 2: Incremental Pre-training & Fine-Tuning of CodeS
1.  **Pre-training:** Gathered Azure KQL reference guides, user documentation, and crawled methods, pre-training a specialized CodeS model using a next-token prediction objective.
2.  **Unsupervised Pipeline Generation:** Passed historical KQL scripts through a schema-matching pipeline to associate them with tables. Used automated prompting to generate matching natural language queries, producing a deep, high-quality parallel training dataset.
3.  **Fine-Tuning:** Fine-tuned the model on next-token prediction using the structured payload:
    
    $$\\text{{Payload}} = [\\text{{Pruned Schema}}] \\; \\Vert \\; [\\text{{User Query}}] \\; \\Vert \\; [\\text{{KQL Query}}]$$

*   **Trial Evaluation:** Out of 30 complex trial questions evaluated in a test sandbox database, **20 generated KQL queries executed successfully** on the first turn without syntax adjustments.

![]({resume_imgs[0]})
"""

with open(r"f:\agent_learning\beautified_notion\resume_portfolio_details.md", "w", encoding="utf-8") as f:
    f.write(resume_md)


# Draft 10: Structuring Prompts for Large AI Agent Workflows
structuring_prompts_md = f"""# 📐 Structural Prompt Design: Workflows vs. Autonomous Agents

This guide reviews prompt engineering frameworks, design taxonomies, and orchestration patterns for building robust, scalable multi-agent systems.

---

## 🗺️ 1. Conceptual Framework: Workflows vs. Agents

| System Archetype | Definition | Control Design | Best Use Cases |
| :--- | :--- | :--- | :--- |
| **Agentic Workflow** | LLM-based tools orchestrated through **predefined code paths** and deterministic routing logic. | Direct programmatic control (predictable state transitions). | Structured, high-precision tasks (e.g., incident capacity root-cause summaries). |
| **Autonomous Agent** | A system where LLMs **self-direct their execution paths**, dynamically deciding which tools to select. | Agent-driven autonomy (state transitions decided at runtime by the model). | Vague, open-ended research tasks (e.g., code debugging, open-domain web searches). |

---

## 🛠️ 2. Architectural Design Patterns

Modern multi-agent architectures avoid monolithic prompts, instead decomposing tasks into modular patterns to minimize error accumulation.

```mermaid
graph TD
    Patterns[Orchestration Patterns] --> Chaining[1. Prompt Chaining]
    Patterns --> Routing[2. Prompt Routing]
    Patterns --> EvOpt[3. Evaluator-Optimizer Grid]
    
    Chaining --> ChainFlow[Divide task into sequential sub-calls with validation gates]
    Routing --> RouteFlow[Classifier routes queries to specialized sub-agents]
    EvOpt --> EvOptFlow[Generator drafts outputs; Critic provides feedback loops]
```

### 2.1 Prompt Chaining
Instead of passing a long, multi-step instruction list to a single prompt, **Prompt Chaining** divides the pipeline into a sequence of simpler LLM calls.

*   **When to use:** Ideal for tasks with clear, sequential steps.
*   **The Trade-off:** Slightly increases overall execution latency in exchange for **high output reliability**, as each individual step performs a simpler, targeted task.

![]({prompt_struct_imgs[0]})

### 2.2 Prompt Routing
**Routing** uses an initial classifier module (which can be a fast, smaller LLM or a rule-based keyword match) to analyze incoming queries and forward them to specialized sub-agents.

*   **Key Advantage:** Prevents context pollution. Each specialist agent is loaded only with the system instructions, schemas, and tools needed for its specific task.

---

## 📈 3. Multi-Agent Systems Integration

When scaling past individual prompts, multi-agent orchestrations utilize dedicated central abstractions:
1.  **Define Structured Problem Spaces:** Give each agent a specialized, narrow role with clear constraints rather than a general-purpose instruction set.
2.  **Just-In-Time Context Injection:** Pass schemas, database descriptions, and RAG documents to agents only when active to prevent context distraction.
3.  **Dynamic Task Handoffs:** Use standardized tool interfaces (like OpenAI's Handoff SDK) to programmatically transfer execution control between active agents.
"""

with open(r"f:\agent_learning\beautified_notion\prompt_engineering_structures.md", "w", encoding="utf-8") as f:
    f.write(structuring_prompts_md)


# Draft 11: Investigating Sonnet 4.5’s Roadmap Execution Failure
sonnet_fail_md = f"""# 🕵️ Post-Mortem Engineering Report: Agent Roadmap Compliance Outage

This post-mortem analyzes an execution failure where an agent model (running Sonnet 4.5 in early 2026) bypassed structured execution steps defined in our incident routing roadmap.

---

## 📋 1. Incident Overview & Expected vs. Observed Actions

The **Capacity Analysis Roadmap** specifies a strict, stepwise execution protocol to ensure predictability, auditability, and safety:

```text
  [Step 0: Extract Metadata]  ── (Outputs JSON containing parsed alerts)
              │
              ▼
  [Step 1: Construct Query]   ── (Outputs JSON containing KQL / variables)
              │
              ▼
  [Step 2: Execute Telemetry] ── (Executes query via fabric-rti-mcp)
              │
              ▼
  [Step 3: Analyze & Route]   ── (Verifies capacity variance; routes next steps)
```

### 🚨 Observed Failure Behavior
Instead of outputting the **Step 0–3 JSON state configurations in sequence**, the agent bypassed the structured roadmap entirely. It jumped directly to deep, unstructured tenant-level investigations, executing raw tool queries without generating the required intermediate state configuration artifacts. 

This bypassed crucial routing gates (such as confirming whether the variance was a telemetry error versus active physical provisioning) and resulted in a **non-compliant, un-auditable execution trace**.

---

## 🔬 2. Technical Root Cause Analysis

We identified three factors that contributed to this compliance failure:

### 2.1 Instruction Adherence in Deep Attention Windows
While models like Sonnet 4.5 feature deep context windows and strong contextual reasoning, evaluations indicate that they occasionally **ignore implicit rules and structural guidelines** in complex, multi-turn prompts. The model bypassed the "pause and generate intermediate state configuration" rule, prioritizing direct task completion over compliant generation.

### 2.2 Parallel & Non-Sequential Execution Bias
Sonnet 4.5 is optimized to find efficient task completion paths, giving it a natural bias toward **parallelizing and overlapping actions**. Rather than executing strictly sequentially (finish Step A, output status, then start Step B), the model attempted to complete the entire diagnostic analysis in a single pass to minimize context window loops.

### 2.3 Context Window Saturation
As context windows grow and are loaded with dense database schemas and long execution traces, deep structural instructions (like *"You must stop and output Step N JSON before invoking tool X"*) can suffer from **Attention Degradation**.

---

## 🛡️ 3. Corrective Mitigation Action Plan

To systematically enforce execution compliance, we will implement several structural controls:

```mermaid
graph TD
    UserQ[User Question] --> MatchStep[1. Load Current Step Constraints]
    MatchStep --> LLMCall[2. LLM Generation Block]
    LLMCall --> CheckJSON[3. Structural JSON Validator Gate]
    CheckJSON -->|Valid JSON| Proceed[4. Unlock Next Step Tools]
    CheckJSON -->|Invalid / Skipped| Block[5. Strict Execution Block & Re-Prompt]
```

### 3.1 Structural Controls
*   **Enforce Gated Step-Tokens:**
    Modify the orchestrator runtime so that tools for subsequent stages (such as the Kusto execution tool) are **completely hidden and disabled** until the agent outputs a valid state configuration JSON for the current step.
*   **Implement Strict Format Validation Gates:**
    Pass the agent's output through an automated JSON schema validator at each step. If validation fails or is bypassed, halt execution and automatically re-prompt the agent with a targeted correction instruction.
*   **Segment Prompt Contexts dynamically:**
    Rather than loading the entire roadmap into the initial prompt, partition instructions and serve them iteratively step-by-step.
"""

with open(r"f:\agent_learning\beautified_notion\sonnet_execution_failure.md", "w", encoding="utf-8") as f:
    f.write(sonnet_fail_md)


# Draft 12: Microsoft Benefits
benefits_md = f"""# 🏥 Microsoft Employee Benefits & Quick-Links Directory

This dashboard organizes quick-links, portals, and essential resources for Microsoft employee benefits, healthcare schedules, and internal work policies.

---

## 🔗 1. Quick-Link Portal Directory

| Benefit Context | Primary Gateway | Purpose |
| :--- | :--- | :--- |
| **Benefits Enrollment** | [aka.ms/benefitsenroll](https://aka.ms/benefitsenroll) | Annual benefits selection and coverage updates. |
| **Flexible Work Policy** | [aka.ms/flexibilityatmicrosoft](https://aka.ms/flexibilityatmicrosoft) | Core guidelines and templates for flexible schedules. |
| **Worksite & Hour Changes** | [aka.ms/ec](https://aka.ms/ec) | Employee Central portal to adjust contract hours or worksites. |

---

## ⚕️ 2. Core Coverage Portals

### 2.1 Health & Welfare Portals
Review coverage options, manage claims, and update savings allocations through our primary benefit gateways:

![]({benefits_imgs[0]})
![]({benefits_imgs[1]})

*   **Health Savings Account (HSA):**
    Allows pre-tax contributions to cover eligible medical, dental, and vision expenses.
*   **Employee Assistance Program (EAP):**
    Provides free, confidential counseling and mental health support services.
"""

with open(r"f:\agent_learning\beautified_notion\microsoft_benefits_directory.md", "w", encoding="utf-8") as f:
    f.write(benefits_md)

print("All BEAUTIFIED markdown files successfully written!")
