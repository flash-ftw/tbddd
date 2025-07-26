import os
import json
import hmac
import hashlib
import asyncio
import logging
from flask import Blueprint, request, jsonify

from src.alphabot_client import AlphabotClient
from src.user_storage import UserStorage

webhook_bp = Blueprint("webhook", __name__)

logger = logging.getLogger(__name__)

# Initialize AlphabotClient and UserStorage
alphabot_client = AlphabotClient()
user_storage = UserStorage()

@webhook_bp.route("/alphabot", methods=["POST"])
async def alphabot_webhook():
    logger.info("Received Alphabot webhook")
    
    try:
        payload = request.get_json()
    except Exception as e:
        logger.error(f"Invalid JSON payload: {e}")
        return jsonify({"error": "Invalid JSON"}), 400

    event = payload.get("event")
    timestamp = payload.get("timestamp")
    received_hash = payload.get("hash")

    if event == "raffle:active":
        raffle_data = payload.get("data", {}).get("raffle")
        if raffle_data:
            raffle_slug = raffle_data.get("slug")
            raffle_name = raffle_data.get("name")
            logger.info(f"Raffle \'{raffle_name}\' ({raffle_slug}) is active. Attempting to register users.")
            
            all_users = user_storage.get_all_users()
            if not all_users:
                logger.info("No users registered to join raffles.")
                return jsonify({"status": "success", "message": "No users registered"}), 200

            for discord_id, api_key in all_users.items():
                logger.info(f"Attempting to register user {discord_id} for raffle {raffle_slug}")
                result = await alphabot_client.register_for_raffle(
                    api_key=api_key,
                    raffle_slug=raffle_slug,
                    discord_id=discord_id
                )
                if result.get("success"):
                    logger.info(f"Successfully registered user {discord_id} for raffle {raffle_slug}")
                    # TODO: Send Discord DM to user about successful entry
                else:
                    error_message = result.get("error", "Unknown error")
                    logger.error(f"Failed to register user {discord_id} for raffle {raffle_slug}: {error_message}")
                    # TODO: Send Discord DM to user about failed entry
        else:
            logger.warning("raffle:active event received but no raffle data found.")
    else:
        logger.info(f"Unhandled event type: {event}")

    return jsonify({"status": "success"}), 200

