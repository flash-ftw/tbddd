# Alphabot Discord Bot

A Discord bot that automatically enters users into Alphabot raffles when they become active. Users can register their personal Alphabot API keys with the bot, and it will automatically attempt to join raffles on their behalf when webhooks are received.

## Features

- **Automatic Raffle Entry**: Automatically joins users in raffles when they become active
- **Webhook Integration**: Receives real-time notifications from Alphabot when raffles go live
- **User Management**: Users can register/remove their personal API keys
- **Manual Raffle Joining**: Users can manually join specific raffles by slug
- **Secure Storage**: User API keys are stored securely on the server
- **Error Handling**: Comprehensive error handling and user notifications

## Discord Commands

- `!setapikey <your_key>` - Register your personal Alphabot API key
- `!removekey` - Remove your stored API key
- `!status` - Check your registration status and see total user count
- `!joinraffle <slug>` - Manually join a specific raffle
- `!help` - Show all available commands

## Setup Instructions

### Prerequisites

1. **Discord Bot**: Create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. **Alphabot API Key**: Get your team's Alphabot API key from your team page
3. **Webhook Secret**: Configure webhook secret in Alphabot settings

### Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
ALPHABOT_TEAM_API_KEY=your_team_alphabot_api_key_here
ALPHABOT_WEBHOOK_SECRET=your_webhook_secret_here
SECRET_KEY=your_flask_secret_key_here
PORT=5000
```

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   cd alphabot-discord-bot
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`
4. Run the application:
   ```bash
   python src/main.py
   ```

### Railway Deployment

1. **Connect GitHub Repository**:
   - Create a new project on Railway
   - Connect your GitHub repository

2. **Set Environment Variables**:
   - Go to your Railway project settings
   - Add all environment variables from `.env.example`

3. **Configure Webhook URL**:
   - After deployment, get your Railway app URL
   - Set the webhook URL in Alphabot to: `https://your-app.railway.app/webhook/alphabot`

4. **Deploy**:
   - Railway will automatically deploy when you push to your main branch

## Architecture

The bot consists of several components:

- **Flask Web Server**: Handles incoming webhooks from Alphabot
- **Discord Bot**: Manages Discord interactions and commands
- **User Storage**: Stores user API keys securely
- **Alphabot Client**: Handles API calls to Alphabot
- **Webhook Processor**: Processes incoming raffle notifications

## How It Works

1. **User Registration**: Users register their personal Alphabot API keys using `!setapikey`
2. **Webhook Reception**: When a raffle becomes active, Alphabot sends a webhook to the bot
3. **Automatic Entry**: The bot retrieves all registered users and attempts to enter them in the raffle
4. **Notifications**: Users receive notifications about successful/failed entries

## Security Notes

- User API keys are stored in a local JSON file (for production, consider using encrypted database storage)
- Webhook requests are verified using HMAC signatures
- API keys in Discord messages are automatically deleted for security
- All sensitive configuration is handled via environment variables

## Rate Limiting

The bot handles Alphabot's rate limits automatically:
- Implements retry logic with exponential backoff
- Respects `Retry-After` headers from the API
- Logs rate limit events for monitoring

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check that `DISCORD_BOT_TOKEN` is correct and the bot has proper permissions
2. **Webhooks not working**: Verify `ALPHABOT_WEBHOOK_SECRET` and webhook URL configuration
3. **API errors**: Check that user API keys are valid and have proper permissions

### Logs

The application logs important events including:
- Webhook receptions and processing
- Raffle entry attempts and results
- User registration/removal events
- API errors and rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

