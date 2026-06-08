# Course spec — Quantization (for agentic post-training AI engineer interviews)

## Target outcome
A learner who completes this course can explain, derive, implement, and make production
tradeoffs for LLM quantization, and is ready to be interviewed as an **agentic
post-training AI engineer**. Scope is limited strictly to **quantization** (and the parts
of post-training/serving that directly touch it). Do not drift into general fine-tuning,
RLHF, or unrelated inference topics beyond what quantization requires.

## Scope & leveling (defines "good enough" so the build converges)
- **Target level:** mid-level / **L2 / Applied Scientist II / Member of Technical Staff** at
  a frontier lab (Microsoft AI, Google DeepMind, OpenAI, Anthropic, Meta). The course must be
  *sufficient to interview at this level*, not exhaustive. Tier definitions + convergence
  rules live in `RUBRIC.md`; only **T1/T2** gaps may block a module.
- **T1 Core (must master, hands-on):** affine map + number formats + granularity +
  calibration + PTQ/QAT (M0); GPTQ (M1); AWQ + the contested GPTQ-vs-AWQ framing (M2);
  LLM.int8() + SmoothQuant outlier handling (M3); NF4/QLoRA + GGUF/K-quants basics (M4);
  FP8 + the W4A16/W8A8/FP8 deployment decision + tooling map/deprecations (M6 + M8);
  the quantize-and-still-tool-calls capstone (M8).
- **T2 Frontier-awareness (must discuss correctly; small from-scratch demo suffices):**
  rotation/incoherence & computational invariance — QuaRot + SpinQuant (M5); MXFP4/NVFP4
  microscaling + gpt-oss / DeepSeek-V3 FP8-training framing (M6); KV-cache quant — KIVI
  (keys per-channel, values per-token) (M7); BitNet b1.58 ternary as a concept (M7).
- **T3 Optional / advanced (one-line "going deeper" pointer + citation only — do NOT
  implement):** QuIP#/QTIP trellis-coded-quantization decoder internals & E8-lattice
  optimality proofs; AQLM codebook joint-optimization details; i-quant importance-matrix
  internals; DeepSeek FP8 FP32-accumulation micro-details; OmniQuant/HQQ; MXFP4 *training*
  (Quartet).
- **T4 Intentionally out of scope (excluded on purpose):** writing production CUDA/Triton
  kernels for these methods; designing a *novel* quantization algorithm; non-LLM / vision-CNN
  quantization specifics; Tensor-Core microarchitecture / RTL; large-scale training infra;
  an exhaustive survey of every method named in `guide.md` beyond these modules. Each is
  recorded once in the `PROGRESS.md` ledger and not revisited.

## Source of truth
- Primary content source and depth target: [../guide.md](../guide.md).
- Treat its rankings, mechanisms, citations, and "Probes" as the canonical outline. Every
  method, number, and arXiv id used in the notebooks should trace back to it (or a primary
  source it points to).

## Environment contract
- Notebooks live in `Quantization/course/notebooks/` and MUST run top-to-bottom on the
  Windows `.venv` kernel (RTX 5090 / Blackwell `sm_120`, 32 GB; PyTorch 2.11 + CUDA 12.8).
- Installed and usable: transformers, accelerate, peft, trl, optimum, bitsandbytes (4-bit
  works on GPU), datasets, gguf, llama-cpp-python (CUDA build), safetensors, scipy,
  matplotlib, numpy. Local models: `LLM_model_weights/Qwen3-1.7B` (use for live demos),
  `Qwen3-14B`, `gemma-4-12B-it`.
- Blackwell is FP8-native (`torch.float8_e4m3fn` / `e5m2`) — use it for the FP8 module.
- WSL-only (do NOT use in the graded path): vLLM, flash-attention, Docker harnesses
  (SWE-bench / Terminal-Bench execution). Reference them conceptually only.
