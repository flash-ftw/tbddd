import hashlib
import hmac
import json
import logging
from flask import Blueprint, request, jsonify
from src.alphabot_client import AlphabotClient
from src.user_storage import UserStorage

logger = logging.getLogger(__name__)
webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/alphabot', methods=['POST'])
def handle_alphabot_webhook():
    """Handle incoming Alphabot webhooks"""
    try:
        # Get the raw request data
        raw_data = request.get_data()
        
        # Parse JSON data
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook request")
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Verify webhook authenticity
        if not verify_webhook(data, raw_data):
            logger.error("Webhook verification failed")
            return jsonify({"error": "Unauthorized"}), 401
        
        # Process the webhook based on event type
        event = data.get('event')
        if event == 'raffle:active':
            process_raffle_active(data)
        else:
            logger.info(f"Received unhandled webhook event: {event}")
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": "Internal server error"}), 500

def verify_webhook(data, raw_data):
    """Verify the webhook authenticity using HMAC"""
    try:
        # Get the webhook secret from environment
        import os
        webhook_secret = os.environ.get('ALPHABOT_WEBHOOK_SECRET')
        if not webhook_secret:
            logger.warning("No webhook secret configured, skipping verification")
            return True  # Allow for development without secret
        
        # Extract hash from data
        received_hash = data.get('hash')
        if not received_hash:
            return False
        
        # Create expected hash
        event = data.get('event', '')
        timestamp = str(data.get('timestamp', ''))
        message = f"{event}\n{timestamp}"
        
        expected_hash = hmac.new(
            webhook_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(received_hash, expected_hash)
        
    except Exception as e:
        logger.error(f"Error verifying webhook: {e}")
        return False

def process_raffle_active(data):
    """Process a raffle:active webhook"""
    try:
        raffle_data = data.get('data', {}).get('raffle', {})
        raffle_slug = raffle_data.get('slug')
        raffle_name = raffle_data.get('name', 'Unknown Raffle')
        
        if not raffle_slug:
            logger.error("No raffle slug found in webhook data")
            return
        
        logger.info(f"Processing raffle:active for '{raffle_name}' (slug: {raffle_slug})")
        
        # Get all registered users
        user_storage = UserStorage()
        users = user_storage.get_all_users()
        
        if not users:
            logger.info("No users registered, skipping raffle processing")
            return
        
        # Process each user
        alphabot_client = AlphabotClient()
        for user_id, api_key in users.items():
            try:
                result = alphabot_client.register_for_raffle(
                    api_key=api_key,
                    raffle_slug=raffle_slug,
                    discord_id=user_id
                )
                
                if result.get('success'):
                    logger.info(f"Successfully registered user {user_id} for raffle {raffle_slug}")
                    # TODO: Send success message to Discord user
                else:
                    logger.warning(f"Failed to register user {user_id} for raffle {raffle_slug}: {result}")
                    # TODO: Send failure message to Discord user
                    
            except Exception as e:
                logger.error(f"Error registering user {user_id} for raffle {raffle_slug}: {e}")
                # TODO: Send error message to Discord user
        
    except Exception as e:
        logger.error(f"Error processing raffle:active webhook: {e}")

