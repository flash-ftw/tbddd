# Alphabot Discord Bot - User Guide

Welcome to the Alphabot Discord Bot! This bot automatically enters you into Alphabot raffles when they become active. Here's how to use it.

## Getting Started

### Step 1: Get Your Alphabot API Key

1. Go to [Alphabot](https://www.alphabot.app) and log in
2. Go to your profile page
3. Find your personal API key (not the team key)
4. Copy this key - you'll need it for registration

### Step 2: Register with the Bot

In any channel where the bot is present, use:
```
!setapikey YOUR_API_KEY_HERE
```

**Important**: The bot will automatically delete your message containing the API key for security. If it can't delete the message, please delete it manually.

### Step 3: Verify Registration

Check that you're registered:
```
!status
```

The bot will confirm your registration and show the total number of registered users.

## Available Commands

### `!setapikey <your_key>`
**Purpose**: Register or update your personal Alphabot API key

**Example**: `!setapikey abc123def456ghi789`

**Notes**: 
- Your message will be automatically deleted for security
- You can update your key anytime by running this command again

### `!removekey`
**Purpose**: Remove your stored API key from the bot

**Example**: `!removekey`

**Notes**: 
- This will stop automatic raffle entries for your account
- You can re-register anytime with `!setapikey`

### `!status`
**Purpose**: Check your registration status and see bot statistics

**Example**: `!status`

**Response**: Shows if you're registered and the total number of registered users

### `!joinraffle <slug>`
**Purpose**: Manually join a specific raffle by its slug

**Example**: `!joinraffle cool-nft-raffle-2024`

**Notes**: 
- You must be registered first with `!setapikey`
- The raffle must be active and accepting entries
- This is useful for joining specific raffles or testing

### `!bothelp`
**Purpose**: Show all available commands and how the bot works

**Example**: `!bothelp`

**Response**: Displays a comprehensive help message with all commands

## How Automatic Raffle Entry Works

1. **Registration**: You register your API key with `!setapikey`
2. **Webhook Reception**: When a raffle becomes active, Alphabot sends a notification to our bot
3. **Automatic Entry**: The bot automatically tries to enter all registered users into the raffle
4. **Notifications**: You'll receive a direct message about whether the entry was successful

## Notifications

The bot will send you direct messages for:
- ✅ Successful raffle entries
- ❌ Failed raffle entries (with reason)
- ⚠️ API key issues or errors

## Frequently Asked Questions

### Q: Do I need to be online for automatic entries?
**A**: No! The bot works 24/7. As long as you're registered, it will try to enter you into raffles even when you're offline.

### Q: Can I use the same API key on multiple Discord accounts?
**A**: Each Discord account needs its own unique Alphabot API key. Using the same key on multiple accounts may cause issues.

### Q: What happens if my API key expires or becomes invalid?
**A**: The bot will notify you via direct message if there are issues with your API key. You'll need to update it with a new one.

### Q: Can I see which raffles I've been entered into?
**A**: The bot will send you notifications for each entry attempt. You can also check your Alphabot profile for entry history.

### Q: Is my API key secure?
**A**: Yes! The bot automatically deletes messages containing API keys, and keys are stored securely on the server. However, never share your API key with others.

### Q: Can I disable automatic entries temporarily?
**A**: Use `!removekey` to stop automatic entries. Use `!setapikey` again when you want to resume.

### Q: What if the bot doesn't respond to my commands?
**A**: Check that:
- The bot is online (green status in Discord)
- You're using the correct command format
- You have permission to send messages in the channel
- Try using commands in a direct message with the bot

## Error Messages and Solutions

### "❌ You need to set your API key first"
**Solution**: Use `!setapikey YOUR_API_KEY` to register

### "❌ API key seems too short"
**Solution**: Check that you copied the complete API key from Alphabot

### "❌ Failed to join raffle: Invalid API key"
**Solution**: Your API key may have expired. Get a new one from Alphabot and update with `!setapikey`

### "❌ Failed to join raffle: Rate limited"
**Solution**: The bot hit Alphabot's rate limits. It will automatically retry. No action needed.

### "❌ Failed to join raffle: Already entered"
**Solution**: You're already entered in this raffle. This is normal and expected.

## Best Practices

1. **Keep your API key private**: Never share it in public channels
2. **Update regularly**: If you get a new API key from Alphabot, update it in the bot
3. **Monitor notifications**: Check your direct messages for entry results
4. **Use `!status` regularly**: Verify you're still registered, especially after Alphabot updates
5. **Be patient**: During high-traffic periods, entries may take a few moments to process

## Privacy and Data

### What data does the bot store?
- Your Discord user ID
- Your Alphabot API key
- Entry attempt logs (for debugging)

### How is my data protected?
- API keys are stored securely on the server
- No personal information beyond Discord ID is collected
- Data is only used for raffle entry functionality

### Can I delete my data?
Yes! Use `!removekey` to remove your API key and associated data from the bot.

## Support

If you need help:

1. **Try `!bothelp`** for quick command reference
2. **Check this guide** for detailed explanations
3. **Contact server administrators** for bot-specific issues
4. **Check Alphabot support** for API key or account issues

## Tips for Success

1. **Register early**: Set up your API key as soon as possible
2. **Keep your Alphabot account active**: Inactive accounts may have API issues
3. **Monitor your entries**: Check Alphabot regularly to see your entry history
4. **Stay updated**: Follow announcements about bot updates or changes
5. **Use manual entries**: For important raffles, consider using `!joinraffle` as backup

## Updates and Changes

The bot may receive updates that:
- Add new features
- Improve reliability
- Fix bugs
- Enhance security

You'll be notified of major changes through Discord announcements. Your registration and settings will be preserved during updates.

---

**Happy raffling! 🎉**

Remember: This bot is a tool to help you participate in raffles more efficiently. Always follow Alphabot's terms of service and raffle rules.

