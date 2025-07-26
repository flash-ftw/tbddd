import requests
import logging
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AlphabotClient:
    """Client for interacting with the Alphabot API"""
    
    BASE_URL = "https://api.alphabot.app/v1"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AlphabotDiscordBot/1.0'
        })
    
    def register_for_raffle(self, api_key: str, raffle_slug: str, discord_id: str, 
                          mint_address: Optional[str] = None, 
                          twitter_id: Optional[str] = None,
                          telegram_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Register a user for a raffle
        
        Args:
            api_key: User's Alphabot API key
            raffle_slug: Unique identifier of the raffle
            discord_id: User's Discord ID
            mint_address: Optional mint address
            twitter_id: Optional Twitter ID
            telegram_id: Optional Telegram ID
            
        Returns:
            Dict containing the API response
        """
        url = f"{self.BASE_URL}/register"
        
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        payload = {
            'slug': raffle_slug,
            'discordId': discord_id
        }
        
        # Add optional fields if provided
        if mint_address:
            payload['mintAddress'] = mint_address
        if twitter_id:
            payload['twitterId'] = twitter_id
        if telegram_id:
            payload['telegramId'] = telegram_id
        
        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited, waiting {retry_after} seconds")
                time.sleep(retry_after)
                # Retry once after rate limit
                response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            # Parse response
            try:
                result = response.json()
            except ValueError:
                result = {"error": "Invalid JSON response", "status_code": response.status_code}
            
            # Add status code to result
            result['status_code'] = response.status_code
            
            if response.status_code == 200:
                logger.info(f"Successfully registered for raffle {raffle_slug}")
            else:
                logger.warning(f"Failed to register for raffle {raffle_slug}: {result}")
            
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while registering for raffle {raffle_slug}")
            return {"error": "Request timeout", "success": False}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while registering for raffle {raffle_slug}: {e}")
            return {"error": str(e), "success": False}
        except Exception as e:
            logger.error(f"Unexpected error while registering for raffle {raffle_slug}: {e}")
            return {"error": str(e), "success": False}
    
    def get_raffle_info(self, api_key: str, raffle_slug: str) -> Dict[str, Any]:
        """
        Get information about a specific raffle
        
        Args:
            api_key: Alphabot API key
            raffle_slug: Unique identifier of the raffle
            
        Returns:
            Dict containing the raffle information
        """
        url = f"{self.BASE_URL}/raffles/{raffle_slug}"
        
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=30)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited, waiting {retry_after} seconds")
                time.sleep(retry_after)
                response = self.session.get(url, headers=headers, timeout=30)
            
            try:
                result = response.json()
            except ValueError:
                result = {"error": "Invalid JSON response", "status_code": response.status_code}
            
            result['status_code'] = response.status_code
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting raffle info for {raffle_slug}: {e}")
            return {"error": str(e), "success": False}

