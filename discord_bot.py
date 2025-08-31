import discord
from discord import app_commands
from discord.ext import commands
import subprocess
from dotenv import load_dotenv
import os

# --- Configuration ---
# You need to replace these values with your own.

# 1. Your Discord Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Make sure to set this in your environment variables or .env file

# 2. The name of the screen session your Minecraft server is running in.
#    You can find this by running `screen -ls` in your terminal.
SCREEN_SESSION_NAME = os.getenv("SCREEN_SESSION_NAME_SERVER")  # e.g., "mserver"

# 3. The exact name of the role that can execute commands.
#    This is case-sensitive and must match the role name in your Discord server.
ALLOWED_ROLE_NAME = os.getenv("ALLOWED_ROLE_NAME")  # e.g., "Staff"

# --- Bot Setup ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready to receive commands.')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="mserverexec", description="Execute a command on the Minecraft server.")
@app_commands.checks.has_role(ALLOWED_ROLE_NAME)
async def mserverexec(interaction: discord.Interaction, command: str):
    """
    Takes a command as input and executes it in the specified screen session.
    The decorator above this function automatically checks for the required role.
    """
    try:
        # The command to be sent to the screen session
        # The `stuff` command simulates typing in the screen session.
        # We append `\n` to simulate pressing Enter.
        screen_command = f"screen -S {SCREEN_SESSION_NAME} -X stuff '{command}\n'"
        
        # Execute the command
        subprocess.run(screen_command, shell=True, check=True)
        
        # Send a confirmation message back to Discord
        await interaction.response.send_message(f"Successfully executed command: `{command}`", ephemeral=True)

    except subprocess.CalledProcessError as e:
        # If the command fails for some reason
        error_message = f"Failed to execute command. Error: {e}"
        await interaction.response.send_message(error_message, ephemeral=True)
        
    except Exception as e:
        # For other potential errors
        await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

# Error handler for the mserverexec command
@mserverexec.error
async def on_mserverexec_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """
    Catches errors from the mserverexec command, including permission errors.
    """
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(
            f"You do not have the required role (`{ALLOWED_ROLE_NAME}`) to use this command.",
            ephemeral=True
        )
    else:
        # For other errors, it's good to log them to the console for debugging
        print(f"An unhandled error occurred in mserverexec command: {error}")
        # Send a generic error message to the user
        await interaction.response.send_message("An unexpected error occurred while running the command.", ephemeral=True)


# --- Run the Bot ---
bot.run(BOT_TOKEN)
