import re

def clean_log(text: str) -> str:
    # strip super noisy lines (timestamps-only, long hex dumps, etc.)
    lines = []
    for ln in text.splitlines():
        if len(ln) > 2_000:  # discard absurdly long lines
            continue
        lines.append(ln)
    return "\n".join(lines)

def head_tail(text: str, head_kb=64, tail_kb=128) -> str:
    # keep first/last chunks if log is huge
    b = text.encode("utf-8", errors="ignore")
    head = b[: head_kb*1024].decode("utf-8", "ignore")
    tail = b[-tail_kb*1024 :].decode("utf-8", "ignore")
    return head + "\n...\n" + tail
