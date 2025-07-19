"""
API Key Testing Utility for AI Music Agent

This script helps users validate their OpenAI and ModelsLab API keys
before using the AI Music Agent application.
"""

import openai
import requests


def test_internet_connection():
    """Test internet connectivity."""
    print("--- Checking Internet Connection ---")
    try:
        requests.get("https://www.google.com", timeout=5)
        print("✅ Internet connection is working.\n")
        return True
    except Exception as e:
        print(f"❌ Internet connection issue: {e}")
        return False


def test_openai_api_key(api_key):
    """Test OpenAI API key validity."""
    print("\n--- Testing OpenAI API Key ---")
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.models.list()
        models = [m.id for m in response.data]
        print(f"✅ OpenAI API key is valid! Available models: {len(models)} total")
        print(f"   Sample models: {models[:3]}...")
        return True
    except Exception as e:
        print(f"❌ OpenAI API key is invalid or there is a connection issue: {e}")
        return False


def test_modelslab_api_key(api_key):
    """Test ModelsLab API key validity."""
    print("\n--- Testing ModelsLab API Key ---")
    headers = {"Authorization": f"Bearer {api_key}"}
    test_url = "https://modelslab.com/api/v6/"  # Base endpoint for connectivity

    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            print("✅ ModelsLab API key is likely valid!")
            return True
        elif response.status_code in [401, 403]:
            print("❌ ModelsLab API key is invalid or unauthorized.")
            return False
        else:
            print(f"⚠️  Received unexpected response: {response.status_code}")
            print("   Check ModelsLab API documentation for valid test endpoint.")
            return False

    except Exception as e:
        print(f"❌ Error connecting to ModelsLab API: {e}")
        return False


def main():
    """Main function to run API key tests."""
    print("🔑 AI Music Agent - API Key Validation Utility")
    print("=" * 50)

    # Test internet connection first
    if not test_internet_connection():
        print("\n❌ Cannot proceed without internet connection.")
        return

    # Get API keys from user
    print("Please provide your API keys for testing:")
    openai_api_key = input("Enter your OpenAI API Key: ").strip()
    modelslab_api_key = input("Enter your ModelsLab API Key: ").strip()

    if not openai_api_key or not modelslab_api_key:
        print("❌ Both API keys are required for testing.")
        return

    # Test both API keys
    openai_valid = test_openai_api_key(openai_api_key)
    modelslab_valid = test_modelslab_api_key(modelslab_api_key)

    # Summary
    print("\n" + "=" * 50)
    print("🔍 API Key Validation Summary:")
    print(f"   OpenAI API Key: {'✅ Valid' if openai_valid else '❌ Invalid'}")
    print(f"   ModelsLab API Key: {'✅ Valid' if modelslab_valid else '❌ Invalid'}")

    if openai_valid and modelslab_valid:
        print("\n🎉 All API keys are valid! You can now use the AI Music Agent.")
    else:
        print("\n⚠️  Please fix the invalid API keys before using the AI Music Agent.")


if __name__ == "__main__":
    main()
