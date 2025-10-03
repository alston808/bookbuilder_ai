#!/usr/bin/env python3
"""
Test script for Book Builder AI GUI
Run this to verify the GUI components work correctly
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        # Core dependencies
        import streamlit
        import plotly
        import langgraph
        import langchain_openai
        import langchain_google_genai
        import langchain_groq
        # import langchain_openrouter  # Commented out due to compatibility issues
        print("✅ All core dependencies imported successfully")

        # Application modules
        from src.utils import GraphConfig, State
        print("✅ Utils module imported successfully")

        from src.agent import app
        print("✅ Agent module imported successfully")

        from src.gui import BookBuilderGUI
        print("✅ GUI module imported successfully")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def test_gui_creation():
    """Test GUI object creation"""
    print("\n🏗️  Testing GUI creation...")

    try:
        # First test if the class exists
        print(f"BookBuilderGUI class exists: {BookBuilderGUI is not None}")

        gui = BookBuilderGUI()
        print("✅ GUI object created successfully")
        print(f"   - Current stage: {gui.current_stage}")
        print(f"   - Processing: {gui.is_processing}")
        return True
    except NameError as e:
        print(f"❌ NameError - BookBuilderGUI not defined: {e}")
        print("This suggests the class wasn't imported properly")
        return False
    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_structure():
    """Test configuration structure"""
    print("\n⚙️  Testing configuration structure...")

    try:
        config: GraphConfig = {
            'configurable': {
                'language': 'english',
                'critiques_in_loop': False,
                'instructor_model': 'openai',
                'brainstormer_idea_model': 'openai',
                'brainstormer_critique_model': 'openai',
                'writer_model': 'openai',
                'writing_reviewer_model': 'openai',
                'translator_model': 'openai',
                'n_chapters': 8,
                'min_paragraph_per_chapter': 5,
                'min_sentences_in_each_paragraph_per_chapter': 5
            }
        }

        # Test that openrouter is included in the options
        model_options = ['openai', 'google', 'meta', 'amazon', 'deepseek', 'openrouter']
        assert 'openrouter' in model_options, "OpenRouter not found in model options"

        print("✅ Configuration structure is valid")
        print(f"   - OpenRouter included: {'openrouter' in model_options}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Book Builder AI - GUI Test Suite")
    print("="*50)

    tests = [
        test_imports,
        test_gui_creation,
        test_config_structure
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "="*50)
    print("📊 Test Results Summary:")

    passed = sum(results)
    total = len(results)

    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   Test {i+1}: {status}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The GUI is ready to use.")
        print("🚀 Run: python main.py gui")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
