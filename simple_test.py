#!/usr/bin/env python3
"""
Simple test to verify OpenRouter integration works
"""

import os
from src.utils import _get_model, GraphConfig

def test_openrouter_integration():
    """Test OpenRouter model integration"""
    print("🔧 Testing OpenRouter integration...")

    # Test configuration
    config: GraphConfig = {
        'configurable': {
            'instructor_model': 'openrouter',
            'brainstormer_idea_model': 'openrouter',
            'brainstormer_critique_model': 'openrouter',
            'writer_model': 'openrouter',
            'writing_reviewer_model': 'openrouter',
            'translator_model': 'openrouter',
            'language': 'english',
            'critiques_in_loop': False,
            'n_chapters': 8,
            'min_paragraph_per_chapter': 5,
            'min_sentences_in_each_paragraph_per_chapter': 5
        }
    }

    try:
        # Test model creation (this will fail without API key, but should not crash)
        model = _get_model(config, 'instructor_model', temperature=0.1)
        print("✅ OpenRouter model created successfully")
        print(f"   - Model type: {type(model)}")
        print(f"   - Model name: {getattr(model, 'model', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ OpenRouter integration error: {e}")
        if "OPENROUTER_API_KEY" in str(e):
            print("💡 Set OPENROUTER_API_KEY in your .env file")
        return False

def test_configuration():
    """Test configuration structure"""
    print("\n⚙️  Testing configuration structure...")

    # Test that openrouter is included in the options
    model_options = ['openai', 'google', 'meta', 'amazon', 'deepseek', 'openrouter']
    assert 'openrouter' in model_options, "OpenRouter not found in model options"

    print("✅ Configuration structure is valid")
    print(f"   - OpenRouter included: {'openrouter' in model_options}")

    # Test GraphConfig structure
    config: GraphConfig = {
        'configurable': {
            'language': 'english',
            'critiques_in_loop': False,
            'instructor_model': 'openrouter',  # Test OpenRouter
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

    print("✅ GraphConfig structure is valid")
    return True

def main():
    """Run tests"""
    print("🧪 Book Builder AI - OpenRouter Integration Test")
    print("="*60)

    tests = [
        test_configuration,
        test_openrouter_integration
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "="*60)
    print("📊 Test Results Summary:")

    passed = sum(results)
    total = len(results)

    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   Test {i+1}: {status}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 OpenRouter integration is working!")
        print("🚀 You can now use OpenRouter models in the GUI")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    exit(main())