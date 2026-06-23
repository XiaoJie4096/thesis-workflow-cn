# Foreign Literature Title And Abstract Retrieval

Use this reference when the user requests English or foreign literature. Keep this channel focused on metadata retrieval with mandatory abstracts.

## Platform Routing

| Need | Preferred source | Access mode | Notes |
|------|------------------|-------------|-------|
| Cross-disciplinary discovery | OpenAlex | REST API | Broad coverage; abstracts may be stored as inverted indexes |
| DOI and publisher metadata | Crossref | REST API | Strong for DOI, title, venue, dates; abstracts are inconsistent |
| Biomedical literature | PubMed | REST API | Strong for biomedical titles and abstracts through E-utilities |

Prefer official APIs and structured metadata over browser scraping.

## Search Pattern

1. Define topic, discipline, year range if specified, language scope, and target English count.
2. Expand the query into 2-3 conservative English variants:
   - direct phrase from the topic,
   - synonym or nearby concept,
   - abbreviation/full-name form when relevant.
3. First pass: collect candidate titles and source IDs.
4. Second pass: fetch abstracts for selected candidates.
5. If one source has title metadata but no abstract, try another source before excluding the record.
6. Deduplicate by DOI, then PubMed ID, then normalized title plus year.
7. Keep only records with a real abstract in the final output.

Do not include missing-abstract records in the final English deliverable. Put them in the search record as unused candidates.

## Output Data Shape

Use this working record shape internally or in scripts:

```json
{
  "title": "Attention Is All You Need",
  "abstract": "The dominant sequence transduction models...",
  "abstract_status": "found",
  "authors": ["Ashish Vaswani", "Noam Shazeer"],
  "source_type": "conference paper",
  "year": 2017,
  "venue": "NeurIPS 2017",
  "volume_issue": null,
  "pages": null,
  "doi": "10.5555/3295222.3295349",
  "pubmed_id": null,
  "source_platforms": ["crossref", "openalex"],
  "fetched_at": "2026-06-15"
}
```

`abstract_status` values:

| Status | Meaning |
|--------|---------|
| `found` | Abstract was retrieved and may be delivered |
| `missing` | Checked source has no usable abstract; do not deliver unless another source fills it |
| `blocked` | Page/API access was blocked |
| `not_checked` | Abstract lookup was intentionally skipped; do not deliver |

## Merge Priority

| Field | Priority |
|-------|----------|
| `abstract` | PubMed > Crossref when present > OpenAlex |
| `title` | Crossref/PubMed > OpenAlex |
| `venue` | Crossref/PubMed > OpenAlex |
| `source_type` | Crossref type when clear > PubMed publication type > OpenAlex type |
| `volume_issue` | Crossref/PubMed > OpenAlex |
| `pages` | Crossref/PubMed > OpenAlex |
| `doi` | Crossref > OpenAlex > PubMed article IDs |

## API Cheatsheet

### OpenAlex

Search:

```bash
curl -s "https://api.openalex.org/works?search=large+language+models&per-page=10"
```

DOI lookup:

```bash
curl -s "https://api.openalex.org/works/https://doi.org/10.xxxx/yyyy"
```

Reconstruct `abstract_inverted_index` before output:

```js
function restoreAbstract(index) {
  const words = [];
  for (const [word, positions] of Object.entries(index || {})) {
    for (const pos of positions) words[pos] = word;
  }
  return words.join(" ");
}
```

### Crossref

Title search:

```bash
curl -s "https://api.crossref.org/works?query.title=graph+neural+network&rows=10"
```

DOI lookup:

```bash
curl -s "https://api.crossref.org/works/10.xxxx/yyyy"
```

Use Crossref for DOI, title, venue, publisher, ISSN/ISBN, publication date, and publication type. Clean JATS/XML tags if Crossref returns an abstract.

### PubMed

Search:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=CRISPR+gene+editing&retmax=20&retmode=json"
```

Metadata:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=12345678&retmode=json"
```

Abstract XML:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=12345678&rettype=abstract&retmode=xml"
```

## Final English MD Format

Use a minimal format parallel to the Chinese output:

```markdown
# English Titles and Abstracts

## [1]
作者：...
题名：...
文献类型/来源类型：期刊论文
期刊名/出版社/学校/会议名：...
年份：...
卷(期)：...
页码：...

Abstract: ...
```

Use Chinese field labels. Keep English titles and abstracts in English. Use `期刊论文`, `学位论文`, `专著`, `会议论文`, or another accurate source type. Use `未标明` for fields unavailable after checking the source, and `无` for fields that do not apply.

Do not add DOI, source-platform blocks, query logs, raw JSON, relevance labels, or missing-abstract candidates to the final file unless the user explicitly asks for them.
