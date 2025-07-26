#!/usr/bin/env python3
"""
Test Runner Script for Gmail Automation
Provides easy ways to run different test suites with HTML reporting
"""

import subprocess
import sys
import os
from datetime import datetime


def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False


def install_dependencies():
    """Install required dependencies"""
    return run_command([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ], "Installing dependencies")


def run_all_tests():
    """Run all tests with HTML reporting"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/gmail_automation_report_{timestamp}.html"
    
    return run_command([
        sys.executable, "-m", "pytest", 
        "test_gmail_automation.py",
        "--html", report_file,
        "--self-contained-html",
        "-v"
    ], f"Running all tests (Report: {report_file})")


def run_quick_tests():
    """Run quick tests only (excluding slow tests)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/gmail_quick_tests_{timestamp}.html"
    
    return run_command([
        sys.executable, "-m", "pytest", 
        "test_gmail_automation.py",
        "-m", "not slow",
        "--html", report_file,
        "--self-contained-html",
        "-v"
    ], f"Running quick tests (Report: {report_file})")


def run_launch_only_tests():
    """Run Gmail launch-only tests"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/gmail_launch_tests_{timestamp}.html"
    
    return run_command([
        sys.executable, "-m", "pytest", 
        "test_gmail_automation.py::TestGmailLaunchOnly",
        "--html", report_file,
        "--self-contained-html",
        "-v"
    ], f"Running launch-only tests (Report: {report_file})")


def run_specific_test(test_name):
    """Run a specific test"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/gmail_specific_test_{timestamp}.html"
    
    return run_command([
        sys.executable, "-m", "pytest", 
        f"test_gmail_automation.py::{test_name}",
        "--html", report_file,
        "--self-contained-html",
        "-v"
    ], f"Running specific test: {test_name} (Report: {report_file})")


def show_test_info():
    """Show available tests"""
    print("\n📋 Available Test Commands:")
    print("="*50)
    print("1. run_tests.py --all          : Run all tests")
    print("2. run_tests.py --quick        : Run quick tests (no slow tests)")
    print("3. run_tests.py --launch-only  : Run Gmail launch tests only")
    print("4. run_tests.py --install      : Install dependencies")
    print("5. run_tests.py --info         : Show this information")
    print("6. run_tests.py --test <name>  : Run specific test")
    print("\n📊 Available Tests:")
    print("-" * 30)
    
    # List available tests
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", "-q", "test_gmail_automation.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if '::test_' in line:
                    test_name = line.strip()
                    print(f"   • {test_name}")
        else:
            print("   Could not collect test information")
    except Exception as e:
        print(f"   Error collecting tests: {e}")
    
    print(f"\n📁 Reports will be saved in: {os.path.abspath('reports')}/")
    print("\n🌐 Open the HTML report in your browser to view detailed results!")


def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        show_test_info()
        return
    
    command = sys.argv[1].lower()
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    if command == "--install":
        install_dependencies()
    elif command == "--all":
        run_all_tests()
    elif command == "--quick":
        run_quick_tests()
    elif command == "--launch-only":
        run_launch_only_tests()
    elif command == "--test" and len(sys.argv) > 2:
        test_name = sys.argv[2]
        run_specific_test(test_name)
    elif command == "--info":
        show_test_info()
    else:
        print(f"❌ Unknown command: {command}")
        show_test_info()


if __name__ == "__main__":
    print("🧪 Gmail Automation Test Runner")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
