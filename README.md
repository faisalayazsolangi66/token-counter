# token-counter

Estimate token counts for text. By default it uses a word-based estimate
(about 0.75 words per token, roughly 4 characters per token). If
`tiktoken` is installed it also reports an exact count — but tiktoken is
optional and never required.

## Requirements

- Python 3.8+
- No third-party packages (standard library only; `tiktoken` optional)

## Usage

```bash
python3 main.py prompt.txt
echo "Hello world" | python3 main.py
python3 main.py prompt.txt --json
python3 main.py prompt.txt --encoding cl100k_base
```

Options:

- `file` — text file to count (default: read from stdin)
- `--encoding` — tiktoken encoding to use when available (default: cl100k_base)
- `--json` — print the result as JSON

## Example

```bash
$ echo "Hello, this is a short test sentence for counting tokens." | python3 main.py
```

Sample output:

```
Characters: 59
Words: 10
Estimated tokens: ~14
  (char-based: 15, word-based: 13)
tiktoken not installed; showing estimate only (pip install tiktoken for exact counts).
```

## License

MIT — see [LICENSE](LICENSE).
