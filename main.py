#!/usr/bin/env python3
"""Estimate token counts for text.

Uses a word-based estimate (about 0.75 words per token, i.e. roughly
4 characters per token) by default. If tiktoken is installed it is used
for an exact count with the chosen encoding, but it is never required.
"""
import argparse
import re
import sys

# Rough rule of thumb used by OpenAI: ~4 characters or ~0.75 words per token.
CHARS_PER_TOKEN = 4.0
WORDS_PER_TOKEN = 0.75


def word_count(text):
    return len(re.findall(r"\S+", text))


def estimate_tokens(text):
    """Return (char-based estimate, word-based estimate)."""
    char_est = max(1, round(len(text) / CHARS_PER_TOKEN)) if text else 0
    word_est = max(1, round(word_count(text) / WORDS_PER_TOKEN)) if text else 0
    return char_est, word_est


def tiktoken_count(text, encoding_name):
    """Exact count via tiktoken if installed, else None."""
    try:
        import tiktoken
    except ImportError:
        return None
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def main():
    parser = argparse.ArgumentParser(
        description="Estimate token counts for text (word-based estimate; "
                    "uses tiktoken if installed, but does not require it).")
    parser.add_argument("file", nargs="?", help="Text file to count "
                        "(default: read from stdin).")
    parser.add_argument("--encoding", default="cl100k_base",
                        help="tiktoken encoding to use when available "
                             "(default: cl100k_base).")
    parser.add_argument("--json", action="store_true",
                        help="Print the result as JSON.")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as exc:
            print(f"Error: cannot read {args.file}: {exc}", file=sys.stderr)
            return 1
    else:
        text = sys.stdin.read()

    words = word_count(text)
    chars = len(text)
    char_est, word_est = estimate_tokens(text)
    estimate = round((char_est + word_est) / 2) if text else 0
    exact = tiktoken_count(text, args.encoding)

    if args.json:
        import json
        print(json.dumps({
            "characters": chars, "words": words,
            "estimated_tokens": estimate,
            "char_based_estimate": char_est,
            "word_based_estimate": word_est,
            "tiktoken_tokens": exact,
            "tiktoken_encoding": args.encoding if exact is not None else None,
        }))
        return 0

    print(f"Characters: {chars}")
    print(f"Words: {words}")
    print(f"Estimated tokens: ~{estimate}")
    print(f"  (char-based: {char_est}, word-based: {word_est})")
    if exact is not None:
        print(f"tiktoken ({args.encoding}): {exact} tokens")
    else:
        print("tiktoken not installed; showing estimate only "
              "(pip install tiktoken for exact counts).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
