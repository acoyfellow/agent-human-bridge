#!/usr/bin/env python3
"""
Project Loop Runner

Executes exactly ONE iteration:
1. Load PRD
2. Select highest-priority pending story with completed dependencies
3. Enforce tests-first
4. Run verification
5. Update status and save
"""

import json
import subprocess
import sys
from pathlib import Path

def load_prd():
    prd_path = Path(__file__).parent / "prd.json"
    with open(prd_path, 'r') as f:
        return json.load(f)

def save_prd(prd):
    prd_path = Path(__file__).parent / "prd.json"
    with open(prd_path, 'w') as f:
        json.dump(prd, f, indent=2)

def log_progress(message):
    progress_path = Path(__file__).parent / "progress.txt"
    with open(progress_path, 'a') as f:
        f.write(message + "\n")

def find_eligible_story(prd):
    pending_stories = [s for s in prd["stories"] if s["status"] == "pending"]
    pending_stories.sort(key=lambda s: s["priority"])
    completed_ids = {s["id"] for s in prd["stories"] if s["status"] == "completed"}

    for story in pending_stories:
        deps_completed = all(dep in completed_ids for dep in story.get("dependencies", []))
        if deps_completed:
            return story

    return None

def run_verification(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    prd = load_prd()
    story = find_eligible_story(prd)

    if not story:
        log_progress("STOP: No eligible pending story found")
        print("No eligible story")
        return 1

    max_retries = prd.get("rules", {}).get("max_retries", 0)
    current_retries = story.get("retries", 0)
    if current_retries >= max_retries:
        log_progress(f"STOP: Story {story['id']} exceeded max_retries ({max_retries})")
        story["status"] = "failed"
        save_prd(prd)
        return 1

    test_file = story.get("test_file")
    if test_file and not Path(test_file).exists():
        story["retries"] = current_retries + 1
        log_progress(f"FAIL: Story {story['id']} - test_file {test_file} does not exist")
        save_prd(prd)
        print(f"Test file missing: {test_file}")
        return 1

    command = story["verification"]
    success, output = run_verification(command)

    if not success:
        story["retries"] = current_retries + 1
        log_progress(f"FAIL: Story {story['id']} verification failed\nOutput: {output}")
        save_prd(prd)
        print(f"Verification failed: {command}")
        return 1

    story["status"] = "completed"
    log_progress(f"COMPLETE: Story {story['id']} - {story['title']}")
    save_prd(prd)
    print(f"Story {story['id']} completed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
