#!/usr/bin/env python3
"""
Test script to simulate Alphabot webhook calls
"""

import requests
import json
import hashlib
import hmac
import time

def create_test_webhook_payload():
    """Create a test webhook payload for raffle:active event"""
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    
    payload = {
        "event": "raffle:active",
        "timestamp": timestamp,
        "hash": "test_hash",  # Will be calculated below
        "data": {
            "raffle": {
                "id": "test_raffle_123",
                "slug": "test-raffle-slug",
                "name": "Test Raffle",
                "description": "A test raffle for webhook testing",
                "type": "raffle",
                "status": "active",
                "visibility": "public",
                "startDate": timestamp,
                "endDate": timestamp + (24 * 60 * 60 * 1000),  # 24 hours later
                "winnerCount": 1,
                "bannerImageUrl": "https://example.com/banner.jpg",
                "blockchain": "ETH",
                "twitterUrl": "https://twitter.com/test",
                "discordUrl": "https://discord.gg/test",
                "entryCount": 0,
                "registering": "string",
                "projectId": "test_project",
                "teamId": "test_team",
                "dtc": True,
                "requirePremium": False,
                "connectDiscord": True,
                "connectTwitter": False,
                "connectWallet": False,
                "connectEmail": False,
                "connectTelegram": False,
                "connectPassword": False,
                "connectCaptcha": False,
                "signWallet": False,
                "excludePreviousWinners": False,
                "requiredTokens": [],
                "discordServerRoles": [],
                "twitterFollows": [],
                "users": {
                    "id": "test_user",
                    "address": "test_address",
                    "connections": []
                }
            }
        }
    }
    
    return payload

def calculate_webhook_hash(event, timestamp, secret="test_webhook_secret"):
    """Calculate the webhook hash for verification"""
    message = f"{event}\n{timestamp}"
    return hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def test_webhook_endpoint(url="http://localhost:5000/webhook/alphabot"):
    """Test the webhook endpoint with a simulated payload"""
    payload = create_test_webhook_payload()
    
    # Calculate the correct hash
    payload["hash"] = calculate_webhook_hash(
        payload["event"], 
        payload["timestamp"]
    )
    
    print("Testing webhook endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the webhook endpoint. Is the server running?")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

def test_invalid_webhook(url="http://localhost:5000/webhook/alphabot"):
    """Test the webhook endpoint with an invalid hash"""
    payload = create_test_webhook_payload()
    payload["hash"] = "invalid_hash"
    
    print("\nTesting webhook endpoint with invalid hash...")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 401:
            print("✅ Invalid webhook correctly rejected!")
        else:
            print("❌ Invalid webhook was not rejected!")
            
    except Exception as e:
        print(f"❌ Error testing invalid webhook: {e}")

if __name__ == "__main__":
    print("Alphabot Webhook Test Script")
    print("=" * 40)
    
    # Test valid webhook
    test_webhook_endpoint()
    
    # Test invalid webhook
    test_invalid_webhook()
    
    print("\nTest completed!")

