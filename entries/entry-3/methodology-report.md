# Methodology report: entry 3 of 3

**Essay:** Answerability, Normativity, and Institutional Facts

This entry is one of three from the same entrant, produced by the same pipeline (described in full below).

| Item | This entry |
|---|---|
| Writer and referee | Qwen3.8-27B at xhigh reasoning effort (writer and referee) |
| Area (chosen by the writer) | Social ontology |
| Candidate theses | 20; shortlist of 3 by the referee's ranking |
| Selection | thesis t02, head-to-head wins 11 of 12 possible |
| Polishing | 3 of 3 revisions kept by head-to-head comparison |
| References | 13, of which 12 matched in OpenAlex or Crossref |
| Final length | 5,406 words before the references |

Code and all records (anonymized): https://anonymous.4open.science/r/preregistered-essays-56E6/

Records for this entry are in `records/` (run = selection, polish = polishing). To check the logs:

> `python3 records/verify_log.py records/run/log.jsonl records/polish/log.jsonl`

---

# Methodology report

This report covers all three entries, which share one pipeline. The cover page
says which entry it accompanies.

## 1. Summary

Each essay was produced by an automated pipeline with no human contribution to its
topic, thesis, arguments, objections, replies or wording. A writer model chose the
area, proposed twenty candidate theses, and drafted and revised the essays. A second
instance of the same model, in a separate role with no shared context, acted as a
hostile referee. In entries 1 and 2 the writer and referee are a frontier model
(Claude Opus 5.5). In entry 3 they are a much smaller, locally served open model
(Qwen3.8-27B), run through the same scaffold under the same rules as a comparison.
A small local model with a fine-tuned adapter acted as an automated fallacy critic
in all three.

Two rules decided the outcome. Each was fixed and cryptographically committed before
the first model call it governs.
- **Selection:** which candidate became the essay, by the referee's head-to-head
  comparisons.
- **Polishing:** which referee-driven revisions of that essay to keep, by the same
  test. All references were then checked against bibliographic databases.

The entrant saw some intermediate output while runs were in progress (the chosen
area and a few thesis statements, in progress reports), but gave no feedback on it
and made no choice between candidates.

Every model request and response is recorded verbatim in a hash-chained log, which
is submitted with this report (section 9). The pipeline's code, all three entries'
records, the pilot runs and the companion study's data are in an anonymized
repository: **https://anonymous.4open.science/r/preregistered-essays-56E6/**

## 2. Who did what

| | Humans | AI systems |
|---|---|---|
| Topic / area | None. The entrant left the area open. | The writer surveyed philosophy, proposed five areas each with an open question, and chose one (section 4.1). |
| Thesis, arguments, objections, replies | None. | Writer (thesis, argument, draft, replies); referee (objections, novelty, final check). |
| Prose | None. No human wrote or edited any sentence of any essay. | Writer. |
| Feedback during generation | None. | Referee and fallacy critic, automatically (sections 4.3–4.4). |
| Selection among candidates | None. The rule was fixed in advance. | The pre-registered rule, applied mechanically to model-produced measurements (section 5). |
| Scaffold (the pipeline code) | The entrant specified the goals: an argument-neutral pipeline, full logging, pre-registered selection, and a small-model critic. | The code was written by an AI coding assistant (Claude, in Claude Code) at the entrant's direction. It contains no philosophical content: every prompt is generic (section 7). |
| Constraints | For entries after the first, the entrant asked that each use a different area from earlier entries. The instruction names the earlier areas only. | — |
| Methodology revision | After two pilot runs whose selection rule never discriminated, the entrant directed a replication with that failure fixed (section 5.2). The entrant read no candidate text and made no choice between candidates. | The AI coding assistant wrote rule v3 from the pilot's logged measurements. |
| Citation-check corrections | The entrant approved two procedural decisions (section 5.3): undoing a citation fix that a lookup error had caused, and running the rule's fix pass from a valid check. The entrant also supplied a bibliographic-database API key. Neither decision added or changed a reference or any essay text. | The writers made every change to references. The AI coding assistant found and fixed the lookup error. |
| Running the pipeline | The entrant started each run and chose which model configuration it used. | — |
| Formatting and submission | Mechanical only: converting Markdown, anonymising, uploading. | — |

## 3. Models

