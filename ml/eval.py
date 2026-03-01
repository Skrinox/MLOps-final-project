import os
import json
import sys


MAE_THRESHOLD = float(os.getenv("MAE_THRESHOLD", "5.0"))

def main():
    # Read the JSON payload piped from train.py
    if not sys.stdin.isatty():
        payload = sys.stdin.read().strip()
    else:
        if len(sys.argv) > 1:
            payload = sys.argv[1]
        else:
            print(json.dumps({"error": "No input payload found"}))
            sys.exit(1)
        
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
        
    mae = float(data["mae"])
    passed = mae <= MAE_THRESHOLD
    
    result = {
        "passed": passed,
        "mae": mae,
        "threshold": MAE_THRESHOLD,
        "model_version": data.get("model_version"),
        "run_id": data.get("run_id"),
    }
    
    
    print(json.dumps(result))
    
    if not passed:
        sys.exit(1)

if __name__ == "__main__":
    main()