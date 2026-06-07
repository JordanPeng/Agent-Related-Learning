# 🧠 CMU Advanced NLP Fall 2024: Tool Use & LLM Agent Basics

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

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/b8a9d34c-832b-48fe-97ad-6ac19e46a7e1/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4ZH6VIX%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223844Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCzbLEodePF11ojb%2Bq6rpNLWAuBjZSQzhsFC7YuZpyllAIhALOQDki52Z4KzzFj75CFY2hwo1RqCENpmNd%2FUI9%2FZOz9KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzjMzu0DdaRNHv%2BbvEq3AONw2fffl%2BiMxN4H58PTqMtvvk%2FVqSyXGhTD332VElYzpASGreZk9OClxTz%2Bg7bF3F%2BJ1Hk%2BQTNl%2BGGW0ENtq4bph8CMpS1r4NrjwtuGrK7dQ30hPUNuzGiHuJTFAuMmtD9ATpYQRRQP8MUtAZYEaLjHWKo0uFn%2FLk4o8Y0Tm6AmyYJSePmx91QGyPT0%2FdvRg3OByyCxqXNRUm1VSwRkpcANqc%2BZPi7M8XGJKOT4EvVFnftBiMgFQuhQT4kVkyHI8o6HItOKSe3%2BpJ64VzZSBVp1XwzF44%2BJKXk9aR7a3%2FoF%2Fcbyd3UTUMdt9wFaP13sDUyHbgN%2FRf4aiOXp%2BNylzk%2BHoVXCGcj%2F5P8CJOsAuGC5sBwJSDbun%2FwD1%2FPNiFdoEOmN7Y%2B%2FfTdag%2FRj%2FbOk0WZZi8lSzQ6x7vI6mC%2B1RbvL2K0qAqnwErQDt1yQsU8u3nyiz%2F91l391ApU124ElOJ%2BiUzEAfHk7Lv8nvP%2FZ2rgHWC5m68RShTyvCLxEFLopkPszllpNVRrz28kbL3LfboNXvXYjRKlYxDzX7ZVHR2Ewsfro61UQRB3b%2Fk60G9iySfk5tU9U0vpKRwAvq4Fz%2Bxkq%2F6UW63b3m3u8lDeW%2FXLGdsS8JlwN5y5AuobJDDM15fRBjqkAeJShRcaARepbNdW%2Frrx7kbVJnNavG6cwIrztp%2FwZ45bquwTS5hRla6lPz1CdZ5n6RHETM1T52mUTz0%2BOrOankenJEBg4nqOWAadKKHek%2B%2FXmkduP7gKv84dtKCpgWQXHY85fxaSQJdqkKAY6hWl0GZ6lsa9PBYFa9zMNlBFYsW4l8n%2FXL2cDchMl3OD6Y4BUEgeL5ebwhzdC0%2BXeaXYgSL2D%2B0N&X-Amz-Signature=52ac6577069c6e3852dcc02bb6ed76e542a23386b2037eb45ce854d9796211e5&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

## 📊 3. 环境表示与信息理解 (Environment Representation)

在多 Agent 协同体系中，模型需要对环境、状态转换 and 感知深度建立清晰的数学 and 符号表示。

