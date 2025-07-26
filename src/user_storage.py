import json
import os
import logging
from typing import Dict, Optional
from threading import Lock

logger = logging.getLogger(__name__)

class UserStorage:
    """Simple file-based storage for user API keys"""
    
    def __init__(self, storage_file: str = None):
        if storage_file is None:
            # Default to a file in the database directory
            base_dir = os.path.dirname(__file__)
            storage_file = os.path.join(base_dir, 'database', 'user_keys.json')
        
        self.storage_file = storage_file
        self.lock = Lock()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not os.path.exists(self.storage_file):
            self._save_data({})
    
    def _load_data(self) -> Dict[str, str]:
        """Load user data from file"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Error loading user data: {e}, returning empty dict")
            return {}
    
    def _save_data(self, data: Dict[str, str]) -> None:
        """Save user data to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
            raise
    
    def set_user_api_key(self, discord_id: str, api_key: str) -> bool:
        """
        Store or update a user's API key
        
        Args:
            discord_id: User's Discord ID
            api_key: User's Alphabot API key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.lock:
                data = self._load_data()
                data[discord_id] = api_key
                self._save_data(data)
                logger.info(f"Stored API key for user {discord_id}")
                return True
        except Exception as e:
            logger.error(f"Error storing API key for user {discord_id}: {e}")
            return False
    
    def get_user_api_key(self, discord_id: str) -> Optional[str]:
        """
        Get a user's API key
        
        Args:
            discord_id: User's Discord ID
            
        Returns:
            The user's API key if found, None otherwise
        """
        try:
            with self.lock:
                data = self._load_data()
                return data.get(discord_id)
        except Exception as e:
            logger.error(f"Error getting API key for user {discord_id}: {e}")
            return None
    
    def remove_user_api_key(self, discord_id: str) -> bool:
        """
        Remove a user's API key
        
        Args:
            discord_id: User's Discord ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.lock:
                data = self._load_data()
                if discord_id in data:
                    del data[discord_id]
                    self._save_data(data)
                    logger.info(f"Removed API key for user {discord_id}")
                    return True
                else:
                    logger.warning(f"No API key found for user {discord_id}")
                    return False
        except Exception as e:
            logger.error(f"Error removing API key for user {discord_id}: {e}")
            return False
    
    def get_all_users(self) -> Dict[str, str]:
        """
        Get all stored users and their API keys
        
        Returns:
            Dict mapping Discord IDs to API keys
        """
        try:
            with self.lock:
                return self._load_data()
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return {}
    
    def user_exists(self, discord_id: str) -> bool:
        """
        Check if a user has an API key stored
        
        Args:
            discord_id: User's Discord ID
            
        Returns:
            True if user exists, False otherwise
        """
        return self.get_user_api_key(discord_id) is not None
    
    def get_user_count(self) -> int:
        """
        Get the number of registered users
        
        Returns:
            Number of users with stored API keys
        """
        try:
            with self.lock:
                data = self._load_data()
                return len(data)
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0

