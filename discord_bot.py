import discord
from discord import app_commands
from discord.ext import commands
import subprocess
from dotenv import load_dotenv
import os

print("Loading environment variables...")

load_dotenv()  # Load environment variables from a .env file if present

print("Bot Token:", os.getenv("BOT_TOKEN"))

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SCREEN_SESSION_NAME = os.getenv("SCREEN_SESSION_NAME_SERVER")
ALLOWED_ROLE_NAME = os.getenv("ALLOWED_ROLE_NAME")

print("Configuration:")
print("SCREEN_SESSION_NAME:", SCREEN_SESSION_NAME)
print("ALLOWED_ROLE_NAME:", ALLOWED_ROLE_NAME)  

# --- Bot Setup ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f"Bot is configured to allow the role: '{ALLOWED_ROLE_NAME}'") 
    print('Bot is ready to receive commands.')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# --- Base Command Error Handler ---
async def handle_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """A generic error handler for slash commands."""
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message(
            f"You do not have the required role (`{ALLOWED_ROLE_NAME}`) to use this command.",
            ephemeral=True
        )
    else:
        # It's good to log unhandled errors for debugging
        print(f"An unhandled error occurred in a command: {error}")
        # Send a generic error message
        # Check if the interaction has already been responded to
        if not interaction.response.is_done():
            await interaction.response.send_message("An unexpected error occurred while running the command.", ephemeral=True)
        else:
            await interaction.followup.send("An unexpected error occurred while running the command.", ephemeral=True)


# --- Minecraft Server Commands ---

@bot.tree.command(name="mserverexec", description="Execute a command on the Minecraft server.")
#@app_commands.checks.has_role(ALLOWED_ROLE_NAME) #Just implement it on the server in the Integration panel
async def mserverexec(interaction: discord.Interaction, command: str):
    """
    Takes a command as input and executes it in the specified screen session.
    The decorator above this function automatically checks for the required role.
    """
    try:
        print(f"Received command from {interaction.user}: {command}")
        # The command to be sent to the screen session
        # The `stuff` command simulates typing in the screen session.
        # We append `\n` to simulate pressing Enter.
        screen_command = f"screen -S {SCREEN_SESSION_NAME} -X stuff '{command}\n'"
        
        # Execute the command
        subprocess.run(screen_command, shell=True, check=True)
        
        # Send a confirmation message back to Discord
        await interaction.response.send_message(f"Successfully executed command: `{command}`", ephemeral=True)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        if not interaction.response.is_done():
            await interaction.response.send_message(error_message, ephemeral=True)
        else:
            await interaction.followup.send(error_message, ephemeral=True)

@mserverexec.error
async def on_mserverexec_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


@bot.tree.command(name="mserverstart", description="Starts the Minecraft server.")
async def mserverstart(interaction: discord.Interaction):
    """Starts the Minecraft server using the 'make start_minecraft' command."""
    try:
        print(f"Received start command from {interaction.user}")
        await interaction.response.defer(ephemeral=True, thinking=True)
        subprocess.run("make start_minecraft", shell=True, check=True)
        await interaction.followup.send("The Minecraft server is starting.", ephemeral=True)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        if not interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)

@mserverstart.error
async def on_mserverstart_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


@bot.tree.command(name="mserverstop", description="Stops the Minecraft server.")
async def mserverstop(interaction: discord.Interaction):
    """Stops the Minecraft server using the 'make stop_minecraft' command."""
    try:
        print(f"Received stop command from {interaction.user}")
        await interaction.response.defer(ephemeral=True, thinking=True)
        subprocess.run("make stop_minecraft", shell=True, check=True)
        await interaction.followup.send("The Minecraft server is stopping.", ephemeral=True)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        if not interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)

@mserverstop.error
async def on_mserverstop_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


@bot.tree.command(name="mserverestart", description="Restarts the Minecraft server.")
async def mserverestart(interaction: discord.Interaction):
    """Restarts the Minecraft server using the 'make restart_minecraft' command."""
    try:
        print(f"Received restart command from {interaction.user}")
        await interaction.response.defer(ephemeral=True, thinking=True)
        subprocess.run("make restart_minecraft", shell=True, check=True)
        await interaction.followup.send("The Minecraft server is restarting.", ephemeral=True)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        if not interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)

@mserverestart.error
async def on_mserverestart_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


@bot.tree.command(name="mserverstatus", description="Checks the status of the server screen sessions.")
async def mserverstatus(interaction: discord.Interaction):
    """Checks the server status using the 'make check' command."""
    try:
        print(f"Received status command from {interaction.user}")
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        # Execute the command and capture the output
        result = subprocess.run(
            "make check",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        
        output = result.stdout.strip()
        
        # Provide a more user-friendly message if there's no output
        if not output:
            output = "No running screen sessions found."
            
        await interaction.followup.send(f"**Server Status:**\n```\n{output}\n```", ephemeral=True)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        if not interaction.response.is_done():
            await interaction.followup.send(error_message, ephemeral=True)

@mserverstatus.error
async def on_mserverstatus_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


# --- Run the Bot ---
bot.run(BOT_TOKEN)