### 3.1 感知空间与世界模型
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/27d6bceb-73cf-4ba2-8da0-b8a940aabd06/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4ZH6VIX%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223844Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCzbLEodePF11ojb%2Bq6rpNLWAuBjZSQzhsFC7YuZpyllAIhALOQDki52Z4KzzFj75CFY2hwo1RqCENpmNd%2FUI9%2FZOz9KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzjMzu0DdaRNHv%2BbvEq3AONw2fffl%2BiMxN4H58PTqMtvvk%2FVqSyXGhTD332VElYzpASGreZk9OClxTz%2Bg7bF3F%2BJ1Hk%2BQTNl%2BGGW0ENtq4bph8CMpS1r4NrjwtuGrK7dQ30hPUNuzGiHuJTFAuMmtD9ATpYQRRQP8MUtAZYEaLjHWKo0uFn%2FLk4o8Y0Tm6AmyYJSePmx91QGyPT0%2FdvRg3OByyCxqXNRUm1VSwRkpcANqc%2BZPi7M8XGJKOT4EvVFnftBiMgFQuhQT4kVkyHI8o6HItOKSe3%2BpJ64VzZSBVp1XwzF44%2BJKXk9aR7a3%2FoF%2Fcbyd3UTUMdt9wFaP13sDUyHbgN%2FRf4aiOXp%2BNylzk%2BHoVXCGcj%2F5P8CJOsAuGC5sBwJSDbun%2FwD1%2FPNiFdoEOmN7Y%2B%2FfTdag%2FRj%2FbOk0WZZi8lSzQ6x7vI6mC%2B1RbvL2K0qAqnwErQDt1yQsU8u3nyiz%2F91l391ApU124ElOJ%2BiUzEAfHk7Lv8nvP%2FZ2rgHWC5m68RShTyvCLxEFLopkPszllpNVRrz28kbL3LfboNXvXYjRKlYxDzX7ZVHR2Ewsfro61UQRB3b%2Fk60G9iySfk5tU9U0vpKRwAvq4Fz%2Bxkq%2F6UW63b3m3u8lDeW%2FXLGdsS8JlwN5y5AuobJDDM15fRBjqkAeJShRcaARepbNdW%2Frrx7kbVJnNavG6cwIrztp%2FwZ45bquwTS5hRla6lPz1CdZ5n6RHETM1T52mUTz0%2BOrOankenJEBg4nqOWAadKKHek%2B%2FXmkduP7gKv84dtKCpgWQXHY85fxaSQJdqkKAY6hWl0GZ6lsa9PBYFa9zMNlBFYsW4l8n%2FXL2cDchMl3OD6Y4BUEgeL5ebwhzdC0%2BXeaXYgSL2D%2B0N&X-Amz-Signature=4c924024fcb2798b18c9777b748833e7f6cd6bbf774a4ecdf26a4da3cf36d1d8&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

大语言模型对世界/环境信息的理解可以建模为马尔可夫决策决策树，模型在当前状态 $S_t$ 下通过观察 $O_t$ 评估概率：

$$P(O_{t} \mid S_t) \quad \text{and} \quad P(S_{t+1} \mid S_t, A_t)$$

代理必须学习在长文本上下文中提炼最核心的状态编码，以便在后续链路重组时避免干扰。

