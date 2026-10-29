"""The essay pipeline — an AI-authored philosophy essay with a computed critique
loop and a pre-registered, mechanical selection (no human picks between drafts).

Stages (each a `python -m essay <verb>`, each reading/writing one run dir):
  init      config + pre-registration of the selection rule (hashed, before any
            generation — the selector can't be tuned to the results)
  theses    the writer proposes N candidate theses in the given area
  screen    per thesis: the objector's strongest objection + a novelty pass
  develop   shortlisted theses -> draft -> [steps -> hat critic (hat + placebo
            arms) -> writer fixes or defends each flag] x rounds -> final critic
            pass, grounding, objection check
  select    verify the pre-registration, score every candidate, pick the winner
  human     record a human intervention verbatim (the rules want AI as sole author;
            every human touch is logged, not remembered)

Every model call (full prompt, full response, usage, served-by model, latency) and
every human note lands in one hash-chained `log.jsonl` — the chat log the
competition asks entrants to retain, and the source for the methodology report.
"""
