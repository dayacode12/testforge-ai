#!/usr/bin/env python3
"""
Quick test to verify all services are connected and pipeline can run
Run this before creating the Jenkins job
"""
import requests
import subprocess
import sys
from datetime import datetime

def test_service(name, url, timeout=5):
    """Test if a service is reachable"""
    try:
        response = requests.get(url, timeout=timeout)
        print(f"✅ {name}: {url} - {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ {name}: {url} - {str(e)}")
        return False

def test_docker():
    """Test if Docker is available"""
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Docker: Available")
            return True
        else:
            print(f"❌ Docker: Not accessible")
            return False
    except Exception as e:
        print(f"❌ Docker: {str(e)}")
        return False

def test_network():
    """Test if shared-network exists"""
    try:
        result = subprocess.run(
            ["docker", "network", "inspect", "shared-network"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Docker Network: shared-network exists")
            return True
        else:
            print(f"❌ Docker Network: shared-network not found")
            return False
    except Exception as e:
        print(f"❌ Docker Network: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print("🔍 JENKINS PIPELINE READINESS CHECK")
    print("="*70 + "\n")
    
    print("Testing Services:\n")
    
    checks = {
        "Jenkins": test_service("Jenkins", "http://localhost:8080/login", timeout=5),
        "Ollama": test_service("Ollama", "http://localhost:11434/", timeout=5),
        "TestForge-AI": test_service("TestForge-AI", "http://localhost:8001/", timeout=5),
        "Docker": test_docker(),
        "Shared Network": test_network(),
    }
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = sum(checks.values())
    total = len(checks)
    
    for service, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {service}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🚀 All systems ready! You can now:")
        print("   1. Go to http://localhost:8080")
        print("   2. Click 'New Item'")
        print("   3. Name: testforge-ai-pipeline")
        print("   4. Type: Pipeline")
        print("   5. Configure with Git + Jenkinsfile")
        print("   6. Click 'Build Now'")
    else:
        print("\n⚠️  Some services are not ready. Please check:")
        for service, status in checks.items():
            if not status:
                print(f"   - {service}")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
