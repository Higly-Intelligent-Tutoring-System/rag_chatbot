import argparse
import asyncio
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path

import requests
from evaluation.config import eval_settings, core_settings, datasets_dir


def send_request_to_api(question, api_url, results_dict, index):
    """Send a single request to the API in a separate thread."""
    thread_id = str(uuid.uuid4())
    
    try:
        resp = requests.post(
            url=f"{api_url}/chat",
            json={
                "message": question,
                "thread_id": thread_id,
            },
            timeout=60,
        )
        resp.raise_for_status()
        
        results_dict[index] = {
            "question": question,
            "thread_id": thread_id,
            "status": "success",
            "response": resp.json(),
            "timestamp": datetime.now().isoformat(),
        }
        print(f"✓ Query {index + 1} completed (thread_id: {thread_id})")
        
    except requests.exceptions.RequestException as e:
        results_dict[index] = {
            "question": question,
            "thread_id": thread_id,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        print(f"✗ Query {index + 1} failed: {e}")


def wait_for_api(api_url, max_retries=30):
    """Wait for API to be ready using the /liveness endpoint."""
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{api_url}/liveness", timeout=2)
            if response.status_code == 200:
                print(f"✅ API is ready at {api_url}")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        retry_count += 1
        if retry_count < max_retries:
            print(f"⏳ Waiting for API to start... ({retry_count}/{max_retries})")
            time.sleep(1)
    
    raise RuntimeError("API failed to start after 30 seconds")


def run_evaluation(api_url, test_queries):
    """Run evaluation queries against the API using threads."""
    results_dict = {}
    threads = []
    
    for index, question in enumerate(test_queries):
        thread = threading.Thread(
            target=send_request_to_api,
            args=(question, api_url, results_dict, index),
            daemon=False,
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    print(f"⏳ Waiting for {len(threads)} threads to complete...")
    for thread in threads:
        thread.join()
    
    print(f"✅ All requests completed!")
    
    return [results_dict[i] for i in sorted(results_dict.keys())]


def print_and_export_results(results):
    """Print results summary and export to JSON."""
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "error")
    
    print(f"\n📊 Results Summary:")
    print(f"   Successful: {successful}/{len(results)}")
    print(f"   Failed: {failed}/{len(results)}")

    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n📄 Detailed results saved to eval_results.json")


async def main(env_file, dataset_path):
    api_process = None
    
    try:
        # 1. Load test queries ---------------------------------------------------
        print(f"📋 Loading dataset from: {dataset_path}")
        try:
            with open(dataset_path) as f:
                test_queries = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON in {dataset_path}: {e}") from e
        
        print(f"📋 Loaded {len(test_queries)} test queries")

        # 2. Build & compile Chatbot API ----------------------------------------
        cmd = f"(export $(cat {env_file} | xargs) && uv run --package api uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload)"
        print(f"🚀 Starting API server...")
        
        api_process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        api_url = "http://localhost:8000"
        wait_for_api(api_url)

        # 3. Run evaluation
        results = run_evaluation(api_url, test_queries)
        
        # 4. Print and export results
        print_and_export_results(results)
        
    finally:
        # 5. Graceful shutdown ---------------------------------------------------
        if api_process is not None:
            print("\n🛑 Shutting down API server...")
            api_process.terminate()
            try:
                api_process.wait(timeout=5)
                print("✅ API server stopped gracefully")
            except subprocess.TimeoutExpired:
                print("⚠️  API server did not stop, forcing kill...")
                api_process.kill()
                api_process.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run evaluation queries in parallel")
    parser.add_argument(
        "--env",
        type=str,
        required=True,
        help="Path to .env file to load environment variables",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to dataset JSON file with test queries",
    )
    
    args = parser.parse_args()
    
    # Validate files exist
    env_path = Path(args.env)
    if not env_path.exists():
        print(f"❌ Error: Environment file not found: {args.env}")
        sys.exit(1)
    
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"❌ Error: Dataset file not found: {args.dataset}")
        sys.exit(1)
    
    print(f"📦 Loading environment from: {args.env}")
    
    asyncio.run(main(args.env, str(dataset_path)))


# (export $(cat envs/.env.prod.ltu | xargs) && uv run --package evaluation python -m evaluation.chatbot_auto --env envs/.env.prod.ltu --dataset packages/evaluation/src/evaluation/evals/datasets/vilnius.json)