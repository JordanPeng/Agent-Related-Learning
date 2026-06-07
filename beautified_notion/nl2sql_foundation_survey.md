# 📝 Deep Learning NL2SQL Foundations (Before LLMs)

This study guide reviews the fundamental architectures, taxonomies, and methodologies used in neural Natural Language to SQL (NL2SQL) translation prior to the emergence of highly generalized Large Language Models.

---

## 📌 1. Definition of the NL2SQL Problem

Given a **Natural Language Query (NLQ)** describing user intent, and a **Relational Database (RDB)** with a specific schema $\mathcal{S}$ (comprising tables, columns, and foreign keys):
Generate a mathematically equivalent **SQL Query** $\mathcal{Q}$ that executes successfully on the target database, returning the precise data matching the user's intent.

$$f(\text{NLQ}, \mathcal{S}) \to \mathcal{Q}$$

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/c4339ac5-11be-4674-9c46-33c8dcd4c858/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666TENQZV4%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223900Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIFrq7sByoXn0fpZe8zg88au8GOaVF4XmGn1pelY2WujiAiA6oCSdfcZj3%2F791yDBcZeqDaIHs%2FDFTocZuR8z%2FrItVCqIBAin%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMrX4Zba7jBsEn80mfKtwD9hoEe0C2x6OVQy1K%2F4gb4meDazaBqrloVnaPW4tZ9wFqChzO8fTUg9citVGIS9ZbYDVPv3Qtguh%2Bk3ltAY9YWB088dMki4VETyzjEv5%2BVfvNjca6E1uPceI%2Bdx64mifz%2F0X2l69hMJAPfEhR2rAM3ECdNn0yNMLYA0a%2BC6Tyz0B%2FJFl9ymLIG%2FsGuAY7i4YO5R81%2F49HgeenO34RaF8FsRppSprdsWDveaKdcRDs16NBUJ7onTdW0GUk1NCVGEeEEzqOfz0FeSMluC%2F%2BEFarIYnNJW2jiGzKiRW%2B6ypEnh4jDVwHJgKsMTfs%2BtkSeiA1W70D5HW1halSB2VKvmHNinZ88qKOqTVQNzWS9XcbJR%2FJWkX2c9Hc0fcgYaMhRu5cNqnein5jbKTYMqEDXwfj0xlzhjOZig%2Bi%2BbxIkWW7RWR5FMsrnU3bSxVpQaoGxIhwG0Xqhat547M0XvfrYMj4dSdtIz4vtEPZZU4mwkjQbKWjulHaWXBGpKT0ds7E6cqjnrbCsO8jXF7SsJ8vy147Way52mnZaYCLZsvLPWtnSHToKHxxb%2Fuc8ldAPcgCCJVyOOCHDQC5SymuosHl3B80ABzhDbvxvxL5bFFScVGmi1H9K71jqyEtRlGhYvEwgdeX0QY6pgG638r6161261ytu4YweOPRsQjiUIq5DOKWJLj%2FCERfY2h5aKtdmcMzgXSv0Fai0rbVWcQHxZ23h5bvdAHXy8lMXQJK%2B6IMXqnDXf7foMolG9Ym5P%2F9W56ieGD0M5zAHxyumlrsSaUgML3UYlItyAi6rT7xmGfj8uvdqwayHRbf2HtnPCffECdc50FTNtZB3baptmlc1jVl07qFCcbu%2FClgoEXIeczk&X-Amz-Signature=6c8b0664dc13ad0925c2f4f387bed61e076d25988e32c3967dfdd12dd49cde70&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/fd0a5159-00aa-408d-9beb-2ca7e331c33b/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666TENQZV4%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223900Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIFrq7sByoXn0fpZe8zg88au8GOaVF4XmGn1pelY2WujiAiA6oCSdfcZj3%2F791yDBcZeqDaIHs%2FDFTocZuR8z%2FrItVCqIBAin%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMrX4Zba7jBsEn80mfKtwD9hoEe0C2x6OVQy1K%2F4gb4meDazaBqrloVnaPW4tZ9wFqChzO8fTUg9citVGIS9ZbYDVPv3Qtguh%2Bk3ltAY9YWB088dMki4VETyzjEv5%2BVfvNjca6E1uPceI%2Bdx64mifz%2F0X2l69hMJAPfEhR2rAM3ECdNn0yNMLYA0a%2BC6Tyz0B%2FJFl9ymLIG%2FsGuAY7i4YO5R81%2F49HgeenO34RaF8FsRppSprdsWDveaKdcRDs16NBUJ7onTdW0GUk1NCVGEeEEzqOfz0FeSMluC%2F%2BEFarIYnNJW2jiGzKiRW%2B6ypEnh4jDVwHJgKsMTfs%2BtkSeiA1W70D5HW1halSB2VKvmHNinZ88qKOqTVQNzWS9XcbJR%2FJWkX2c9Hc0fcgYaMhRu5cNqnein5jbKTYMqEDXwfj0xlzhjOZig%2Bi%2BbxIkWW7RWR5FMsrnU3bSxVpQaoGxIhwG0Xqhat547M0XvfrYMj4dSdtIz4vtEPZZU4mwkjQbKWjulHaWXBGpKT0ds7E6cqjnrbCsO8jXF7SsJ8vy147Way52mnZaYCLZsvLPWtnSHToKHxxb%2Fuc8ldAPcgCCJVyOOCHDQC5SymuosHl3B80ABzhDbvxvxL5bFFScVGmi1H9K71jqyEtRlGhYvEwgdeX0QY6pgG638r6161261ytu4YweOPRsQjiUIq5DOKWJLj%2FCERfY2h5aKtdmcMzgXSv0Fai0rbVWcQHxZ23h5bvdAHXy8lMXQJK%2B6IMXqnDXf7foMolG9Ym5P%2F9W56ieGD0M5zAHxyumlrsSaUgML3UYlItyAi6rT7xmGfj8uvdqwayHRbf2HtnPCffECdc50FTNtZB3baptmlc1jVl07qFCcbu%2FClgoEXIeczk&X-Amz-Signature=7228735cafa4c4ed11511b28f8df0be97bd64aa34dbabe2c4d24376c347c69e4&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/2d861715-3c1c-4b05-b49e-e9f42bc4f4f5/ddb11439-c8d8-44af-bb35-79e6cea91b77/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666TENQZV4%2F20260607%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260607T223900Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEN7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIFrq7sByoXn0fpZe8zg88au8GOaVF4XmGn1pelY2WujiAiA6oCSdfcZj3%2F791yDBcZeqDaIHs%2FDFTocZuR8z%2FrItVCqIBAin%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMrX4Zba7jBsEn80mfKtwD9hoEe0C2x6OVQy1K%2F4gb4meDazaBqrloVnaPW4tZ9wFqChzO8fTUg9citVGIS9ZbYDVPv3Qtguh%2Bk3ltAY9YWB088dMki4VETyzjEv5%2BVfvNjca6E1uPceI%2Bdx64mifz%2F0X2l69hMJAPfEhR2rAM3ECdNn0yNMLYA0a%2BC6Tyz0B%2FJFl9ymLIG%2FsGuAY7i4YO5R81%2F49HgeenO34RaF8FsRppSprdsWDveaKdcRDs16NBUJ7onTdW0GUk1NCVGEeEEzqOfz0FeSMluC%2F%2BEFarIYnNJW2jiGzKiRW%2B6ypEnh4jDVwHJgKsMTfs%2BtkSeiA1W70D5HW1halSB2VKvmHNinZ88qKOqTVQNzWS9XcbJR%2FJWkX2c9Hc0fcgYaMhRu5cNqnein5jbKTYMqEDXwfj0xlzhjOZig%2Bi%2BbxIkWW7RWR5FMsrnU3bSxVpQaoGxIhwG0Xqhat547M0XvfrYMj4dSdtIz4vtEPZZU4mwkjQbKWjulHaWXBGpKT0ds7E6cqjnrbCsO8jXF7SsJ8vy147Way52mnZaYCLZsvLPWtnSHToKHxxb%2Fuc8ldAPcgCCJVyOOCHDQC5SymuosHl3B80ABzhDbvxvxL5bFFScVGmi1H9K71jqyEtRlGhYvEwgdeX0QY6pgG638r6161261ytu4YweOPRsQjiUIq5DOKWJLj%2FCERfY2h5aKtdmcMzgXSv0Fai0rbVWcQHxZ23h5bvdAHXy8lMXQJK%2B6IMXqnDXf7foMolG9Ym5P%2F9W56ieGD0M5zAHxyumlrsSaUgML3UYlItyAi6rT7xmGfj8uvdqwayHRbf2HtnPCffECdc50FTNtZB3baptmlc1jVl07qFCcbu%2FClgoEXIeczk&X-Amz-Signature=5bf4867375e104eb94b4119e8b06b8c7a724476fc222d10a74192cccc5d09189&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

### 4.1 Value Grounding Strategies
*   **Tri-Gram / Fuzzy Jaro-Winkler Matching:** Computes string similarities between words in the query and column headers to identify likely candidates.
*   **FTS (Full-Text Search) In-Memory Lookup:** Formulates a fast, behind-the-scenes query (using BM25 indexes or similar) to see if a query argument matches a specific database column value. This provides the generator with concrete evidence (e.g., *"Europe" matches the 'continent' column*) before it begins translating.
