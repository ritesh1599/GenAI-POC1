import argparse, os, json, sys
from smartrca.config import SETTINGS
from smartrca.s3_io import read_s3_text
from smartrca.analyze import analyze_text_log

def read_input(path: str) -> str:
    if path.startswith("s3://"):
        return read_s3_text(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def main():
    ap = argparse.ArgumentParser(description="SmartRCA: analyze Glue/Spark logs with LLM")
    ap.add_argument("--path", required=True, help="local path or s3://bucket/key")
    args = ap.parse_args()

    text = read_input(args.path)
    result = analyze_text_log(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
