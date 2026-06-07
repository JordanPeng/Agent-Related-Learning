## TL;DR

- **Master GPTQ, AWQ, the number-format/granularity fundamentals (INT8/INT4/FP16/BF16/FP8, symmetric vs asymmetric, per-tensor/channel/group), PTQ vs QAT, LLM.int8(), SmoothQuant, GGUF/K-quants, and NF4/QLoRA first** — these are table-stakes that come up in essentially every post-training or inference-systems interview.
- **For the advanced tier, the three highest-leverage methods to know cold are (1) rotation/incoherence methods (QuaRot + SpinQuant), (2) hardware-native low precision (FP8 and MXFP4/NVFP4 microscaling, as used in DeepSeek-V3 and gpt-oss), and (3) extreme low-bit codebook/vector quantization (QuIP#/QTIP and AQLM)** — plus KV-cache quantization (KIVI/KVQuant) and BitNet b1.58 as strong differentiators.
- **For harness-engineering and post-training roles at frontier labs, the interviewer is most likely to probe the why-it-works mechanisms (Hessian error compensation, activation-aware scaling, outlier handling, Hadamard rotations/incoherence, codebooks) and production tradeoffs (W4A16 vs W8A8 vs FP8, vLLM/TensorRT-LLM/llama.cpp support).** Tooling has moved: AutoGPTQ and AutoAWQ are both archived/deprecated as of 2025; GPTQModel and vLLM's llm-compressor are the current paths.

---

## Key Findings

1. **Two competing axes structure the whole field.** (a) *What you quantize*: weight-only (W4A16 — memory/bandwidth bound, dominant for single-stream/local) vs weight+activation (W8A8/W4A4 — compute bound, dominant for high-throughput batched serving). (b) *How you fight outliers*: keep them in higher precision (LLM.int8()), migrate them (SmoothQuant), protect salient channels (AWQ), or rotate them away (QuaRot/SpinQuant). Nearly every method is best understood as an answer to the activation/weight outlier problem.
2. **GPTQ and AWQ remain the two must-know PTQ algorithms.** GPTQ = layer-wise, Hessian-based (Optimal Brain Quantization lineage) error-compensating weight quantization. AWQ = activation-aware per-channel scaling to protect the ~1% salient weight channels. Empirically they are close: the Red Hat/Neural Magic study *"Give Me BF16 or Give Me Death? Accuracy-Performance Trade-Offs in LLM Quantization"* (Kurtic et al., arXiv:2411.02355, ACL 2025) found "a small gap between methods on academic benchmarks but a more pronounced difference in favor of GPTQ on" real-world generative tasks (Arena-Hard, HumanEval, MBPP) for Llama-3.1-Instruct W4A16. Know both, and present the comparison as genuinely contested and benchmark-dependent.
3. **Hardware-native low precision is the biggest 2024–2026 shift.** FP8 (E4M3/E5M2) is effectively lossless for W8A8 inference and is now used for *training* (DeepSeek-V3 trained natively in FP8). MXFP4/NVFP4 microscaling 4-bit formats are native on NVIDIA Blackwell, and OpenAI's gpt-oss shipped with MoE weights natively in MXFP4. This is the single most "current" topic and a strong signal of awareness.
4. **Rotation/incoherence is the dominant idea in cutting-edge PTQ.** QuaRot (Hadamard rotations), SpinQuant (learned rotations), and QuIP#/QTIP (incoherence + codebooks) all exploit the same insight: an orthogonal/rotation transform that is computationally invariant can spread outliers across dimensions, making weights and activations near-Gaussian and easy to quantize to 4 bits or below.
5. **Tooling has consolidated and shifted.** AutoGPTQ was archived April 11, 2025 (→ GPTQModel); AutoAWQ was archived/deprecated May 2025 (→ vLLM llm-compressor). Production serving runs on vLLM (llm-compressor/compressed-tensors), TensorRT-LLM (NVIDIA ModelOpt), SGLang, and llama.cpp/GGUF. SpinQuant and QuaRot have reached production: SpinQuant ships in Meta's quantized on-device Llama models via ExecuTorch; QuaRot is built into AMD Quark.

---

## Details

### GROUP 1 — Basic & Popular Methods (ranked by interview probability)

### Tier 0 — The fundamentals (asked in nearly every interview)

**What quantization is.** Mapping high-precision values (FP32/FP16/BF16) to a smaller set of low-precision values to cut memory, memory-bandwidth, and (when activations are also quantized) compute. The canonical affine map is `x_q = round(x/s) + z`, with scale `s` and zero-point `z`; dequantization is `x ≈ s·(x_q − z)`.

**Number formats.**

- **FP32/FP16/BF16**: BF16 keeps FP32's 8 exponent bits (same dynamic range) but only 7 mantissa bits — the default training/serving precision because it avoids overflow without loss scaling.
- **FP8**: two encodings, **E4M3** (4 exponent, 3 mantissa — more precision, less range; used for weights/activations and the forward pass) and **E5M2** (5 exponent, 2 mantissa — more range; used for gradients in the backward pass). E4M3 has lower mean-absolute-error than E5M2 for inference.
- **INT8 / INT4**: integer grids. INT8 W8A8 is near-lossless; INT4 is weight-only's sweet spot.
- **NF4**: 4-bit NormalFloat, a non-uniform quantile-based grid information-theoretically optimal for normally distributed weights.

**Symmetric vs asymmetric.** Symmetric uses a single scale, zero maps to 0 (no zero-point) — faster, hardware-friendly, standard for weights. Asymmetric adds a zero-point to handle skewed/one-sided distributions (e.g., post-ReLU activations) — more accurate for asymmetric ranges, slightly more compute.

**Granularity.** Per-tensor (one scale for the whole tensor — fastest, least accurate) → per-channel/per-row (one scale per output channel) → per-group (one scale per block of, e.g., 64 or 128 weights — the standard for 4-bit weight quantization, best accuracy/overhead tradeoff). Finer granularity better contains outlier damage at the cost of more scale storage.

**Calibration.** Running a small representative dataset through the model to collect activation statistics (ranges, Hessians, salient channels) used to set scales/clip thresholds. Static (offline, fixed scales) vs dynamic (computed at runtime per token — more accurate for activations, what makes W8A8-FP "lossless").

**PTQ vs QAT.** PTQ quantizes a trained model with little/no retraining (GPTQ, AWQ, SmoothQuant — minutes to hours). QAT simulates quantization during training/fine-tuning with a straight-through estimator so weights adapt to low precision (BitNet, LLM-QAT, gpt-oss QAT recovery) — best accuracy at extreme bit-widths but expensive. An interviewer will expect you to say PTQ is default for LLMs because retraining is costly, and QAT is reserved for sub-4-bit or when PTQ accuracy is insufficient.

> **Probes:** Walk through quantizing one weight matrix end-to-end. Why does per-group beat per-tensor? Why is BF16 preferred over FP16 for training? When asymmetric over symmetric? Why are activations harder to quantize than weights? (Answer: systematic outlier channels.)
> 

---

### Tier 1 — Must-know algorithms

**1. GPTQ (Frantar et al., 2022) — highest probability.** Weight-only PTQ (typically W4A16, group size 128). Builds on Optimal Brain Quantization/Optimal Brain Surgeon: minimizes the layer reconstruction error `‖WX − ŴX‖²` and, after quantizing each weight (column), updates the remaining not-yet-quantized weights to compensate, using approximate second-order (Hessian) information `H = 2XXᵀ + λI`. Key tricks: the Hessian is just the input covariance (one forward pass, no labels/backprop); quantize in fixed column order (order doesn't matter at LLM scale); Cholesky decomposition for a numerically stable inverse-Hessian; block-wise updates for speed. Compresses to 3–4 bits with ~1–2% accuracy loss.

> *Probes:* Why use the Hessian? How is it computed cheaply? What is the OBQ→GPTQ speedup insight (fixed-order + Cholesky)? Why does it work for 3–4-bit but degrade at 2-bit without smaller groups?
> 

**2. AWQ (Lin et al., 2023, MLSys 2024 best paper) — co-highest probability.** Weight-only PTQ. Insight: not all weights matter equally — protecting just ~0.1–1% of *salient* weight channels dramatically reduces error, and saliency is identified by *activation* magnitude, not weight magnitude. To avoid hardware-unfriendly mixed precision, AWQ instead applies an equivalent per-channel scaling transform: scale up salient channels (giving them finer effective resolution) and inversely scale activations, mathematically preserving the output. No backprop/reconstruction, so it generalizes across domains and doesn't overfit the calibration set.

> *Probes:* Why look at activations to find important weights? Why scaling instead of keeping outliers in FP16? How is AWQ different from GPTQ (no Hessian/sequential updates)? Tradeoff of the scaling hyperparameter search.
> 

**3. LLM.int8() / bitsandbytes (Dettmers et al., 2022).** The foundational outlier paper. At ~6.7B parameters, systematic **emergent outlier features** appear in a few hidden dimensions (~0.1% of features) that dominate predictive performance — zeroing them tanks the model. LLM.int8() uses vector-wise (per-row/per-column) INT8 quantization plus **mixed-precision decomposition**: the ~6 outlier feature dimensions go through a 16-bit matmul, the other 99.9% through INT8, then results combine. Preserves accuracy but is often *slower* than FP16 (the decomposition is hardware-inefficient). bitsandbytes also provides the 4-bit NF4 path.

> *Probes:* What are emergent features and at what scale do they appear? Why is LLM.int8() accurate but slow? Contrast its outlier handling with SmoothQuant's and QuaRot's.
> 

**4. SmoothQuant (Xiao et al., 2023).** Enables W8A8 (both weights and activations in INT8). Insight: activations have outliers and are hard to quantize; weights are easy. SmoothQuant **migrates the difficulty** via a mathematically equivalent per-channel scaling transform `diag(s)`: divide activations by `s`, multiply weights by `s`, controlled by a smoothing-strength hyperparameter α (default 0.5; higher α pushes more difficulty to weights). Unlike LLM.int8(), it yields real speedups (up to ~1.56×) because all matmuls stay INT8.

> *Probes:* Direction of migration and why it's valid. How α trades weight vs activation difficulty. Why W8A8 matters for throughput (compute-bound) vs W4A16 (memory-bound).
> 

**5. GGUF / GGML + K-quants (llama.cpp).** GGUF is the file format (successor to GGML) that packages quantized weights + metadata for memory-mapped, mostly-CPU/edge inference. Quantization families: legacy (Q4_0, Q5_1 …), **K-quants** (Q2_K…Q6_K — super-blocks with hierarchical scales; Q4_K_M is the de facto default), and **i-quants** (IQ2/IQ3 — importance-matrix-guided, vector-quantization-style, better at sub-4-bit). The "_K_M" naming = K-quant, Medium. Hugely important for the local-LLM ecosystem.

> *Probes:* Why block-wise scales? What's the difference between legacy, K-, and i-quants? When would you pick GGUF over GPTQ/AWQ? (Answer: CPU/edge/offload; GPTQ/AWQ aren't CPU-optimized.)
> 

**6. NF4 / QLoRA (Dettmers et al., 2023).** QLoRA = finetune a frozen NF4-quantized base model with LoRA adapters in BF16, enabling 65B finetuning on one 48GB GPU. Three innovations: **NF4** (4-bit NormalFloat, quantile grid optimal for Gaussian weights), **double quantization** (quantize the quantization constants for ~0.37–0.5 extra bits/param savings), **paged optimizers** (NVIDIA unified memory to survive gradient-checkpointing spikes). NF4 matches BF16 finetuning quality and beats FP4.

> *Probes:* Why is NF4 information-theoretically optimal? What is double quantization? Why does QLoRA finetune adapters rather than the quantized weights? Compute dtype vs storage dtype distinction.
> 

---

### GROUP 2 — Advanced Methods (ranked by interview probability)

I evaluated the full candidate list and selected the highest-relevance clusters. The ranking reflects what a frontier-lab post-training/harness interviewer is most likely to probe in 2025–2026.

### #1 (most likely) — Rotation / Incoherence methods: QuaRot + SpinQuant

These are *the* current frontier-PTQ idea and the most-cited 2024–2025 advanced methods.

**QuaRot (Ashkboos et al., NeurIPS 2024; arXiv:2404.00456).** Uses **randomized Hadamard transforms** fused into weight matrices to achieve **computational invariance** (rotating hidden states without changing the output), which eliminates outlier features and makes activations near-Gaussian. This enables true end-to-end 4-bit — *all* weights, activations, AND KV cache in INT4 — with no channels kept in higher precision. Online Hadamard transforms in the attention block let the KV cache be quantized too. Per the paper: "Our 4-bit quantized LLaMa2-70B model has losses of at most 0.47 WikiText-2 perplexity and retains 99% of the zero-shot performance," with a **2.16× prefill speedup** on RTX 3090 GPUs and **up to 3.39× memory saving during decoding**; 6/8-bit are lossless with simple round-to-nearest.

**SpinQuant (Liu et al., Meta, ICLR 2025; arXiv:2405.16406).** Same rotation insight, but the rotation matrices R1/R2 are **learned** via Cayley optimization on the Stiefel manifold (orthonormal constraint) on a small calibration set, plus online Hadamard rotations R3/R4 for KV-cache/activation outliers. Learned rotations beat random ones by up to ~16 points. Verbatim: "SpinQuant attains an average accuracy of 64.0 in extreme W4A4KV4 [quantization on Llama-2-7B]... a mere 2.9 point gap from the full-precision network... the previous LLM-QAT approach... exhibited a 22.0 point gap under identical precision conditions." Takes ~1.3 hours / 100 iterations on one A100 node for a 7B model.

**Production status:** SpinQuant ships in Meta's official quantized on-device **Llama 3.2 1B/3B** models (alongside a QAT+LoRA variant) and runs via **PyTorch ExecuTorch** with Arm KleidiAI kernels on phones. **QuaRot** is built into **AMD Quark** (`--pre_quantization_optimization quarot`) and the LLMC toolkit. vLLM's llm-compressor supports "QuIP and SpinQuant-style transforms."

> *Probes:* What is computational/rotation invariance and why doesn't a rotation change the output? Why does a Hadamard/random orthogonal transform reduce outliers? (Spreads concentrated energy across all dimensions → near-Gaussian → easy to quantize.) Online vs offline (fused) rotations. Why learned (SpinQuant) beats random (QuaRot)?
> 

### #2 — Hardware-native low precision: FP8 and MXFP4 / NVFP4 microscaling

Most "current-events" relevant; signals you track real frontier deployment.

**FP8.** W8A8-FP is essentially lossless across model scales (dynamic per-token activation quant + RTN symmetric weights). Native on Hopper/Ada and later. The bigger story: **FP8 training**. DeepSeek-V3 was trained natively in FP8 using E4M3 on all tensors (departing from the E4M3-forward/E5M2-backward hybrid) plus **fine-grained quantization** — 1×128 tile scaling for activations, 128×128 block scaling for weights — and periodic FP32 accumulation (every 4th MMA promoted to an FP32 master accumulator) to fight the ~14-bit Tensor Core accumulation limit.

**MXFP4 / NVFP4 (microscaling).** OCP Microscaling format: a block of (32 for MXFP4, 16 for NVFP4) FP4 (E2M1) elements shares one scale (E8M0 power-of-two for MXFP4; E4M3 for NVFP4). Native on **Blackwell** Tensor Cores (~2× FP8, ~4× BF16 throughput). **OpenAI's gpt-oss** (model card, arXiv:2508.10925) states: "The models were post-trained with MXFP4 quantization of the MoE weights, making gpt-oss-120b run on a single 80GB GPU (like NVIDIA H100 or AMD MI300X) and the gpt-oss-20b model run within 16GB of memory" — MoE weights at ~4.25 bits/param, the dominant share of total parameters, and an industry first for a frontier-grade open model. Caveats from research: MXFP4's power-of-two scale induces error; NVFP4's tiny group size neutralizes some outlier-mitigation; the Quartet work shows native MXFP4 *training* can be near-lossless on Blackwell with Hadamard transforms.

> *Probes:* What is microscaling / block floating point? Difference between MXFP4 (E8M0 scale, block 32) and NVFP4 (E4M3 scale, block 16)? Why is FP8 lossless but FP4 not? How does DeepSeek keep FP8 *training* stable? Difference between per-tensor and block scaling.
> 

### #3 — Extreme low-bit codebook / vector quantization: QuIP# / QTIP and AQLM

The 2–3-bit frontier; "shows deep expertise."

**QuIP# (Tseng et al., ICML 2024; arXiv:2402.04396).** Weight-only PTQ at 2–3 bits via three pieces: (1) **incoherence processing** with the Randomized Hadamard Transform (makes weights approximately Gaussian — principled outlier suppression); (2) **lattice codebooks** based on the **E8 lattice** (optimal 8-dimensional sphere packing, hardware-friendly vector quantization); (3) inter-layer fine-tuning. First method where 3-bit models scale better than (theoretically lossless) 4-bit — directly refuting the "4-bit is optimal" claim.

**QTIP (Tseng et al., NeurIPS 2024 Spotlight; arXiv:2406.11235)** — the successor. Keeps incoherence processing but replaces vector quantization with **trellis-coded quantization (TCQ)**: a stateful "bitshift trellis" decoder whose cost is *linear* (not exponential) in dimension, so it can quantize in dimensions >100 vs VQ's practical limit of ≤8. Uses lookup-free "computed" codes (1MAD, 3INST) and a 2KiB L1-cache-resident codebook. Beats QuIP# and AQLM in quality at the same throughput; released a Llama 3.1 405B Instruct quant.

**AQLM (Egiazarian et al., ICML 2024; arXiv:2401.06118).** Adapts classic **Additive Quantization / Multi-Codebook Quantization** from information retrieval: each weight group is represented as a *sum* of vectors selected from several learned codebooks, with codebooks jointly optimized across each transformer block. First scheme Pareto-optimal below 3 bits/param; strongest in the extreme 2-bit regime. Supported in HF Transformers/PEFT and SGLang.

> *Probes:* Scalar vs vector quantization. Why E8 lattice? What is incoherence processing and why does a Hadamard transform provide it? VQ vs TCQ codebook-size scaling. Why is 2-bit so much harder than 4-bit?
> 

### Strong differentiators (mention to show breadth)

**KV-cache quantization — KIVI / KVQuant.** For long-context/large-batch serving the KV cache becomes the memory + bandwidth bottleneck. **KIVI** (ICML 2024): a tuning-free 2-bit scheme using the key insight that the **key cache should be quantized per-channel** (it has outlier channels) while the **value cache is quantized per-token** (no channel outliers; per-token confines error and matches streaming append). ~2.6× less peak memory at near-lossless quality. **KVQuant** pushes to ~10M-token context on Llama-7B via per-channel pre-RoPE key quantization + attention-sink-aware handling. Highly relevant to harness/serving roles.

**BitNet b1.58 (Ma et al., 2024).** QAT, not PTQ: train from scratch with weights constrained to ternary {−1, 0, +1} (log₂3 ≈ **1.58 bits**) via a straight-through estimator on FP16 shadow weights and INT8 activations (BitLinear layers). Matmuls become add/subtract (no multiplies). For large enough models, matches FP16 perplexity, defining a new efficiency Pareto frontier; the 2B4T open model was trained on 4T tokens. The flagship "extreme QAT at scale" result — great for a forward-looking discussion.

**HQQ (Badri & Shaji, 2023).** Calibration-*free* PTQ that formulates rounding as a half-quadratic optimization minimizing *weight* (not activation) error, robust to outliers via a sparsity-promoting loss. Quantizes Llama-2-70B in <5 min (~50× faster than GPTQ), supports 1–8 bit, integrated in HF transformers + torchao/Marlin kernels. Good "fast, no calibration" contrast point.

**OmniQuant (Shao et al., ICLR 2024).** Bridges PTQ and QAT cheaply via two learnable, block-wise-optimized modules: **Learnable Weight Clipping** (learns clipping strength, not raw threshold) and **Learnable Equivalent Transformation** (learns SmoothQuant-style scales). A useful "learnable clipping/transformation" reference and a precursor to the rotation methods.

---

### Practical / Production Context (know this for systems-flavored interviews)

- **Format choice by deployment.** The Red Hat/Neural Magic study (arXiv:2411.02355), spanning over 500,000 evaluations, concluded: "(1) FP8 (W8A8-FP) is effectively lossless across all model scales, (2) well-tuned INT8 (W8A8-INT) achieves surprisingly low (1-3%) accuracy degradation, and (3) INT4 weight-only (W4A16-INT) is more competitive than expected." On deployment: "W4A16 is the most cost-efficient for synchronous setups, while W8A8 dominates in asynchronous continuous batching." Mental model: **W4A16** wins memory-bound single-stream/decoding on mid-tier GPUs; **W8A8** (INT8 or FP8) wins compute-bound high-throughput batched serving on high-end GPUs.
- **Tooling shifts (critical to state correctly):** **AutoGPTQ was archived April 11, 2025** ("This repository was archived by the owner on Apr 11, 2025. It is now read-only"; maintainers direct users to switch to GPTQModel as a drop-in replacement). **GPTQModel** is now HF Transformers' actively maintained GPTQ backend (adds asymmetric quant, faster/lower-memory, broad hardware). **AutoAWQ was deprecated/archived May 2025**; vLLM's docs state: "The AutoAWQ library is deprecated. This functionality has been adopted by the vLLM project in llm-compressor. For the recommended quantization workflow, please see the AWQ examples in llm-compressor."
- **Serving stacks:** **vLLM** (via llm-compressor + compressed-tensors) supports GPTQ(Model), AWQ, INT8 W8A8, FP8 W8A8, INT4 W4A16, NVFP4, and weight-only MXFP4 (as of vLLM v0.14.0; MXFP4 *activation* quant not yet supported for compressed-tensors models). **TensorRT-LLM via NVIDIA ModelOpt** supports SmoothQuant, AWQ (incl. W4A8), FP8, INT8, INT4, and NVFP4/MXFP4 for Blackwell. **SGLang** supports FP8, AWQ, GPTQ, INT8 W8A8, AQLM, GGUF, and NVFP4/MXFP4 via ModelOpt. **llama.cpp/GGUF** owns CPU/edge/local. **AMD Quark** offers AWQ, GPTQ, SmoothQuant, and QuaRot-style rotations and feeds vLLM on AMD GPUs.
- **2024–2026 trends:** (1) outlier handling has moved from "isolate" (LLM.int8()) → "migrate" (SmoothQuant) → "rotate away" (QuaRot/SpinQuant); (2) hardware-native FP8/FP4 is collapsing the line between training and inference precision; (3) sub-4-bit is now genuinely usable via codebooks/trellises (QuIP#/QTIP/AQLM); (4) KV-cache and attention quantization are first-class as context lengths explode; (5) QAT is making a comeback for FP4 accuracy recovery (gpt-oss, NVIDIA ModelOpt QAT→NVFP4).

---

## Recommendations (study plan, staged)

1. **Lock down Tier 0 + GPTQ + AWQ first (1–2 days).** Be able to derive the affine quant map, explain per-group scaling, and whiteboard GPTQ's Hessian update and AWQ's activation-aware scaling. These have the highest expected value. **Threshold to advance:** you can explain both algorithms' mechanisms without notes and articulate the GPTQ-vs-AWQ tradeoff.
2. **Add the outlier-handling trio + formats (1–2 days):** LLM.int8() → SmoothQuant → (preview) QuaRot as an evolution story; plus FP8 (E4M3/E5M2), NF4/QLoRA, GGUF/K-quants. **Threshold:** you can narrate "how the field fights activation outliers" as a single arc.
3. **Then the advanced tier in ranked order (2–3 days):** rotation methods (QuaRot/SpinQuant) → microscaling FP4 (MXFP4/NVFP4 + gpt-oss + DeepSeek FP8 training) → codebook/VQ (QuIP#/QTIP/AQLM). Add KIVI and BitNet b1.58 as differentiators. **Threshold:** you can pick the right method for a given deployment constraint and defend it.
4. **For harness/post-training roles specifically:** go one layer deeper on (a) W4A16 vs W8A8 vs FP8 serving tradeoffs and the memory-bound/compute-bound distinction, (b) KV-cache quantization, (c) the current tooling map (GPTQModel, llm-compressor, ModelOpt, vLLM/TensorRT-LLM/SGLang) — be able to say what you'd actually reach for and why. **Threshold:** you can describe an end-to-end "quantize-and-serve" pipeline for a specific model + hardware target.
5. **Have one or two "depth" stories ready** (e.g., why incoherence processing yields Gaussian weights; why DeepSeek needed FP32 accumulation in FP8 training) to demonstrate expertise beyond memorized summaries.

**What would change this ranking:** if the role is edge/on-device, push GGUF/K-quants, NF4, SpinQuant, and BitNet up. If it's pre-training/systems, push FP8 training and MXFP4 training (Quartet) up. If it's pure research, push QTIP/AQLM and the theory of incoherence up.

## Caveats

- **Interview-probability rankings are informed estimates, not measured data** — they reflect method prominence, citation/adoption, and the stated target roles, not a survey of actual interview questions. Treat them as a study-prioritization heuristic.
- **The GPTQ-vs-AWQ "which is better" question is genuinely contested** and benchmark-dependent; present it as a tradeoff, not a settled fact.
- **Tooling and framework-support details change fast** (version-gated features, deprecations). The states cited are as of early–mid 2026; verify current versions before relying on them.
- Some quantitative claims (specific perplexity/speedup numbers) come from individual papers' own reporting and may not replicate across models/hardware; where cited they are anchored to the source's own context (e.g., QuaRot's 2.16× prefill speedup is on RTX 3090).
- All core mechanisms and numbers are anchored to primary papers (arXiv) and official docs where possible; a few secondary summaries were used only for framing.