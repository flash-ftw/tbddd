import os
import logging
import discord
from discord.ext import commands
from src.user_storage import UserStorage
from src.alphabot_client import AlphabotClient

logger = logging.getLogger(__name__)

class DiscordBot:
    """Discord bot for managing Alphabot raffle entries"""
    
    def __init__(self):
        # Set up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot instance
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        # Initialize storage and API client
        self.user_storage = UserStorage()
        self.alphabot_client = AlphabotClient()
        
        # Set up event handlers and commands
        self._setup_events()
        self._setup_commands()
    
    def _setup_events(self):
        """Set up Discord bot events"""
        
        @self.bot.event
        async def on_ready():
            logger.info(f'{self.bot.user} has connected to Discord!')
            logger.info(f'Bot is in {len(self.bot.guilds)} guilds')
        
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return  # Ignore unknown commands
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"❌ Missing required argument: {error.param}")
            elif isinstance(error, commands.BadArgument):
                await ctx.send(f"❌ Invalid argument: {error}")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send("❌ An error occurred while processing your command.")
    
    def _setup_commands(self):
        """Set up Discord bot commands"""
        
        @self.bot.command(name='setapikey', help='Set your Alphabot API key')
        async def set_api_key(ctx, api_key: str = None):
            if api_key is None:
                await ctx.send("❌ Please provide your Alphabot API key: `!setapikey YOUR_API_KEY`")
                return
            
            # Basic validation
            if len(api_key) < 10:
                await ctx.send("❌ API key seems too short. Please check and try again.")
                return
            
            user_id = str(ctx.author.id)
            
            # Store the API key
            if self.user_storage.set_user_api_key(user_id, api_key):
                await ctx.send("✅ Your Alphabot API key has been saved successfully!")
                logger.info(f"User {ctx.author} ({user_id}) set their API key")
                
                # Delete the message containing the API key for security
                try:
                    await ctx.message.delete()
                except discord.errors.NotFound:
                    pass  # Message already deleted
                except discord.errors.Forbidden:
                    await ctx.send("⚠️ I couldn't delete your message. Please delete it manually to keep your API key secure.")
            else:
                await ctx.send("❌ Failed to save your API key. Please try again.")
        
        @self.bot.command(name='removekey', help='Remove your stored Alphabot API key')
        async def remove_api_key(ctx):
            user_id = str(ctx.author.id)
            
            if self.user_storage.remove_user_api_key(user_id):
                await ctx.send("✅ Your Alphabot API key has been removed.")
                logger.info(f"User {ctx.author} ({user_id}) removed their API key")
            else:
                await ctx.send("❌ No API key found for your account.")
        
        @self.bot.command(name='status', help='Check your registration status')
        async def status(ctx):
            user_id = str(ctx.author.id)
            
            if self.user_storage.user_exists(user_id):
                total_users = self.user_storage.get_user_count()
                await ctx.send(f"✅ You are registered for automatic raffle entries!\n"
                             f"📊 Total registered users: {total_users}")
            else:
                await ctx.send("❌ You are not registered. Use `!setapikey YOUR_API_KEY` to get started.")
        
        @self.bot.command(name='joinraffle', help='Manually join a specific raffle')
        async def join_raffle(ctx, raffle_slug: str = None):
            if raffle_slug is None:
                await ctx.send("❌ Please provide a raffle slug: `!joinraffle RAFFLE_SLUG`")
                return
            
            user_id = str(ctx.author.id)
            api_key = self.user_storage.get_user_api_key(user_id)
            
            if not api_key:
                await ctx.send("❌ You need to set your API key first: `!setapikey YOUR_API_KEY`")
                return
            
            # Send initial message
            message = await ctx.send(f"🔄 Attempting to join raffle: `{raffle_slug}`...")
            
            try:
                # Attempt to register for the raffle
                result = self.alphabot_client.register_for_raffle(
                    api_key=api_key,
                    raffle_slug=raffle_slug,
                    discord_id=user_id
                )
                
                if result.get('success'):
                    await message.edit(content=f"✅ Successfully joined raffle: `{raffle_slug}`!")
                    logger.info(f"User {ctx.author} ({user_id}) manually joined raffle {raffle_slug}")
                else:
                    error_msg = result.get('error', 'Unknown error')
                    await message.edit(content=f"❌ Failed to join raffle: {error_msg}")
                    logger.warning(f"User {ctx.author} ({user_id}) failed to join raffle {raffle_slug}: {error_msg}")
                    
            except Exception as e:
                await message.edit(content=f"❌ Error joining raffle: {str(e)}")
                logger.error(f"Error in manual raffle join for user {user_id}: {e}")
        
        @self.bot.command(name='bothelp', help='Show available commands')
        async def help_command(ctx):
            embed = discord.Embed(
                title="🤖 Alphabot Discord Bot Commands",
                description="Automatically join Alphabot raffles when they become active!",
                color=0x00ff00
            )
            
            embed.add_field(
                name="!setapikey <your_key>",
                value="Set your personal Alphabot API key for automatic raffle entries",
                inline=False
            )
            
            embed.add_field(
                name="!removekey",
                value="Remove your stored API key",
                inline=False
            )
            
            embed.add_field(
                name="!status",
                value="Check if you're registered and see total user count",
                inline=False
            )
            
            embed.add_field(
                name="!joinraffle <slug>",
                value="Manually join a specific raffle by its slug",
                inline=False
            )
            
            embed.add_field(
                name="ℹ️ How it works",
                value="1. Set your API key with `!setapikey`\n"
                      "2. The bot will automatically enter you in raffles when they become active\n"
                      "3. You'll receive notifications about entry results",
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    async def start(self):
        """Start the Discord bot"""
        token = os.environ.get('DISCORD_BOT_TOKEN')
        if not token:
            logger.error("DISCORD_BOT_TOKEN environment variable not set")
            return
        
        try:
            await self.bot.start(token)
        except Exception as e:
            logger.error(f"Failed to start Discord bot: {e}")
    
    async def send_notification(self, user_id: str, message: str):
        """Send a direct message to a user"""
        try:
            user = await self.bot.fetch_user(int(user_id))
            if user:
                await user.send(message)
                logger.info(f"Sent notification to user {user_id}")
            else:
                logger.warning(f"Could not find user {user_id}")
        except Exception as e:
            logger.error(f"Error sending notification to user {user_id}: {e}")
    
    def get_bot_instance(self):
        """Get the bot instance for external use"""
        return self.bot

