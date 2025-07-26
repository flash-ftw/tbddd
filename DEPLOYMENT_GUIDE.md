# Alphabot Discord Bot - Deployment Guide

This guide will walk you through deploying the Alphabot Discord Bot to Railway and setting up all necessary configurations.

## Prerequisites

Before starting, ensure you have:

1. **Discord Bot Token**: Create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. **Alphabot Team API Key**: Your team's API key from the Alphabot team page
3. **Alphabot Webhook Secret**: Configure this in your Alphabot team settings
4. **GitHub Account**: For code repository hosting
5. **Railway Account**: For deployment hosting

## Step 1: Discord Bot Setup

### 1.1 Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give your application a name (e.g., "Alphabot Raffle Bot")
4. Click "Create"

### 1.2 Create Bot User

1. In your application, go to the "Bot" section
2. Click "Add Bot"
3. Under "Token", click "Copy" to get your bot token
4. **Save this token securely** - you'll need it for deployment

### 1.3 Configure Bot Permissions

1. In the "Bot" section, scroll down to "Privileged Gateway Intents"
2. Enable "Message Content Intent" (required for command processing)
3. In the "OAuth2" > "URL Generator" section:
   - Select "bot" in Scopes
   - Select these Bot Permissions:
     - Send Messages
     - Read Message History
     - Use Slash Commands
     - Manage Messages (to delete API key messages)

### 1.4 Invite Bot to Your Server

1. Copy the generated URL from the OAuth2 URL Generator
2. Open the URL in your browser
3. Select your Discord server and authorize the bot

## Step 2: Alphabot Configuration

### 2.1 Get Team API Key

1. Log in to [Alphabot](https://www.alphabot.app)
2. Go to your team page
3. Find and copy your team's API key

### 2.2 Configure Webhook

1. In your Alphabot team settings, find the webhook configuration
2. Set the webhook URL to: `https://your-app-name.railway.app/webhook/alphabot`
   (You'll get the actual URL after Railway deployment)
3. Set a webhook secret (a random string you'll use for verification)
4. Enable the `raffle:active` event

## Step 3: GitHub Repository Setup

### 3.1 Create Repository

1. Create a new repository on GitHub
2. Clone this project code to your repository
3. Make sure to include all files except `.env` (which contains secrets)

### 3.2 Repository Structure

Your repository should have this structure:
```
alphabot-discord-bot/
├── src/
│   ├── routes/
│   │   ├── webhook.py
│   │   └── user.py
│   ├── models/
│   │   └── user.py
│   ├── database/
│   ├── static/
│   ├── main.py
│   ├── discord_bot.py
│   ├── alphabot_client.py
│   └── user_storage.py
├── requirements.txt
├── railway.json
├── Procfile
├── .gitignore
├── README.md
└── DEPLOYMENT_GUIDE.md
```

## Step 4: Railway Deployment

### 4.1 Create Railway Project

1. Go to [Railway](https://railway.app)
2. Sign up/log in with your GitHub account
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository

### 4.2 Configure Environment Variables

In your Railway project dashboard, go to "Variables" and add:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
ALPHABOT_TEAM_API_KEY=your_team_alphabot_api_key_here
ALPHABOT_WEBHOOK_SECRET=your_webhook_secret_here
SECRET_KEY=a_random_secret_key_for_flask
PORT=5000
```

**Important**: Use strong, unique values for `SECRET_KEY` and `ALPHABOT_WEBHOOK_SECRET`.

### 4.3 Deploy

1. Railway will automatically detect the Python app and deploy it
2. Wait for the deployment to complete
3. Note your app's URL (e.g., `https://your-app-name.railway.app`)

### 4.4 Update Alphabot Webhook URL

1. Go back to your Alphabot team settings
2. Update the webhook URL to: `https://your-app-name.railway.app/webhook/alphabot`
3. Save the configuration

## Step 5: Testing the Deployment

### 5.1 Test Discord Bot

1. Go to your Discord server
2. Try the command: `!bothelp`
3. The bot should respond with a help message

### 5.2 Test Webhook Endpoint

1. You can test the webhook using the provided test script
2. Or wait for a real raffle to become active and check the logs

### 5.3 Test User Registration

1. In Discord, use: `!setapikey your_personal_alphabot_api_key`
2. Use: `!status` to verify registration
3. The bot should confirm your registration

## Step 6: Monitoring and Maintenance

### 6.1 Railway Logs

1. In your Railway project, go to "Deployments"
2. Click on the latest deployment to view logs
3. Monitor for any errors or issues

### 6.2 Database Backup

The bot stores user data in a JSON file. For production use, consider:
- Regular backups of the user data
- Migrating to a proper database (PostgreSQL, etc.)
- Implementing data encryption

## Troubleshooting

### Common Issues

1. **Bot not responding in Discord**
   - Check that `DISCORD_BOT_TOKEN` is correct
   - Verify bot permissions in Discord server
   - Check Railway logs for errors

2. **Webhooks not working**
   - Verify webhook URL is correct in Alphabot settings
   - Check `ALPHABOT_WEBHOOK_SECRET` matches
   - Test webhook endpoint manually

3. **Users can't register API keys**
   - Check Discord bot permissions
   - Verify the bot can send/delete messages
   - Check Railway logs for storage errors

4. **Raffle joining fails**
   - Verify user API keys are valid
   - Check Alphabot API rate limits
   - Review error logs for specific issues

### Getting Help

1. Check Railway deployment logs
2. Review Discord bot logs
3. Test individual components (webhook, Discord commands)
4. Verify all environment variables are set correctly

## Security Best Practices

1. **Never commit secrets to Git**
   - Use `.gitignore` to exclude `.env` files
   - Store all secrets in Railway environment variables

2. **Rotate secrets regularly**
   - Change webhook secrets periodically
   - Update Discord bot tokens if compromised

3. **Monitor access**
   - Review Railway access logs
   - Monitor Discord bot activity
   - Check for unusual API usage

4. **Backup data**
   - Regular backups of user registrations
   - Document recovery procedures

## Scaling Considerations

For high-traffic usage, consider:

1. **Database Migration**
   - Move from JSON file to PostgreSQL
   - Implement proper user data encryption

2. **Rate Limiting**
   - Implement user-level rate limiting
   - Add queue system for raffle processing

3. **Monitoring**
   - Add application performance monitoring
   - Set up alerts for failures

4. **High Availability**
   - Consider multiple deployment regions
   - Implement health checks and auto-recovery

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Railway and Discord documentation
3. Check Alphabot API documentation
4. Contact the development team with specific error messages and logs