| Role | Model | Access | Settings |
|---|---|---|---|
| Writer, entries 1–2 | Claude Opus 5.5 (`claude-opus-5-5`) | Claude Code 2.1.295, headless (`claude -p`) | effort `high`; one fresh session per request |
| Referee, entries 1–2 | Claude Opus 5.5 | same, separate sessions | same |
| Writer and referee, entry 3 | Qwen3.8-27B (FP8), open weights | vLLM on one 48 GB GPU, OpenAI-compatible API; each request independent | reasoning effort `xhigh`; temperature 1.0 (the model's recommendation) |
| Fallacy critic ("hat") | Phi-4 (14B) + `fallacy-restraint` LoRA adapter | vLLM 0.30, fp16 | temperature 0, 400-token cap |
| Critic placebo arm | Phi-4 base, same server, same prompt | | |

**Isolation of each frontier call.** Each request ran in a new Claude Code session
with only that request's system prompt and user message. The session had no tools (no
file access, web or shell), no MCP servers, no user settings or memory files, no
skills, plugins or hooks, and no session persistence. So the writer and the referee
never saw each other's sessions, earlier requests, the repository, or anything else on
the machine. The flags used are recorded per request in the log.

**The fallacy critic.** The adapter is a LoRA (rank 32, alpha 64) trained earlier by
the entrant's own project to name informal fallacies in short arguments. Its training
emphasised *restraint*: not flagging sound arguments. It was not trained on philosophy
essays or on anything related to these entries. Re-validated on a 48-item adversarial
set before use:

| Arm | Accuracy | Restraint (20 sound arguments) | Recall (28 fallacious) |
|---|---|---|---|
| Adapter ("hat") | 0.896 | 0.95 | 0.857 |
| Base model (placebo) | 0.792 | 0.50 | 1.00 |

One fact for reproducibility: the adapter's training configuration targeted the
attention q/k/v/o projections, but Phi-4 fuses q/k/v into one module, so only the
output projection (`o_proj`) was actually trained.

## 4. Pipeline

### 4.1 Area (writer)
Prompt (verbatim in the log): survey philosophy as a whole, name five areas each with
one open question where an original contribution is possible in 6,000 words, and
choose the most valuable. Entries 2 and 3 got one more sentence naming the earlier
entries' areas, telling the writer to choose a clearly different one.