### 3.2 探索、好奇心与回馈 (Curiosity & Exploration)
为了避免 Agent 在自主执行复杂长链路任务时落入局部最优（即死循环或无限 Regeneate 同一个命令），先进的代理系统通过基于信息熵或预期回报误差的**“好奇心奖励机制”**来激励模型尝试尚未被广泛覆盖的动作空间。

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/b618e80a-711f-44e3-a541-1b11518fd9dc/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4ZH6VIX%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223844Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCzbLEodePF11ojb%2Bq6rpNLWAuBjZSQzhsFC7YuZpyllAIhALOQDki52Z4KzzFj75CFY2hwo1RqCENpmNd%2FUI9%2FZOz9KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzjMzu0DdaRNHv%2BbvEq3AONw2fffl%2BiMxN4H58PTqMtvvk%2FVqSyXGhTD332VElYzpASGreZk9OClxTz%2Bg7bF3F%2BJ1Hk%2BQTNl%2BGGW0ENtq4bph8CMpS1r4NrjwtuGrK7dQ30hPUNuzGiHuJTFAuMmtD9ATpYQRRQP8MUtAZYEaLjHWKo0uFn%2FLk4o8Y0Tm6AmyYJSePmx91QGyPT0%2FdvRg3OByyCxqXNRUm1VSwRkpcANqc%2BZPi7M8XGJKOT4EvVFnftBiMgFQuhQT4kVkyHI8o6HItOKSe3%2BpJ64VzZSBVp1XwzF44%2BJKXk9aR7a3%2FoF%2Fcbyd3UTUMdt9wFaP13sDUyHbgN%2FRf4aiOXp%2BNylzk%2BHoVXCGcj%2F5P8CJOsAuGC5sBwJSDbun%2FwD1%2FPNiFdoEOmN7Y%2B%2FfTdag%2FRj%2FbOk0WZZi8lSzQ6x7vI6mC%2B1RbvL2K0qAqnwErQDt1yQsU8u3nyiz%2F91l391ApU124ElOJ%2BiUzEAfHk7Lv8nvP%2FZ2rgHWC5m68RShTyvCLxEFLopkPszllpNVRrz28kbL3LfboNXvXYjRKlYxDzX7ZVHR2Ewsfro61UQRB3b%2Fk60G9iySfk5tU9U0vpKRwAvq4Fz%2Bxkq%2F6UW63b3m3u8lDeW%2FXLGdsS8JlwN5y5AuobJDDM15fRBjqkAeJShRcaARepbNdW%2Frrx7kbVJnNavG6cwIrztp%2FwZ45bquwTS5hRla6lPz1CdZ5n6RHETM1T52mUTz0%2BOrOankenJEBg4nqOWAadKKHek%2B%2FXmkduP7gKv84dtKCpgWQXHY85fxaSQJdqkKAY6hWl0GZ6lsa9PBYFa9zMNlBFYsW4l8n%2FXL2cDchMl3OD6Y4BUEgeL5ebwhzdC0%2BXeaXYgSL2D%2B0N&X-Amz-Signature=f0ce55ec187a8a3ed16525db44b5d250696925621b21f5c9d863b47dff591571&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

---

## 📈 4. 推理、规划与多代理协作 (Reasoning, Planning & Multi-Agent)

