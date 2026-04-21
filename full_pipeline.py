#!/usr/bin/env python3
"""
Complete automated CI/CD pipeline simulation
Demonstrates: Git clone → Build → Test → Error Analysis → Fix Suggestions
"""
import subprocess
import json
import requests
import sys
from datetime import datetime

OLLAMA_API = "http://ollama:11434/api/generate"
TESTFORGE_API = "http://test-awesome:8000"

def print_header(title):
    print("\n" + "="*75)
    print(f"🚀 {title}")
    print("="*75 + "\n")

def run_build_script():
    """Execute the build script and capture output"""
    print_header("JENKINS BUILD JOB #42 - Running automated tests")
    
    try:
        result = subprocess.run(
            [sys.executable, "build_script.py"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd="."
        )
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return f"Build execution failed: {e}", 1

def send_to_ollama_for_analysis(error_logs):
    """Send error logs to Ollama for AI-powered analysis"""
    print_header("SENDING ERROR LOGS TO OLLAMA FOR AI ANALYSIS")
    
    prompt = f"""You are a senior DevOps/QA engineer. Analyze these test failures:

TEST OUTPUT:
{error_logs}

For EACH error, provide:
1. Root cause
2. Specific code fix
3. How to prevent it

Format your response clearly with bullet points."""

    try:
        print(f"📤 Connecting to Ollama at {OLLAMA_API}...")
        response = requests.post(
            OLLAMA_API,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        
        if response.status_code == 200:
            analysis = response.json().get("response", "")
            return analysis
        else:
            return f"⚠️ Ollama returned error {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to Ollama at http://ollama:11434. Is it running?"
    except requests.exceptions.Timeout:
        return "⚠️ Ollama took too long to respond (timeout)"
    except Exception as e:
        return f"❌ Error communicating with Ollama: {e}"

def send_to_testforge_for_test_generation(feature):
    """Send feature request to testforge-ai for test case generation"""
    print_header("BONUS: GENERATING TEST CASES VIA TESTFORGE-AI")
    
    try:
        print(f"📤 Connecting to testforge-ai at {TESTFORGE_API}/generate-tests...")
        response = requests.post(
            f"{TESTFORGE_API}/generate-tests",
            json={"feature_description": feature},
            timeout=180
        )
        
        if response.status_code == 200:
            test_cases = response.json().get("test_cases", [])
            return test_cases
        else:
            return f"⚠️ TestForge returned error {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to testforge-ai at http://test-awesome:8000. Is it running?"
    except requests.exceptions.Timeout:
        return "⚠️ TestForge took too long to respond (timeout)"
    except Exception as e:
        return f"❌ Error communicating with testforge-ai: {e}"

def display_fixes(analysis):
    """Parse and display the Ollama analysis in a readable format"""
    print("\n" + "█"*75)
    print("█ 🔧 OLLAMA'S AI RECOMMENDATIONS")
    print("█"*75)
    print(analysis)
    print("█"*75 + "\n")

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "╔"*75)
    print("║ 🚀 FULL CI/CD PIPELINE WITH AI-POWERED ERROR ANALYSIS")
    print("║ Started:", timestamp)
    print("╚"*75)
    
    # Step 1: Run build and capture errors
    build_output, exit_code = run_build_script()
    print(build_output)
    
    if exit_code != 0:
        print("\n⚠️  BUILD FAILED - Tests did not pass")
        print("\n" + "="*75)
        print("📊 Test Results Summary:")
        print("="*75)
        if "Results:" in build_output:
            for line in build_output.split("\n"):
                if "Results:" in line or "ERROR:" in line or "test" in line.lower():
                    print(f"  {line}")
        
        print("\n" + "─"*75)
        print("Sending errors to Ollama for root cause analysis...")
        print("─"*75)
        
        # Step 2: Send errors to Ollama for AI analysis
        analysis = send_to_ollama_for_analysis(build_output)
        display_fixes(analysis)
        
    else:
        print("\n✅ BUILD SUCCESSFUL - All tests passed!")
    
    # Step 3: Generate test cases for a new feature
    print_header("FEATURE: Generate test cases for authentication module")
    
    feature_desc = "User authentication system with email validation, password strength checking, and multi-factor authentication support"
    test_cases = send_to_testforge_for_test_generation(feature_desc)
    
    if isinstance(test_cases, list) and len(test_cases) > 0:
        print(f"✅ Generated {len(test_cases)} test case(s):\n")
        for i, tc in enumerate(test_cases[:3], 1):
            if isinstance(tc, dict):
                desc = tc.get('description', str(tc))
            else:
                desc = str(tc)
            print(f"   Test {i}: {desc}")
    else:
        print(f"⚠️ {test_cases}")
    
    print("\n" + "╔"*75)
    print("║ ✨ PIPELINE EXECUTION COMPLETE")
    print("║ All stages finished: Build → Test → Analyze → Generate")
    print("╚"*75 + "\n")

if __name__ == "__main__":
    main()
