# Undergraduate Thesis Topic Framework

Use this reference for Chinese undergraduate thesis topic selection, narrowing, comparison, and proposal-ready planning.

## Intake Questions

Ask only what is necessary. Prefer 3-5 questions, not a long questionnaire.

Core questions:

1. What is the major or discipline?
2. Is there a real project, dataset, internship/company case, survey sample, source code, or only an idea?
3. Does the school prefer system design, empirical research, literature review, case analysis, or another type?
4. What technologies, industries, or topics does the student want or avoid?
5. Are there hard requirements for word count, implementation, data, experiments, references, or title format?

If the user already gives enough constraints, do not re-ask; proceed with assumptions and mark them.

## Topic Evaluation Rubric

Score each dimension from 1 to 5 when comparison is useful.

- Scope clarity: Can the object, scenario, method, and boundary be stated in one sentence?
- Feasibility: Can an undergraduate complete it with available time and resources?
- Evidence availability: Are data, code, cases, survey subjects, documents, or references accessible?
- Literature support: Do retrieved titles and abstracts provide enough material for background, related work, methods, and problem framing?
- Method fit: Does the method match the discipline and thesis type?
- Novelty: Is there at least a modest angle, module, scenario, or comparison point?
- Writing support: Can it naturally produce chapters and subsections?
- Defense risk: Can the student answer why this topic matters and how the work was verified?

Recommendation rule:

- Prefer topics with no score below 3.
- Reject or downgrade topics with high evidence risk.
- In literature-informed selection, reject or downgrade topics that cannot be supported by retrieved titles and abstracts.
- For non-implemented projects, prefer "design", "analysis", "prototype", "path", "strategy", or "scheme" wording.
- For implemented projects, "design and implementation" is acceptable only when there is real code or a credible build plan.

## Literature-Informed Recommendation Workflow

Use this workflow when the user wants recommendations based on keyword search, abstracts, or a local literature database.

1. Parse the user's broad direction into keyword groups:
   - `core`: main discipline, object, or phenomenon.
   - `scenario`: platform, industry, user group, course, region, or application setting.
   - `method`: theory, model, technology, framework, or research method.
   - `outcome`: problem, effect, optimization goal, evaluation index, or practical value.
2. Generate 8-15 search queries from these groups. Prefer several focused searches over one large query.
3. Use the workflow's literature retrieval module when available. For Chinese CNKI/CSSCI/C-journal searches, `../cnki-cssci-search/SKILL.md` is the preferred retrieval module.
4. Retrieve metadata only:
   - title
   - abstract
   - keywords
   - year
   - source
   - authors
   - URL or record ID
   - matched query
5. Store the retrieval result as a Markdown literature database.
6. Analyze the database before recommending topics. Topic recommendations must cite the database patterns in plain language, such as "many abstracts discuss X, but few narrow it to Y".
7. Recommend 10 topics, then identify the top 3.

Do not download full texts in this mode. Full texts are a later writing-stage task, not a topic-selection requirement.

## Markdown Literature Database Template

Use a Markdown file when the user wants a visible database. Suggested filename:

`literature-database-<short-topic>-<YYYYMMDD>.md`

Use this structure:

```markdown
# 文献元数据数据库：<方向>

## 检索设置

- 用户方向：...
- 专业/学科：...
- 检索技能：...
- 检索日期：...
- 数据范围：仅标题、摘要、关键词、来源等元数据；未下载全文

## 关键词组

| 组别 | 关键词 | 用途 |
|---|---|---|
| core | ... | 核心对象 |
| scenario | ... | 应用场景 |
| method | ... | 方法/技术 |
| outcome | ... | 问题/结果 |

## 文献记录

| ID | 年份 | 标题 | 来源 | 关键词 | 匹配检索式 | 摘要要点 | URL/记录 |
|---:|---:|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... | ... | ... |

## 初步聚类

### 主题簇 A：...

- 代表文献：ID ...
- 常见问题：...
- 常见方法：...
- 可写切口：...

### 主题簇 B：...

- 代表文献：ID ...
- 常见问题：...
- 常见方法：...
- 可写切口：...
```

Keep abstracts summarized when the table would become too wide. Preserve full abstracts in separate bullet records only if the user needs them.

## Literature-Informed Topic Output Template

Use this after the literature database exists:

