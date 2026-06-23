---
name: undergraduate-thesis-topic
description: Help choose, narrow, evaluate, rewrite, and justify undergraduate thesis topics, including literature-informed topic recommendation from bibliographic metadata. Use when the user asks for 本科论文选题, 毕业论文选题, 论文题目推荐, 开题方向, 题目优化, 选题可行性, 基于文献推荐选题, literature-informed topic scoping, research-topic scoping, proposal-topic ideas, or needs a Chinese undergraduate thesis topic matched to major, project status, data availability, literature support, difficulty, novelty, and writing feasibility.
---

# Undergraduate Thesis Topic

## Overview

Use this skill to turn a broad major, interest, system idea, or vague thesis direction into a small set of writeable undergraduate thesis topics. Keep the output pragmatic: topics must be narrow enough to write, defensible for an undergraduate project, and honest about whether real implementation, data, experiments, or only design/prototype narrative exists.

## Core Workflow

1. Identify the user's current input type:
   - If they provide only a major or broad field, ask 3-5 short narrowing questions before recommending titles.
   - If they provide a rough title, evaluate and rewrite it directly.
   - If they provide a real project, dataset, internship, codebase, or paper list, anchor the topic to that evidence.
   - If the project is not implemented, keep the topic framed as design, analysis, prototype planning, or expected validation instead of claiming completed implementation.

2. Gather only the minimum missing constraints:
   - Major or discipline.
   - Preferred direction or technologies.
   - Whether there is an implemented system, dataset, experiment, internship material, or only an idea.
   - Expected thesis type: system design, empirical analysis, literature review, algorithm/application, teaching/design case, management/business analysis, etc.
   - School requirements if known: word count, title format, whether real data or implementation is required.

3. Generate candidates in tiers:
   - Safe topics: easiest to complete and defend.
   - Balanced topics: moderate novelty with manageable workload.
   - Ambitious topics: stronger novelty but higher risk; mark the risk clearly.

4. If the user asks for literature-based recommendation, or if the direction is too broad to judge from domain knowledge alone, use Literature-Informed Mode before final recommendations.

5. Score or compare candidates when there are multiple options. Use feasibility, scope clarity, source/data availability, literature support, method fit, novelty, writing difficulty, defense risk, and alignment with undergraduate workload.

6. Recommend 1-3 best choices and explain why. Include a revised title, research object, main chapters or tasks, expected methods, evidence needed, and risks to avoid.

## Literature-Informed Mode

Use this mode when the user wants topic recommendations based on retrieved literature, keywords, titles, abstracts, or a local literature database.

1. Start from the user's major, broad direction, and initial keywords.
2. Expand the direction into search keyword groups:
   - Core object or field.
   - Application scenario or population.
   - Method, theory, technology, or platform.
   - Outcome, problem, or evaluation angle.
3. Ask the user to confirm the keyword groups when the expansion changes the topic boundary.
4. Use the workflow's literature-search module for retrieval. For Chinese CNKI/CSSCI/C-journal searches, prefer `../cnki-cssci-search/SKILL.md` when available. Only request bibliographic metadata: title, abstract, keywords, year, source, author, URL or record identifier, and matched query. Do not download full texts for topic selection.
5. Build or update a Markdown literature database from the retrieved metadata.
6. Analyze the literature database:
   - Frequent concepts and recurring research objects.
   - Underexplored but writeable subtopics.
   - Common methods and evidence types.
   - Topic clusters that are too broad, too mature, or too risky.
7. Recommend 10 undergraduate thesis topics based on the database, not only on general knowledge. For each topic, give the literature signal, reason for recommendation, feasibility, risk, suggested keywords, and suitable thesis type.

## Hard Gates

- Do not invent a completed system, dataset, survey, experiment, company case, or test result. Ask or mark it as proposed/expected if not verified.
- Do not recommend topics that require inaccessible data, excessive algorithm innovation, clinical/legal/financial claims, or graduate-level experiments unless the user explicitly has the resources.
- Do not make the title too large, such as "Research on artificial intelligence in education" or "Design and implementation of an e-commerce platform" without narrowing the object, scenario, method, or module.
- Prefer topics that can support a complete undergraduate thesis structure: background, related work, demand/problem analysis, method/system/design, validation or evaluation plan, conclusion.
- For Chinese deliverables, use natural Chinese academic phrasing, but keep claims modest and defendable.
- In Literature-Informed Mode, do not fabricate retrieved papers. If retrieval has not been done or the database is empty, label the recommendation as pre-search only.
- Do not request or download full texts unless the user separately asks for full-text work. Topic selection should use metadata only.

## Output Patterns

For quick recommendations, produce:

- 5-10 candidate titles.
- A short suitability note for each.
- A risk marker: low, medium, or high.
- The top 1-3 recommendations.

For title refinement, produce:

- Diagnosis of the current title.
- 3-5 revised titles from conservative to more distinctive.
- Recommended final title.
- Why it is easier to write and defend.

For full topic planning, produce:

- Final title.
- Research background and problem.
- Research object and scope boundary.
- Main research/content modules.
- Methods and materials needed.
- Expected innovation or practical value.
- Feasibility and risks.
- Suggested thesis outline.

For literature-informed recommendations, produce:

- Search keyword groups.
- Markdown literature database path or table.
- Literature cluster summary.
- 10 recommended undergraduate thesis topics.
- Reason, evidence signal, feasibility, risk, suggested keywords, and suitable thesis type for each topic.
- Top 3 final recommendations.

## References

Read `references/topic-framework.md` when the task needs scoring, candidate comparison, a full topic plan, literature-informed recommendation, Markdown literature database structure, or a reusable output template.
