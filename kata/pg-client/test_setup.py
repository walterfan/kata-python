#!/usr/bin/env python3
"""Simple test script to verify PostgreSQL connection setup."""

def test_imports():
    """Test if all required modules can be imported."""
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        from dotenv import load_dotenv
        from rich.console import Console
        print("✓ All required modules imported successfully!")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please run: poetry install")
        return False

def test_config():
    """Test configuration loading."""
    try:
        from config import get_database_config, get_connection_string
        config = get_database_config()
        print(f"✓ Configuration loaded: {config['host']}:{config['port']}/{config['database']}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing PostgreSQL Python Client Setup")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Test", test_config),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Ready to run main.py")
    else:
        print("❌ Some tests failed. Please check the setup.")

if __name__ == "__main__":
    main()