```markdown
## 文献观察

- 高频对象：...
- 高频方法：...
- 可写小切口：...
- 不建议方向：...

## 10个推荐选题

| 序号 | 推荐题目 | 文献信号 | 类型 | 可行性 | 风险 | 推荐理由 |
|---:|---|---|---|---|---|---|
| 1 | ... | 摘要中反复出现... | 案例研究/系统设计/实证分析 | 高/中/低 | ... | ... |

## 最推荐的3个

1. ...
2. ...
3. ...

## 后续检索关键词

- ...
```

When explaining "文献信号", refer to clusters, repeated keywords, recurring methods, or gaps seen in the metadata database. Do not imply that full papers were read unless they were actually read.

## Title Narrowing Formula

Use one or more of these forms:

- Object + problem + method: `基于X方法的Y问题研究`
- Scenario + system: `面向X场景的Y系统设计与实现`
- Platform + function: `基于X平台的Y功能模块设计与实现`
- Case + analysis: `基于X案例的Y问题分析与优化研究`
- Population + intervention: `X群体中Y问题及Z对策研究`
- Technology + application: `X技术在Y场景中的应用研究`
- Design-only topic: `面向X需求的Y系统设计方案研究`

Avoid these patterns unless narrowed:

- `人工智能发展研究`
- `电子商务平台设计与实现`
- `大学生就业问题研究`
- `企业财务管理研究`
- `短视频营销研究`

Better narrowed versions:

- `生成式人工智能辅助高校课程作业反馈的应用路径研究`
- `基于Spring Boot的校园二手交易平台商品审核模块设计与实现`
- `地方本科院校计算机专业毕业生就业能力影响因素研究`
- `中小制造企业应收账款管理问题及优化对策研究`
- `本地生活类餐饮商家的短视频内容营销策略研究`

## Discipline-Specific Guidance

Computer science and software engineering:

- Good topics need a concrete user group, scenario, feature set, and technology stack.
- A typical title is "基于……的……系统的设计与实现", covering requirements, design, implementation, and testing.

Management, business, accounting, marketing:

- Good topics need a concrete industry, company type, case, platform, or population.
- Avoid claims requiring private company data unless the user has access.
- Prefer public-data, questionnaire, interview, case-analysis, or literature-supported topics.

Education, humanities, and social sciences:

- Good topics need a clear population, course, text corpus, region, period, or platform.
- Avoid overbroad value judgments.
- Prefer manageable interview, questionnaire, text analysis, classroom design, or comparative analysis methods.

Engineering and design:

- Good topics need a product, process, component, use scenario, parameter, or evaluation standard.
- Avoid topics requiring advanced lab equipment unless confirmed available.

## Candidate Output Template

Use this when the user asks for topic recommendations:

```markdown
| 题目 | 类型 | 可行性 | 风险 | 适合原因 |
|---|---|---:|---|---|
| ... | 系统设计/实证分析/案例研究 | 高/中/低 | ... | ... |
```

Then add:

- 推荐优先级：1, 2, 3.
- 最推荐题目：...
- 为什么推荐：...
- 需要补充的材料：...
- 不建议选择的方向：...

## Refinement Output Template

Use this when the user provides an existing title:

```markdown
原题问题：
- 范围：
- 可写性：
- 风险：

改写方案：
1. 保守版：...
2. 平衡版：...
3. 特色版：...

推荐定稿：...

开题时可以这样说明：
...
```

## Full Topic Plan Template

Use this when the user wants an opening-report-ready direction:

```markdown
题目：...

研究对象与范围：
...

研究问题：
1. ...
2. ...
3. ...

主要内容：
1. ...
2. ...
3. ...
4. ...

研究方法：
- 文献研究法：...
- 案例/问卷/系统设计/实验验证：...

可行性：
- 资料来源：...
- 技术或方法基础：...
- 工作量控制：...

预期创新点：
...

风险与规避：
...

建议目录：
1. 绪论
2. 相关理论与技术基础
3. 需求/问题/现状分析
4. 方案设计/模型构建/案例分析
5. 实现/验证/优化建议
6. 总结与展望
```

## Topic Language

Topic recommendations describe work the thesis will do: "拟设计并实现……", "通过功能测试验证……", "基于问卷数据分析……". Literature signals come from the retrieved records; school rules come from the user.
