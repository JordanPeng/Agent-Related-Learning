# 🎤 Oral Presentation: Literature Survey on Federated Fine-Tuning of LLMs

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

$$\min_{\Theta} \sum_{{i=1}}^{{B}} \mathcal{{L}}_i(W_0 + \Delta W( \theta_i )) \quad \text{{s.t.}} \quad \text{{VRAM}}(\theta_i, b_i) \le \text{{GPU\_Cap}}_i$$

*   Where $\theta_i$ represents the allocated adapter parameters (rank, position) and $b_i$ is the custom batch size for client $i$.

### ⚙️ How FedPipe Works under the Hood
1.  **Iterative Layer Profiling via SVD:**
    Instead of training arbitrary layers, FedPipe uses Singular Value Decomposition (SVD) on weight matrices, assigning adapters to the most information-dense dimensions:
    
    $$W = U \Sigma V^T$$
    
    Weight layers are ranked by the magnitude of their singular values ($\Sigma$), prioritizing high-variance layers for adaptation.
2.  **Adaptive Resource Partitioning:**
    *   *Batch Size:* Scaled proportionally to the node's relative compute capacity, ensuring it stays within a safe, configured VRAM threshold.
    *   *Elastic Ranks:* Clients assign adaptive ranks (e.g., $r=4$ for low-VRAM nodes, $r=16$ for high-VRAM nodes). The global server aggregates these variable-rank matrices by projecting them into a unified low-rank subspace before redistributing them.

---

## 🏁 4. Slide Summary & Future Directions (14:00 - 15:00)

*   **Key Presentation Takeaway:**
    > *"Through methods like SVD projection and adaptive local parameter allocation, we can successfully run federated fine-tuning across highly diverse network environments."*
*   **Future Frontiers:** Highlight Asynchronous Parameter Consolidation to eliminate waiting on slower clients (stragglers), and integrating differential privacy natively inside adapter spaces.
