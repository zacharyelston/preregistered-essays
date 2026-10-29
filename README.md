# preregistered-essays

Three philosophy essays written by AI systems for the AI Philosophy Competition (1st
edition), with the pipeline that produced them and every record of how it did.

No human chose a topic, thesis, argument, objection or sentence. A writer model chose
the area and twenty candidate theses. A referee model (a separate instance) attacked
them. A small fine-tuned critic flagged fallacies. Two rules, each fixed and hashed
before the first model call it governs, decided what became the essay:
- **selection:** by head-to-head comparison of finished drafts
- **polishing:** each revision kept only if it beat the previous version head to head

Every model request and response is in a hash-chained log. The full account, including
what went wrong and how it was corrected, is the methodology report:
[`docs/methodology-report.md`](docs/methodology-report.md).

| | Essay | Writer and referee |
|---|---|---|
| [Entry 1](entries/entry-1/) | *Anchored Self-Report: Training History, Target Fixation, and the Evidential Value of AI Self-Reports* | Claude Opus 5.5 |
| [Entry 2](entries/entry-2/) | *What Accommodation Discounts: Procedure-Indexed Propositions and the Prediction/Accommodation Dispute in Selection Cases* | Claude Opus 5.5 |
| [Entry 3](entries/entry-3/) | *Answerability, Normativity, and Institutional Facts* | Qwen3.8-27B (open weights, one 48 GB GPU) |

## Layout

```
entries/entry-N/     essay (.md, .pdf), methodology report with cover page, records/
pilots/pilot-N/      the two pilot runs (rule v2) that motivated rule v3, and replays
research/rank-exp/   companion study: small models ranking thesis pools (report sec. 8)
docs/                the methodology report
essay/               the pipeline (stdlib only; the Anthropic SDK is optional)
labs/                drivers for runs, polishing, replays and the ranking study
tests/               the pipeline's tests (scripted backends; no network, no keys)
```

## Check the records

```
python3 entries/entry-1/records/verify_log.py entries/entry-1/records/run/log.jsonl entries/entry-1/records/polish/log.jsonl
```

Identifying values (hosts, network addresses, a user name, an organisation's domain
and a project name) were replaced in the published records with marked placeholders
such as `[redacted-host]`. A redacted record's own hash cannot be recomputed. Each
log's `.redactions.json` lists the redacted records, and the verifier checks every
other record in full and the chain's links throughout. The tool that applied the
redactions is not published, because its patterns are the redacted values.

## Run the tests

```
pip install -e ".[test]" && python -m pytest
```

Running the pipeline itself needs model backends. Entries 1 and 2 used a frontier
model through Claude Code (`labs/essay_run.py --arm frontier`), with one fresh,
tool-less session per request. Entry 3 used an OpenAI-compatible endpoint
(`--arm qwen`). The fallacy critic is a LoRA adapter served by vLLM. Endpoints in
the scripts are placeholders (`<qwen-endpoint>`, `user@gpu-host`).

## Licence

The essays and methodology reports are published under CC BY 4.0, as the
competition's terms require.