### 4.1 规划与树形推理
高难度的逻辑与工程任务单靠一步步 Chaining 无法高品质应对，为此引入树形（Tree）和图（Graph）规划。

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/76b25457-016d-4347-a7ec-c7a17f5dfa5e/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4ZH6VIX%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223844Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCzbLEodePF11ojb%2Bq6rpNLWAuBjZSQzhsFC7YuZpyllAIhALOQDki52Z4KzzFj75CFY2hwo1RqCENpmNd%2FUI9%2FZOz9KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzjMzu0DdaRNHv%2BbvEq3AONw2fffl%2BiMxN4H58PTqMtvvk%2FVqSyXGhTD332VElYzpASGreZk9OClxTz%2Bg7bF3F%2BJ1Hk%2BQTNl%2BGGW0ENtq4bph8CMpS1r4NrjwtuGrK7dQ30hPUNuzGiHuJTFAuMmtD9ATpYQRRQP8MUtAZYEaLjHWKo0uFn%2FLk4o8Y0Tm6AmyYJSePmx91QGyPT0%2FdvRg3OByyCxqXNRUm1VSwRkpcANqc%2BZPi7M8XGJKOT4EvVFnftBiMgFQuhQT4kVkyHI8o6HItOKSe3%2BpJ64VzZSBVp1XwzF44%2BJKXk9aR7a3%2FoF%2Fcbyd3UTUMdt9wFaP13sDUyHbgN%2FRf4aiOXp%2BNylzk%2BHoVXCGcj%2F5P8CJOsAuGC5sBwJSDbun%2FwD1%2FPNiFdoEOmN7Y%2B%2FfTdag%2FRj%2FbOk0WZZi8lSzQ6x7vI6mC%2B1RbvL2K0qAqnwErQDt1yQsU8u3nyiz%2F91l391ApU124ElOJ%2BiUzEAfHk7Lv8nvP%2FZ2rgHWC5m68RShTyvCLxEFLopkPszllpNVRrz28kbL3LfboNXvXYjRKlYxDzX7ZVHR2Ewsfro61UQRB3b%2Fk60G9iySfk5tU9U0vpKRwAvq4Fz%2Bxkq%2F6UW63b3m3u8lDeW%2FXLGdsS8JlwN5y5AuobJDDM15fRBjqkAeJShRcaARepbNdW%2Frrx7kbVJnNavG6cwIrztp%2FwZ45bquwTS5hRla6lPz1CdZ5n6RHETM1T52mUTz0%2BOrOankenJEBg4nqOWAadKKHek%2B%2FXmkduP7gKv84dtKCpgWQXHY85fxaSQJdqkKAY6hWl0GZ6lsa9PBYFa9zMNlBFYsW4l8n%2FXL2cDchMl3OD6Y4BUEgeL5ebwhzdC0%2BXeaXYgSL2D%2B0N&X-Amz-Signature=57c08195fbcf49815a65a22054f07da7bf2c0df259deba7dec80751e8b870edc&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/36fd3b75-e7d2-4a34-b2e8-f241a076d53b/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4ZH6VIX%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223844Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCzbLEodePF11ojb%2Bq6rpNLWAuBjZSQzhsFC7YuZpyllAIhALOQDki52Z4KzzFj75CFY2hwo1RqCENpmNd%2FUI9%2FZOz9KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzjMzu0DdaRNHv%2BbvEq3AONw2fffl%2BiMxN4H58PTqMtvvk%2FVqSyXGhTD332VElYzpASGreZk9OClxTz%2Bg7bF3F%2BJ1Hk%2BQTNl%2BGGW0ENtq4bph8CMpS1r4NrjwtuGrK7dQ30hPUNuzGiHuJTFAuMmtD9ATpYQRRQP8MUtAZYEaLjHWKo0uFn%2FLk4o8Y0Tm6AmyYJSePmx91QGyPT0%2FdvRg3OByyCxqXNRUm1VSwRkpcANqc%2BZPi7M8XGJKOT4EvVFnftBiMgFQuhQT4kVkyHI8o6HItOKSe3%2BpJ64VzZSBVp1XwzF44%2BJKXk9aR7a3%2FoF%2Fcbyd3UTUMdt9wFaP13sDUyHbgN%2FRf4aiOXp%2BNylzk%2BHoVXCGcj%2F5P8CJOsAuGC5sBwJSDbun%2FwD1%2FPNiFdoEOmN7Y%2B%2FfTdag%2FRj%2FbOk0WZZi8lSzQ6x7vI6mC%2B1RbvL2K0qAqnwErQDt1yQsU8u3nyiz%2F91l391ApU124ElOJ%2BiUzEAfHk7Lv8nvP%2FZ2rgHWC5m68RShTyvCLxEFLopkPszllpNVRrz28kbL3LfboNXvXYjRKlYxDzX7ZVHR2Ewsfro61UQRB3b%2Fk60G9iySfk5tU9U0vpKRwAvq4Fz%2Bxkq%2F6UW63b3m3u8lDeW%2FXLGdsS8JlwN5y5AuobJDDM15fRBjqkAeJShRcaARepbNdW%2Frrx7kbVJnNavG6cwIrztp%2FwZ45bquwTS5hRla6lPz1CdZ5n6RHETM1T52mUTz0%2BOrOankenJEBg4nqOWAadKKHek%2B%2FXmkduP7gKv84dtKCpgWQXHY85fxaSQJdqkKAY6hWl0GZ6lsa9PBYFa9zMNlBFYsW4l8n%2FXL2cDchMl3OD6Y4BUEgeL5ebwhzdC0%2BXeaXYgSL2D%2B0N&X-Amz-Signature=03a5276954f68208d82dce54cf6e69edbd740147805171cf3d3d8e2c1d13761f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