- If a method's real tooling won't install/run here (e.g. GPTQModel/AutoAWQ on Blackwell
  Windows, QuaRot/QuIP# kernels), implement the **core mechanism from scratch in PyTorch**
  on a small tensor/model and label it clearly. The idea must still be demonstrated live.

## Pedagogical rules (every module)
- Learning objectives + prerequisites up top.
- Intuition → math (KaTeX) → implementation (real or from-scratch) → a measurement
  (perplexity / VRAM / latency / MSE) in a table or plot → "Interview drill" (5–8 Q&A) →
  one "Depth story" → pointer to next module.
- Cite primary sources (arXiv id / official doc) for every named method and number, with
  the source's context (model + hardware) when quoting a figure.
- Keep demos cheap: prefer Qwen3-1.7B and small tensors; guard heavy/optional cells behind
  a `RUN_HEAVY = False` style flag near the top.

## Modules

| # | Notebook | Must cover (concepts + interview probes) | Hands-on (runs on this machine) |
|---|----------|------------------------------------------|---------------------------------|
| 0 | `00_foundations.ipynb` | Affine map `x_q=round(x/s)+z`; FP32/FP16/BF16/FP8/INT8/INT4/NF4; symmetric vs asymmetric; granularity (per-tensor/channel/group); calibration (static vs dynamic); PTQ vs QAT; memory-bound vs compute-bound; W4A16 vs W8A8 vs FP8. Probes: quantize a matrix end-to-end; why per-group beats per-tensor; why BF16 over FP16; why activations are harder than weights. | Implement quantize/dequantize from scratch (sym+asym); MSE vs granularity on a matrix with outlier channels; BF16 vs FP16 dynamic-range overflow; FP8 cast on the 5090; NF4 non-uniform grid; static vs dynamic activation quant; model-size estimator; peek at a real Qwen3 weight tensor. |
| 1 | `01_gptq.ipynb` | GPTQ = layer-wise Hessian-based error-compensating weight PTQ; OBQ/OBS lineage; `H=2XXᵀ+λI` is input covariance (one forward pass, no labels); fixed-order quantization + Cholesky inverse-Hessian; block updates; group size; W4A16. Probes: why the Hessian; how computed cheaply; OBQ→GPTQ speedup; why 3–4-bit works but 2-bit degrades. (Frantar et al., arXiv:2210.17323) | From-scratch GPTQ on one Linear layer (compute H from activations, quantize column-by-column with error compensation), compare reconstruction error vs round-to-nearest; if GPTQModel installs cleanly, quantize Qwen3-1.7B W4A16 and measure perplexity + VRAM, else keep the from-scratch demo. |
| 2 | `02_awq.ipynb` | AWQ = activation-aware weight-only PTQ; ~0.1–1% salient channels identified by **activation** magnitude; equivalent per-channel scaling instead of mixed precision; no backprop/reconstruction. GPTQ vs AWQ is contested/benchmark-dependent (arXiv:2411.02355: small gap on academic benchmarks, GPTQ edge on generative tasks for Llama-3.1 W4A16). Probes: why look at activations to find important weights; scaling vs keeping FP16 outliers; AWQ vs GPTQ. (Lin et al., arXiv:2306.00978) | From-scratch AWQ: find salient channels via activation stats, apply per-channel scale search, show error drop vs naive RTN; tabulate GPTQ-vs-AWQ tradeoff. |
| 3 | `03_outliers_int8_smoothquant.ipynb` | The outlier arc: LLM.int8() emergent features (~0.1% of dims at ~6.7B) + mixed-precision decomposition (accurate but often slower than FP16); SmoothQuant migrates activation difficulty to weights via `diag(s)`, α default 0.5, enables real W8A8 speedups. Probes: what/where are emergent features; why LLM.int8() is slow; migration direction & validity; α tradeoff; W8A8 (compute-bound) vs W4A16 (memory-bound). (Dettmers arXiv:2208.07339; Xiao arXiv:2211.10438) | Visualize activation outlier channels in Qwen3-1.7B; bitsandbytes INT8 load + generate; from-scratch SmoothQuant scaling on a Linear, sweep α, show activation/weight error tradeoff. |
| 4 | `04_gguf_nf4_qlora.ipynb` | GGUF format + K-quants (super-blocks, Q4_K_M default) + i-quants (importance-matrix); when GGUF over GPTQ/AWQ (CPU/edge/offload). NF4 (quantile grid optimal for Gaussian), double quantization, paged optimizers, QLoRA (NF4 base + BF16 LoRA), storage vs compute dtype. Probes: block-wise scales; legacy vs K vs i-quants; why NF4 is information-optimal; double quant; why finetune adapters not quantized weights. (Dettmers arXiv:2305.14314) | Quantize a model to GGUF Q4_K_M with llama.cpp/gguf + run via llama-cpp-python on GPU; load Qwen3-1.7B in NF4 (bitsandbytes) and attach a tiny LoRA adapter (peft), show it trains a step; compare NF4 vs FP4 reconstruction. |
| 5 | `05_rotation_quarot_spinquant.ipynb` | Rotation/incoherence: computational invariance (orthogonal transform leaves output unchanged); Hadamard/random rotations spread outlier energy → near-Gaussian → 4-bit-friendly; QuaRot (random Hadamard, W4A4 incl. KV); SpinQuant (learned rotations via Cayley/Stiefel, beats random by up to ~16 pts); production (SpinQuant in Meta on-device Llama 3.2; QuaRot in AMD Quark). Probes: why a rotation doesn't change output; why Hadamard reduces outliers; online vs fused; learned vs random. (QuaRot arXiv:2404.00456; SpinQuant arXiv:2405.16406) | From-scratch: build a random Hadamard matrix, rotate a weight/activation vector with outliers, show kurtosis/outlier drop and lower 4-bit MSE; verify output invariance `(xQ)(QᵀW)=xW`. |
| 6 | `06_fp8_mxfp4_nvfp4.ipynb` | Hardware-native low precision: FP8 E4M3 (precision) vs E5M2 (range), W8A8-FP effectively lossless; FP8 training (DeepSeek-V3: E4M3 everywhere, 1×128/128×128 tile/block scaling, periodic FP32 accumulation). Microscaling: MXFP4 (block 32, E8M0 scale) vs NVFP4 (block 16, E4M3 scale), Blackwell-native; gpt-oss MoE weights in MXFP4 (~4.25 bpp). Probes: what is block floating point; MXFP4 vs NVFP4; why FP8 lossless but FP4 not; how DeepSeek keeps FP8 training stable. (DeepSeek-V3 arXiv:2412.19437; gpt-oss arXiv:2508.10925) | Real FP8 on the 5090: cast Qwen3 weights to `float8_e4m3fn`/`e5m2`, compare error and `finfo` ranges; from-scratch MXFP4 vs NVFP4 block quant (shared scale per block) with error vs block size; FP8 vs INT8 comparison. |
| 7 | `07_extreme_lowbit_kv_bitnet.ipynb` | Sub-4-bit + KV + QAT-at-scale: QuIP#/QTIP (incoherence + E8 lattice / trellis-coded quantization), AQLM (additive multi-codebook), 3-bit beating 4-bit; KV-cache quant — KIVI (keys per-channel, values per-token) & KVQuant; BitNet b1.58 ternary {−1,0,+1}≈1.58 bits, matmul→add/sub. Probes: scalar vs vector quant; why E8; incoherence; VQ vs TCQ scaling; why keys per-channel/values per-token; ternary QAT. (QuIP# arXiv:2402.04396; QTIP arXiv:2406.11235; AQLM arXiv:2401.06118; KIVI arXiv:2402.02750; BitNet arXiv:2402.17764) | From-scratch: scalar vs 2D vector-quantization codebook on weights (show VQ wins); KV-cache quant simulation comparing per-channel vs per-token on real attention K/V; a ternary BitLinear forward (STES). |
| 8 | `08_production_and_capstone.ipynb` | Format choice by deployment: FP8 ~lossless, INT8 1–3% drop, INT4 W4A16 competitive (arXiv:2411.02355, 500k+ evals); **W4A16 for sync/single-stream (memory-bound), W8A8 for async continuous batching (compute-bound)**. Tooling map + deprecations: AutoGPTQ archived Apr 2025 → GPTQModel; AutoAWQ deprecated May 2025 → vLLM llm-compressor; serving on vLLM/TensorRT-LLM(ModelOpt)/SGLang/llama.cpp; QuaRot in AMD Quark, SpinQuant via ExecuTorch. Probes: pick the method for a given deployment & defend it; end-to-end quantize-and-serve pipeline. | **Capstone:** quantize Qwen3-1.7B to 4-bit (NF4/bitsandbytes), then verify it still tool-calls correctly on a small sample from `datasets/BFCL_Berkeley-Function-Calling-Leaderboard` (or tau2), measuring answer validity + VRAM + latency vs the bf16 baseline; produce a one-page "which quantization when" decision table. |

## Capstone
Module 8 is the capstone: an end-to-end "quantize a real local model, prove it still does
the agentic task (tool-calling) acceptably, and quantify the quality/VRAM/latency tradeoff"
notebook, plus the production decision table. It must run on the Windows venv using the
already-downloaded BFCL/tau2 data and Qwen3-1.7B.

## Definition of done
- Modules 0–8 each reach `passed` under `RUBRIC.md` (all **T1/T2** material correct + hard
  gates green; open T3/T4 items are fine and live in the ledger).
- The interview-coverage pass (`interview-question-collector`) reports
  `INTERVIEW COVERAGE: SUFFICIENT` for the target level, or any remaining gaps are T3/T4.
- Whole-course review passes: ordering matches the outlier→rotation→hardware→extreme arc
  from `guide.md`, no T1/T2 gaps vs the guide's must-know methods, no duplicated derivations.
- `notebooks/README.md` lists the modules, the run order, and the one-line "what you'll be
  able to answer" for each (builder creates it in the final pass).
