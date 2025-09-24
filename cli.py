import argparse, json
from smartrca.s3_io import read_s3_text
from smartrca.analyze import analyze_text_log

def read_input(path: str) -> str:
    """Read from local path or s3://bucket/key"""
    if path.startswith("s3://"):
        return read_s3_text(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def main():
    parser = argparse.ArgumentParser(
        description="SmartRCA with RAG: Analyze Glue/Spark logs using LLM + Knowledge Base"
    )
    parser.add_argument("--path", required=True, help="local path or s3://bucket/key")
    args = parser.parse_args()

    # Step 1: Read log
    text = read_input(args.path)

    # Step 2: Analyze log (Phase 2: RAG-enhanced)
    result = analyze_text_log(text)

    # Step 3: Print structured output
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