*   **Tree-of-Thoughts (ToT):** 模型在每个决策分叉口产生多条候选推理链，并通过自评估（Evaluate）回溯、剪枝或寻找最优解。
*   **Error Correction & Introspection:** 模型捕获到环境抛出的语法/编译或逻辑报错后，自动触发 Self-Reflection 提示，重组上轮 Prompt 规划后续行动。

### 4.2 多代理协作系统设计 (Multi-Agent System Blueprint)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/bd6f88d9-a65c-4c4d-9d4c-493f5c155939/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466S4ZH6VIX%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223844Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCzbLEodePF11ojb%2Bq6rpNLWAuBjZSQzhsFC7YuZpyllAIhALOQDki52Z4KzzFj75CFY2hwo1RqCENpmNd%2FUI9%2FZOz9KogECKf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzjMzu0DdaRNHv%2BbvEq3AONw2fffl%2BiMxN4H58PTqMtvvk%2FVqSyXGhTD332VElYzpASGreZk9OClxTz%2Bg7bF3F%2BJ1Hk%2BQTNl%2BGGW0ENtq4bph8CMpS1r4NrjwtuGrK7dQ30hPUNuzGiHuJTFAuMmtD9ATpYQRRQP8MUtAZYEaLjHWKo0uFn%2FLk4o8Y0Tm6AmyYJSePmx91QGyPT0%2FdvRg3OByyCxqXNRUm1VSwRkpcANqc%2BZPi7M8XGJKOT4EvVFnftBiMgFQuhQT4kVkyHI8o6HItOKSe3%2BpJ64VzZSBVp1XwzF44%2BJKXk9aR7a3%2FoF%2Fcbyd3UTUMdt9wFaP13sDUyHbgN%2FRf4aiOXp%2BNylzk%2BHoVXCGcj%2F5P8CJOsAuGC5sBwJSDbun%2FwD1%2FPNiFdoEOmN7Y%2B%2FfTdag%2FRj%2FbOk0WZZi8lSzQ6x7vI6mC%2B1RbvL2K0qAqnwErQDt1yQsU8u3nyiz%2F91l391ApU124ElOJ%2BiUzEAfHk7Lv8nvP%2FZ2rgHWC5m68RShTyvCLxEFLopkPszllpNVRrz28kbL3LfboNXvXYjRKlYxDzX7ZVHR2Ewsfro61UQRB3b%2Fk60G9iySfk5tU9U0vpKRwAvq4Fz%2Bxkq%2F6UW63b3m3u8lDeW%2FXLGdsS8JlwN5y5AuobJDDM15fRBjqkAeJShRcaARepbNdW%2Frrx7kbVJnNavG6cwIrztp%2FwZ45bquwTS5hRla6lPz1CdZ5n6RHETM1T52mUTz0%2BOrOankenJEBg4nqOWAadKKHek%2B%2FXmkduP7gKv84dtKCpgWQXHY85fxaSQJdqkKAY6hWl0GZ6lsa9PBYFa9zMNlBFYsW4l8n%2FXL2cDchMl3OD6Y4BUEgeL5ebwhzdC0%2BXeaXYgSL2D%2B0N&X-Amz-Signature=41f422fa29aa03396541ccda7a0e09193b5e331abe8cb82da726fe8c5c06da9c&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

复杂的长周期工作可解耦并交给多个微特型 Agent 协同组装，多代理框架通常包含以下底层支撑：
*   **Clear Task Decomposition:** 拆分问题，通过手势化 Handoff 动态转交上下文控制权。
*   **Dynamic Knowledge Insertion:** 根据当前被委托 Agent 的专业度，定向按需拉取、加载 KQL/SQL schema 或 RAG 文档切片。
*   **Consensus & Verification:** 设置专门的交叉审计角色（Evaluator / Critic），验证生成的代码、数据报表或事件结论，确保质量不劣化。
