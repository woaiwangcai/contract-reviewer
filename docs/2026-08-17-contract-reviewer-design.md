# Contract Reviewer Design

## Goal

Build a small, polished, model-provider-neutral AI workflow for reviewing Chinese
commercial contracts. A user supplies a DOCX file, the workflow converts it to
Markdown, sends it with a reusable review skill to an OpenAI-compatible API, and
writes both Markdown and standalone HTML reports.

## Scope

The public project contains one command-line workflow:

```text
DOCX -> Markdown -> review skill + contract -> model API -> Markdown -> HTML
```

Included:

- DOCX paragraphs, headings, lists, and tables converted to readable Markdown.
- One configurable OpenAI-compatible model client.
- A model-neutral contract-review skill with evidence and output requirements.
- Markdown and self-contained HTML reports.
- A fictional example contract, focused tests, and public documentation.

Excluded:

- PDF and legacy DOC conversion.
- Knowledge bases, customer files, reference routing, and MinerU.
- Tracked changes, comments, batch review, web UI, and agent planning.
- Any files, prompts, logs, or secrets from the private working project.

## Interface

The primary command is:

```powershell
python main.py --input examples/sample_contract.docx
```

Optional arguments select a skill and output directory. Model settings come from
environment variables:

```text
MODEL_API_KEY
MODEL_BASE_URL
MODEL_NAME
```

The workflow creates `<document>-review.md` and `<document>-review.html`.

## Components

- `main.py`: validates CLI arguments and presents concise Chinese status/errors.
- `src/docx_to_md.py`: deterministic DOCX-to-Markdown conversion.
- `src/model_client.py`: one OpenAI-compatible chat-completions request.
- `src/md_to_html.py`: Markdown rendering with a standalone HTML template.
- `src/workflow.py`: orchestrates the four stages and owns output paths.
- `skills/contract_review.md`: task instructions, evidence rules, severity rules,
  and a stable Markdown response contract.

## Error Handling

The command fails clearly for a missing or invalid DOCX, empty extracted text,
missing model settings, API failures, and empty model responses. Secrets are never
printed or persisted. Partial model output is not cached.

## Verification

Automated tests cover DOCX conversion, table conversion, HTML rendering, safe output
names, missing configuration, and the workflow with a fake model client. The release
check also scans tracked files for likely secrets and runs the documented example.

## Release

The repository is named `contract-reviewer`. Version `v1.0.0` includes source code,
README, fictional example input, example reports, tests, an MIT license, and a GitHub
Release archive. The README leads with the result, explains the workflow, and provides
a copy-paste quick start.
