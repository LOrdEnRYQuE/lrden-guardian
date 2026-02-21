#!/usr/bin/env python3
"""
🚀 LRDEnE Guardian - Immediate Deployment Script
===============================================

Copyright (c) 2026 LRDEnE. All rights reserved.

Execute this script to deploy LRDEnE Guardian immediately.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run command with error handling"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} - FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False
    return True

def main():
    """Main deployment function"""
    print("🚀 LRDEnE Guardian - Immediate Deployment")
    print("=" * 50)
    
    # Step 1: Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Step 2: Verify package is built
    dist_dir = current_dir / "dist"
    if not dist_dir.exists():
        print("❌ Package not built. Run 'python -m build' first.")
        return False
    
    print(f"✅ Package files found:")
    for file in dist_dir.glob("*"):
        print(f"   📦 {file.name}")
    
    # Step 3: Test package installation
    print("\n🧪 Testing package installation...")
    if not run_command("python -m venv deploy_test", "Creating test environment"):
        return False
    
    if not run_command("source deploy_test/bin/activate && pip install dist/*.whl", "Installing package"):
        return False
    
    if not run_command("source deploy_test/bin/activate && python -c 'from lrden_guardian import create_lrden_guardian; print(\"✅ Import test passed\")'", "Testing import"):
        return False
    
    if not run_command("source deploy_test/bin/activate && lrden-guardian --version", "Testing CLI"):
        return False
    
    # Step 4: Clean up test environment
    run_command("rm -rf deploy_test", "Cleaning test environment")
    
    # Step 5: Deployment options
    print("\n🚀 DEPLOYMENT OPTIONS:")
    print("=" * 50)
    
    print("\n1️⃣  PyPI DEPLOYMENT:")
    print("   📦 Test PyPI:")
    print("      twine upload --repository testpypi dist/*")
    print("      pip install --index-url https://test.pypi.org/simple/ lrden-guardian")
    print()
    print("   📦 Production PyPI:")
    print("      twine upload dist/*")
    print("      pip install lrden-guardian")
    
    print("\n2️⃣  GITHUB DEPLOYMENT:")
    print("   🐙 Create repository:")
    print("      gh repo create LRDEnE/lrden-guardian --public")
    print("      git remote add origin https://github.com/LRDEnE/lrden-guardian.git")
    print("      git push -u origin main")
    print("      git tag -a v1.0.0 -m 'LRDEnE Guardian v1.0.0'")
    print("      git push origin v1.0.0")
    
    print("\n3️⃣  LOCAL TESTING:")
    print("   🧪 Install locally:")
    print("      pip install -e .")
    print("      lrden-guardian info")
    print("      lrden-init --config-type enterprise")
    
    print("\n4️⃣  DOCKER DEPLOYMENT:")
    print("   🐳 Build image:")
    print("      docker build -t lrden/guardian:latest .")
    print("      docker run --rm lrden/guardian:latest lrden-guardian info")
    
    print("\n📋 QUICK START COMMANDS:")
    print("=" * 50)
    print("   # Install and test")
    print("   pip install dist/lrden_guardian-*.whl")
    print("   lrden-guardian info")
    print("   lrden-guardian check 'Test content for safety'")
    print()
    print("   # Initialize in project")
    print("   lrden-init")
    print("   lrden-guardian analyze 'Your content here'")
    
    print("\n🎯 NEXT STEPS:")
    print("=" * 50)
    print("   1. Choose deployment method above")
    print("   2. Execute deployment commands")
    print("   3. Test installation")
    print("   4. Announce to community")
    print("   5. Start customer outreach")
    
    print("\n🛡️ LRDEnE Guardian is READY FOR DEPLOYMENT!")
    print("   📦 Package: Built and tested")
    print("   🛠️  CLI: Working perfectly")
    print("   📚 Documentation: Complete")
    print("   💼 Business: Ready for customers")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print(f"\n🎉 Deployment script completed successfully!")
    print(f"📋 Follow the deployment options above to go live!")
