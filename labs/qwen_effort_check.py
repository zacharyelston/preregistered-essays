"""One objector-shaped task at each reasoning effort (off / low / medium / xhigh):
does each level return the parseable JSON the stage needs, and what does it cost?
The key comes from an env var (never a flag or a file).

    VLLM_API_KEY=... .venv/bin/python labs/qwen_effort_check.py \
        --url https://<qwen-endpoint> --model qwen3.8-27b
"""
import argparse
import time

from essay import stages as S
from essay.backends import OpenAICompatBackend

USER = ("Thesis: An AI system's self-reports about its inner states are no evidence that it "
        "has them, because training on human self-reports fully explains why it produces "
        "them.\n\nGive the single strongest objection to this thesis and argument. Then rate "
        "how damaging it is if unanswered, 1 (minor) to 5 (fatal). Reply with a JSON object: "
        "{\"objection\": str, \"severity\": int, \"rationale\": str}.")
EFFORTS = {"off": {"enable_thinking": False}, "low": {"reasoning_effort": "low"},
           "medium": {"reasoning_effort": "medium"}, "xhigh": {"reasoning_effort": "xhigh"}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--key-env", default="VLLM_API_KEY")
    a = ap.parse_args()
    for name, kw in EFFORTS.items():
        be = OpenAICompatBackend(a.url, a.model, api_key_env=a.key_env, max_tokens=None,
                                 temperature=0.7, timeout=3600,
                                 extra={"chat_template_kwargs": kw})
        t0 = time.time()
        c = be.complete(S.OBJECTOR_SYSTEM, USER, stage="objection")
        secs = time.time() - t0
        try:
            v = S.extract_json(c.text)
            parsed = f"severity {v.get('severity')}; objection: {str(v.get('objection'))[:150]}"
        except ValueError as e:
            parsed = f"UNPARSEABLE ({e}): {c.text[:200]!r}"
        toks = (c.usage or {}).get("completion_tokens")
        print(f"{name:<7} {secs:6.1f}s  completion_tokens {toks}  stop {c.stop_reason}\n"
              f"        {parsed}", flush=True)


if __name__ == "__main__":
    main()
