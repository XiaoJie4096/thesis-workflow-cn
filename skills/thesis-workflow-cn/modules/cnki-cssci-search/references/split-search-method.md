# Split Search Method

Use this reference to design generic CNKI split searches without hard-coding a topic.

## Target Count

The target export count drives the stopping point:

- Small targets such as 5-10: keep strict; export direct matches first.
- Medium targets such as 20-30: use direct plus nearby support.
- Large targets such as 50 or more: include theoretical background only with clear labels.

If strict results are insufficient, report the strict count before expanding.

## Group Design

Create three levels.

### Group A: Directly Relevant

Use words from the user's exact topic:

- Main object or research subject.
- Core technology, method, model, tool, or system.
- Target scenario, population, material, industry, or application.
- Main outcome or task.

Use these as the terms in Group A, then search them with the combination-order rules below. Record zero-result batches; they are evidence that direct CSSCI literature is limited.

### Group B: Nearby Support

Use terms that support design, evaluation, mechanism, application, or adjacent cases. These should still be close enough to help the user's work.

Examples of generic nearby dimensions:

- user experience, interaction, evaluation, adoption, usability
- design strategy, model construction, framework, mechanism
- application case, empirical study, comparative study

### Group C: Theoretical Background

Use broader theory or field-context terms only when needed for the target count or literature review.

Theoretical background should never be reported as direct relevance.

## Combination-Order Search

For each group, search by descending combination order. A group may contain any number of terms; do not assume a fixed count.

### Order Rules

1. Start with the full intersection of all terms in the group.
2. If the full intersection supplies enough relevant records for the target, stop the group. Do not run lower-order combinations.
3. If the full intersection is insufficient, move down exactly one order.
4. Once a lower order is entered, run every combination at that order before judging sufficiency.
5. Judge sufficiency only after an order is complete.
6. Continue downward only if the completed order is still insufficient.
7. Single-term searches are the last order, and if reached, every term in the group must be searched.

### Why This Matters

Do not run terms linearly. A search process like `term 1 -> enough -> stop` overrepresents the first term and may skip other core concepts. Also do not immediately drop from a failed full intersection to a nearby or theoretical group; lower-order combinations within the current group may still be relevant.

### Generic Example

If a group has terms `A`, `B`, `C`, and `D`, the order is:

```text
Order 4:
A * B * C * D

Order 3, only if Order 4 is insufficient:
A * B * C
A * B * D
A * C * D
B * C * D

Order 2, only if completed Order 3 is insufficient:
A * B
A * C
A * D
B * C
B * D
C * D

Order 1, only if completed Order 2 is insufficient:
A
B
C
D
```

Stop checks happen only after `Order 4`, after all `Order 3` searches, after all `Order 2` searches, and after all `Order 1` searches.

## Moving Between Groups

Complete Group A through the needed combination order before moving to Group B. Move to Group B only if Group A cannot meet the target with acceptable direct relevance. Move to Group C only if Group A plus Group B are still insufficient or the user explicitly wants background/theory coverage.

## Ambiguity And Breadth Rules

- If one short term produces many unrelated fields, mark it as ambiguous and require a qualifier.
- If a broad term crosses many unrelated disciplines, combine it with object, scene, method, or field terms.
- If an expansion improves count but lowers relevance, keep it in a lower relevance tier.
- Do not silently invent long synonym lists. Prefer conservative alternatives and ask when interpretation matters.
- Do not use a large OR-heavy expression just to increase count.

## Batch Record Template

Record this for every batch:

```text
批次：
组别：
组合阶层：
检索词：
字段：
来源过滤：
总库结果：
学术期刊：
CSSCI/C刊：
过滤后：
保留数：
相关性等级：
保留/剔除理由：
```

## Selection Rules

Select records by title and abstract when available. Prefer papers that explicitly connect to the user's object, method, scenario, or theoretical need.

Deduplicate across batches by title or CNKI encrypted record ID.

Stop when the target count is reached unless the user asked for exhaustive retrieval.

This stopping rule applies after a completed combination order, not after each individual query inside that order.
