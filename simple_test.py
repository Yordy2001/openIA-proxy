#!/usr/bin/env python3
"""
Simple direct test of OpenAI API
"""

import openai
import os

def test_direct_openai():
    """Test OpenAI directly without config dependencies"""
    print("🔍 Testing OpenAI API Directly")
    print("=" * 40)
    
    # Check for API key in environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set: export OPENAI_API_KEY='your-key-here'")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Create client directly
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
        
        # Test simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the cheaper model
            messages=[
                {"role": "user", "content": "Responde solo con: TEST OK"}
            ],
            max_tokens=10,
            temperature=0
        )
        
        if response.choices and response.choices[0].message.content:
            result = response.choices[0].message.content.strip()
            print(f"✅ OpenAI Response: '{result}'")
            
            if "TEST OK" in result.upper():
                print("🎉 OpenAI is working correctly!")
                return True
            else:
                print("⚠️ Unexpected response format")
                return False
        else:
            print("❌ No response content received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    test_direct_openai() 