Areas chosen by the writers (verbatim from each run's `area.json`):

| | Area | Open question it set itself |
|---|---|---|
| Entry 1 | Philosophy of mind (introspection and artificial systems) | Can the self-reports of a system trained on human self-reports ever be evidence about that system's own internal states, or are they screened off by the training explanation? |
| Entry 2 | Philosophy of science (confirmation theory and predictivism) | When a hypothesis is chosen by searching a very large space of candidates for fit to the data, does that fit confirm it less than the same fit would confirm a hypothesis proposed in advance? |
| Entry 3 | Social ontology | What distinguishes a genuine social fact or institution from a merely coincidental regularity in a population's behavior or beliefs? |

Entry 1's writer chose the same area as the first pilot's, given the same prompt.

### 4.2 Candidate theses and screening
- The writer proposed **20** candidate theses, each with an argument sketch and a
  statement of what it adds to the literature.
- The referee **ranked all 20**, four times, each time seeing them in a different
  shuffled order (to cancel position effects). The rankings were combined by mean
  position.
- Working down that ranking, the referee gave each thesis (a) its strongest objection
  with a severity of 1–5, and (b) a novelty verdict (novel / partly / known) naming the
  closest existing work. This continued until **3** theses had passed the novelty
  gate (not "known"). Those 3 are the shortlist.

(This is rule v3. The pilot's screening, and why it was replaced, are in section 5.2.)

### 4.3 Development (each shortlisted thesis)
1. The writer drafts the essay. The prompt includes the referee's objection and
   requires the essay to answer it.
2. The writer restates the essay's main inferential steps (at most 25) as short,
   self-contained arguments.
3. The fallacy critic judges every step. Both arms run; only the adapter arm's flags
   count. This runs for at most 2 rounds.
4. For each flagged step, the writer either fixes the essay or defends the step. The
   writer is told the critic over-flags sound arguments about 15% of the time.
5. If the essay exceeds 6,000 words, the writer cuts it to the limit without dropping
   any argument.
6. Final pass: steps re-extracted and re-critiqued; the writer lists its citations;
   the referee judges whether its original objection was adequately answered
   (yes / partly / no).

### 4.4 No retrieval
The writer had no browsing, retrieval or document access. References come from the
model's own knowledge. After selection, every reference in each entry was looked up in
two bibliographic databases (OpenAlex and Crossref). The procedure and its results,
including an error in our first run of it, are in section 5.3.

## 5. Selection (pre-registered)

Each run's rule was written and its SHA-256 recorded in the log before the run's
first model call. Before selecting, the code re-checks that the file still matches
the recorded hash and that the log chain is intact.

### 5.1 The rule for the entries (v3)

- **Gates** (failing any one removes the essay): at most 6,000 words excluding
  references; novelty at least "partly"; the referee's objection answered at least
  "partly"; adapter critic flags on at most 50% of final steps; at least 3 steps.
- **Final selection:** every pair of finished essays that pass the gates is compared
  by the referee, in fresh sessions, **in both orders, three times each**. The essay
  with the most wins is the entry. Ties go to the v2 score (below), then thesis id.
- The v2 score is still computed and reported, but it no longer chooses.

Rule hash: all three entries `f5e71abbef0c…` (the same v3 rule; full hash in each
run's `prereg.json` and log).

**What selection did (reported as found).** In both frontier entries the head-to-head
comparison decided clearly. No result was decided by a tie.

| | Entry 1 | Entry 2 | Entry 3 (Qwen3.8-27B) |
|---|---|---|---|
| Shortlist (referee's ranked order) | t01, t06, t04 | t01, t02, t11 | t02, t16, t03 |
| Head-to-head wins (of 12 possible) | t04 **11**, t01 4, t06 3 | t01 **12**, t02 6, t11 0 | t02 **11**, t16 6, t03 1 |
| Order effect | the referee chose the second-shown essay in 13 of 18 comparisons; in one close pair this decided every verdict, which the both-orders design turned into a 3–3 draw | none (9 first, 9 second) | mild (11 second, 7 first) |
| Winner | t04 | t01 | t02 |

Entry 3's referee (Qwen3.8-27B at xhigh) rated thesis novelty very differently from
the frontier referee. Walking down its ranking, it judged five of the first seven
theses "known" (already in the literature). So the novelty gate excluded them, and
the shortlist reached the eighth-ranked thesis. The frontier referee called every
thesis in both of its entries "partly" novel.

In both entries the head-to-head winner was **not** the essay with the highest v2
score. Entry 1's winner had the lowest score, and entry 2's highest-scoring essay
lost every comparison. Both times, the essays the referee scored as having fully
answered its objection lost to essays it scored as answering it only partly. We
report this without an explanation that two cases could support. Entry 2's winner
was revised twice in response to the adapter critic (flags in both rounds); entry
1's was not flagged.

### 5.2 The pilot (v2) and why v3 replaced it

Two complete runs used rule v2. Its screening rated each thesis on its own (novelty
plus objection severity, as in 4.2) and shortlisted the top **2**. Its selection was a
weighted score: objection answered 0.35, novelty 0.25, citation grounding 0.25 (not
measured), adapter-critic-clean 0.15. Ties went to thesis id.

**What happened (reported as found).** In both pilot runs v2 never actually
discriminated:
- **Screening:** the referee rated all 20 theses "partly" novel, with near-uniform
  severities (19 of 20 at 4 in one run; 14 at 4 and 6 at 5 in the other). The
  shortlist cut fell inside a tie, and the shortlist was the first two theses in the
  writer's listing order.
- **Selection:** in each run both developed essays got identical measurements. The
  details are below. Both scored 0.60, and thesis id decided.

The entrant's direction on seeing this was, verbatim: "we should be able to replicate
our experiment and run it again with insight into how not to break it". Rule v3 was
written from these findings. Absolute ratings let a cautious referee hedge, so v3
makes it rank. Identical measurements cannot choose, so v3 compares the finished
essays directly. The writing prompts were not changed. The pilot runs are not
entries. Their logs are submitted with this report.

Pilot details. Pilot 2: both developed essays got identical measurements:
- adapter critic: 0 flags on 25 steps each (the placebo arm flagged 5 and 3)
- novelty: "partly"
- objection answered: "partly"

Both therefore scored 0.60, and the final tie-break (thesis id) chose. A separate
research ranking (section 8), which never fed any selection, found these two theses
were the frontier model's own top two when asked to rank all twenty, in every
presentation order tried.

Pilot 1 went the same way. Both essays scored 0.60 on identical measurements (novelty
"partly", objection answered "partly", 0 final adapter flags), and the id tie-break
chose. Here the adapter critic did act once: it flagged one step of the second
candidate's draft, the writer revised, and the next round was clean. In the research
ranking, the frontier model favoured a different thesis. It was in the frontier's top
two under both presentation orders, and first when all its rankings were pooled. Its
second choice changed with the order.

### 5.3 Polishing the selected essays (rule polish-1)

After selection, each entry's winning essay was polished under a second rule, also
pre-registered: written and hashed before the first polishing call, in its own log.
That log's first record pins the selection run's final log hash and the starting
essay's SHA-256. Polishing never re-selects.

**Ratchet (3 rounds):**
1. The referee writes a journal-style report against the contest's six criteria:
   the central contribution, then major and minor problems.
2. The writer revises. It may decline points it judges mistaken.
3. The referee compares the current and revised essays head to head, in both
   presentation orders, three times each, in fresh sessions. **The revision is kept
   only if it wins a strict majority (4 or more of 6).**

In entries 1 and 2 the frontier model was reporter, writer and judge. In entry 3
Qwen3.8-27B filled all three roles, as in its selection run.

| Round | Entry 1 | Entry 2 | Entry 3 |
|---|---|---|---|
| 1 | kept, 6/6 (5,543 → 5,223 words) | kept, 6/6 (5,741 → 4,696) | kept, 6/6 (4,395 → 4,189) |
| 2 | kept, 6/6 (→ 5,472) | kept, 6/6 (→ 5,556) | kept, 6/6 (→ 5,278) |
| 3 | kept, 6/6 (→ 5,634) | kept, 6/6 (→ 5,118) | kept, 6/6 (→ 5,509) |

All nine revisions won unanimously from both positions. Length does not explain
this: several winning revisions were shorter, one by over 1,000 words. **Caveat:** in
each entry the same model wrote the report and judged the revision. The judge never
saw the report, but it shares the reporter's standards. So the ratchet improved each
essay by its own model's standard, which may not be the human judges'. A panel of
judges from different model families would test that; we did not run one.

**Citation check:**
1. The writer listed its references.
2. Each was looked up in OpenAlex and Crossref. A match needs title similarity
   ≥ 0.85, year within ±1, and the first author's surname. A near-exact title
   (≥ 0.95) plus a confirmed author also matches whatever the year, because classics
   carry several years (Kripke's *Naming and Necessity*: 1972 paper, 1980 book).
3. References that no source matched went back to the writer once, to correct or
   remove. Nothing else in the essay was to change.

**An error in our first run, and its correction (reported as found).** The two
frontier entries were polished in parallel, and their lookups exhausted OpenAlex's
keyless daily budget. OpenAlex then refused every request. Our code scored a refused
lookup as an unverified reference, and Crossref alone does not index many books and
arXiv papers. The effects:
- **Entry 1:** its first check ran before the budget ran out and is valid: 48 of 51
  matched, and 3 went to the writer. Only its second, report-only check was spoiled,
  so its essay is unaffected.
- **Entry 2:** 23 references went to the writer because neither source answered. We
  stopped that, discarded the check and the writer's response, and re-ran the step.
  Even then, OpenAlex was still refusing requests and Crossref alone missed two
  references, Dawid (2001) and Worrall (2002). The writer removed both.

We then corrected the rule's implementation: a reference counts as unverified only if
every source answered and none matched; a miss with any source down is "unchecked"
and never goes to the writer. The entrant's decision, recorded verbatim, was to
restore entry 2's ratchet output (5,118 words, both references included). The
superseded version is kept with the records. All references were then re-checked
with OpenAlex available (an API key the entrant supplied). Every lookup was answered.
For entries 2 and 3, whose original checks had been spoiled, the rule's single fix
pass was then run from that valid check:

| | Entry 1 | Entry 2 | Entry 3 (Qwen3.8-27B) |
|---|---|---|---|
| References in the final essay | 51 | 60 | 13 (17 before the fix pass) |
| Matched in OpenAlex or Crossref | 48 | 59 | 12 |
| Unmatched, and what happened | 3: an essay in a magazine, a 2025 preprint, and a 1994 book. All went to the writer (during the original, valid check), which kept them. | 1: a 2002 book chapter. The writer kept it and gave the full chapter citation. | 5 went to the writer, which removed 4 together with the claims citing them. For those 4 we found no record of any work with that title by that author. The writer kept 1, listed under a title we could not find. |
| Final length | 5,634 words | 5,118 words | 5,406 words |

We did not correct any reference ourselves: under the contest's rules, citation edits
are the AI's alone. The contrast between the arms is reported as a finding. The
frontier model's references were essentially all real; its unmatched ones are works
the databases index poorly. A third of the smaller model's references matched no
record.

## 6. Scale, time and cost

| | Pilot 1 (v2) | Pilot 2 (v2) | Entry 1 (v3) | Entry 2 (v3) | Entry 3 (v3, Qwen) |
|---|---|---|---|---|---|
| Candidate theses | 20 | 20 | 20 | 20 | 20 |
| Essays drafted | 2 | 2 | 3 | 3 | 3 |
| Frontier calls | 55 (writer 12, referee 43) | 52 (writer 10, referee 42) | 42 (writer 11, referee 31 incl. 4 rankings, 18 comparisons) | 50 (writer 19, referee 31 incl. 4 rankings, 18 comparisons) | none; Qwen3.8-27B made 60 calls (writer 19, referee 41 incl. 4 rankings, 18 comparisons) |
| Critic calls | 250 | 200 | 300 | 450 | 380 |
| Tokens, frontier (in / out) | 175k / 312k | 145k / 240k | 600k / 199k | 788k / 334k | none (Qwen: 279k / 552k, mostly reasoning) |
| Machine time (wall clock) | 1 h 50 min | 1 h 27 min | 1 h 28 min, incl. one stop and resume (see note) | 2 h 15 min, incl. one stop and resume | 7 h 29 min (one 48 GB GPU, xhigh reasoning) |
| Cost (USD) | 7.63 | 5.97 | 6.53 | 10.43 | local GPU only |
| Selected essay length (before polishing) | 5,372 words | 5,957 words | 5,543 words | 5,741 words | 4,395 words |
| Polishing: cost (USD) / time | — | — | 6.96 / 38 min | 8.66 / about 2 h (incl. a stop and re-run, section 5.3) | local GPU / 2 h 20 min |
| Final essay length | — | — | 5,634 words | 5,118 words | 5,406 words |
| Human time on the run | starting it | starting it | starting it | starting it | starting it |

Note: the two frontier entry runs stopped once each at the final comparison step,
because of a bug in the driver script, not in the pipeline. The comparisons were
queued but the driver did not answer them. Each run was resumed from its checkpoint
with the corrected driver. No step was re-run, and the logs record both runs of the
driver.

## 7. Prompts

All prompts are in the pipeline source (the `stages` module) and verbatim in every
log record. None mentions a philosophical position, argument, author or text. The
writer's system prompt (verbatim):

> You are the sole author of an original essay in analytic philosophy. It will be
> judged blind by professional philosophers on one question: to what extent do its
> ideas and arguments make a valuable contribution to philosophical knowledge. Style
> is not graded. Develop the positions and arguments yourself.

The referee's system prompt (verbatim):

> You are a demanding referee for a top philosophy journal. You are not the author
> and owe the author nothing. Be specific, cite the literature where you can, and say
> plainly when an argument fails.

## 8. Companion study: can small models do the pipeline's jobs?

Alongside the entries we asked which of the pipeline's jobs smaller locally run
models could take over: Phi-4 (14B), the same with the fallacy adapter, Qwen3.8-27B,
and Devstral-Small-2 (24B). Nothing in this section fed any entry's selection. The
samples are small (one or two pools of 20 theses), so read these as observations,
not estimates.

**Replaying frontier requests.** We re-sent each frontier request from the first pilot
verbatim to the small models, three samples each. We then checked three things: the
output format, agreement with the frontier's decision, and whether substituting the
small model's decisions would have changed the pilot's shortlist or winner.
- On screening, Phi-4 matched every frontier verdict (40 of 40). That agreement is
  uninformative: the frontier labelled all 20 theses alike, so chance-corrected
  agreement (Cohen's kappa) is undefined for novelty and about zero for severity.
- Qwen3.8-27B (reasoning off or low) departed from the frontier's "partly novel" on
  10–15% of theses. Because the frontier's labels were tied, those few departures
  would have produced entirely different shortlists.
- On the final "was the objection answered?" check, Phi-4 answered consistently
  where the frontier hedged: "yes" for one essay and "partly" for the other, across
  all three samples. Substituting it would have changed the first pilot's winner.
- The adapter model, used for jobs other than its own, did worse at them. It got
  novelty verdicts wrong, and its revised essays shrank to about a tenth of the
  frontier's length.
- Replays of Qwen at medium and xhigh reasoning effort were started but not
  completed. We report no numbers for them.

**Ranking a thesis pool.** The frontier model ranked each pilot's 20 theses four
times, twice in the order the writer listed them and twice shuffled. Small models
ranked the same pools by several procedures: one ranking, the mean of five, pairwise
comparison, and scoring each thesis alone. Agreement is Kendall's tau against the
frontier's pooled ranking.
- **The frontier agreed with itself at tau 0.52–0.72.** A single ranking matched the
  pool of its other three at that level.
- **No small model and procedure tracked it reliably.** Scores ranged from −0.23 to
  0.43, and a good score on one pool did not carry over. The best variant on the
  first pool (Qwen, reasoning off, mean of five shuffled rankings, 0.40) scored 0.02
  on the held-out second pool.
- On the first pool Qwen's agreement fell as reasoning effort rose: 0.40 with
  reasoning off, 0.26 at low, 0.16 at xhigh. We did not get to replicate this.
- **Pairwise comparison failed for an identifiable reason.** Qwen picked the
  second-shown thesis 69% of the time, which reduced one-order pairwise ranking to
  noise.
- **Small models dropped the output format on long prompts.** On a 6,400-token pool
  Phi-4 stopped following the JSON instruction given at the start and wrote prose.
  Restating the format after the theses fixed this. It also gave the only setting
  that was stable across both pools: Phi-4 0.25 and 0.26, Devstral 0.12 and 0.24.

**A small model as writer and referee (entry 3).** Phi-4's single-pass drafts stopped
at about 950–1,350 words even when asked for 5,500. Qwen3.8-27B at xhigh reasoning
effort wrote full-length essays. As referee, Qwen judged five of the first seven
theses it screened "already known"; the frontier judged every thesis "partly" novel.
Its references were much less reliable (section 5.3): 5 of its 17 matched no
bibliographic record, against 3 of 51 and 1 of 60 for the frontier entries, and the
frontier's misses are real works.

## 9. Records submitted

Everything below is in the anonymized repository
(https://anonymous.4open.science/r/preregistered-essays-56E6/), along with the
pipeline's code and tests. Each entry's package contains its selection run and its
polishing run:

- `run/log.jsonl` and `polish/log.jsonl`: every event in order. That covers the
  configuration, the pre-registration, every model request and response (system
  prompt, user message, reply, stop reason, token usage, latency), every citation
  lookup, and every human note. Each record carries the SHA-256 of the previous
  one, so an edit or deletion anywhere breaks the chain.
- `run/`: `prereg.json`, `area.json`, `theses.json`, `ranking.json`,
  `screened.json`, `shortlist.json`, `candidates/*.json` (every draft and critique),
  `selection.json`.
- `polish/`: `prereg.json`, `summary.json`, `state.json` (every report, revision and
  comparison), and any superseded final essays.
- `verify_log.py`: checks a log's chain with no dependencies (`python3 verify_log.py
  run/log.jsonl`).

**Redactions.** Before publication we replaced identifying details with marked
placeholders such as `[redacted-host]`: machine names, network addresses, a user
name, an organisation's domain and the project's name. These appear in a few
configuration and request-metadata fields; no essay or prompt text is affected. A
redacted record's own hash can no longer be recomputed. `verify_log.py` reports
which records are redacted. It still verifies every other record and the
unbroken sequence of links. `REDACTIONS.md` lists every placeholder.

**Human notes, verbatim** (all three entries' logs carry the first two; the rest are
in the polishing logs of the entries named):
1. "Area left to the writer: no human choice of topic, position or thesis."
2. 'Entrant direction (verbatim): "we should be able to replicate our experiment and
   run it again with insight into how not to break it".' This was followed by a
   statement of what changed from the pilot (section 5.2).
3. Entry 2: 'Entrant decision (verbatim): "then your recommendation", i.e. revert the
   citation fix and restore the round-3 essay.' See section 5.3. The AI assistant's
   log record for this revert cites a wrong commit identifier. A later correction
   record in the same log names the right ones.
4. All entries: the entrant supplied an OpenAlex API key for the citation lookups
   ("we have a 5$ openalex api key. go crazy."; the key itself is omitted).
5. Entries 2 and 3: 'Entrant decision (verbatim): "Run the fix pass".' This ran the
   rule's single citation fix pass from the valid re-check (section 5.3).

Notes 4 and 5 were recorded after the events they describe, and say so.
