#!/usr/bin/env python3
"""
Jenkins build job simulator
Runs tests, captures errors, sends to Ollama for analysis
"""
import subprocess
import json
import requests
import sys
from datetime import datetime

OLLAMA_API = "http://ollama:11434/api/generate"
TESTFORGE_API = "http://test-awesome:8000"

def run_build_script():
    """Execute the build script and capture output"""
    print("\n" + "="*70)
    print("📦 JENKINS BUILD JOB #42 - Running automated tests")
    print("="*70 + "\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "build_script.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return f"Build execution failed: {e}", 1

def send_to_ollama_for_analysis(error_logs):
    """Send error logs to Ollama for AI-powered analysis"""
    print("\n" + "="*70)
    print("🤖 SENDING ERROR LOGS TO OLLAMA FOR ANALYSIS")
    print("="*70 + "\n")
    
    prompt = f"""You are a senior DevOps/QA engineer. Analyze these test failures and provide fixes:

TEST OUTPUT:
{error_logs}

Provide:
1. Root cause of each failure
2. Specific fix for each issue
3. Prevention tips

Be concise and actionable."""

    try:
        print(f"📤 Sending to Ollama at {OLLAMA_API}...")
        response = requests.post(
            OLLAMA_API,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code == 200:
            analysis = response.json().get("response", "")
            return analysis
        else:
            return f"Ollama error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to Ollama. Make sure it's running on http://ollama:11434"
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

def send_to_testforge_for_test_generation(feature):
    """Send feature request to testforge-ai for test case generation"""
    print("\n" + "="*70)
    print("🧪 GENERATING TEST CASES VIA TESTFORGE-AI")
    print("="*70 + "\n")
    
    try:
        print(f"📤 Sending to testforge-ai at {TESTFORGE_API}/generate-tests...")
        response = requests.post(
            f"{TESTFORGE_API}/generate-tests",
            json={"feature_description": feature},
            timeout=120
        )
        
        if response.status_code == 200:
            test_cases = response.json().get("test_cases", [])
            return test_cases
        else:
            return f"TestForge error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to testforge-ai. Make sure it's running on http://test-awesome:8000"
    except Exception as e:
        return f"Error communicating with testforge-ai: {e}"

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🚀 Automated CI/CD Pipeline Started at {timestamp}")
    
    # Step 1: Run build and capture errors
    build_output, exit_code = run_build_script()
    print(build_output)
    
    if exit_code != 0:
        print("\n⚠️  BUILD FAILED - Tests did not pass")
        print("\nSending error logs to Ollama AI for analysis...")
        
        # Step 2: Send errors to Ollama for AI analysis
        analysis = send_to_ollama_for_analysis(build_output)
        print("\n" + "="*70)
        print("🔧 OLLAMA'S AI ANALYSIS AND RECOMMENDATIONS:")
        print("="*70)
        print(analysis)
        
    else:
        print("\n✅ BUILD SUCCESSFUL - All tests passed!")
    
    # Step 3: Generate test cases for a new feature (independent of build result)
    print("\n\n" + "="*70)
    print("📋 BONUS: Generating test cases for new feature")
    print("="*70)
    
    feature_desc = "User authentication with email and password validation"
    test_cases = send_to_testforge_for_test_generation(feature_desc)
    
    if isinstance(test_cases, list):
        print(f"\n✅ Generated {len(test_cases)} test cases:")
        for i, tc in enumerate(test_cases[:3], 1):  # Show first 3
            print(f"\n  Test {i}: {tc.get('description', tc)}")
    else:
        print(f"\n{test_cases}")
    
    print("\n" + "="*70)
    print("✨ Pipeline execution complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
