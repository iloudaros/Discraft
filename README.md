# Discraft - Discord to Minecraft Server Bot

Discraft is a powerful and easy-to-use Discord bot that acts as a bridge to your Minecraft server. It allows authorized users to execute commands on the Minecraft server directly from a Discord channel, streamlining server management. The bot runs in a `screen` session for persistence, and a `makefile` is included for easy process management.

## Features

*   **Remote Command Execution:** Run any Minecraft server command from the comfort of your Discord server.
*   **Role-Based Access Control:** Restrict command execution to specific roles (e.g., 'Staff'), ensuring server security.
*   **Persistent Operation:** Utilizes `screen` to run the bot and Minecraft server in the background, ensuring they stay online.
*   **Easy Setup:** Configuration is straightforward using an `.env` file.
*   **Simple Management:** A `makefile` provides simple commands to start, stop, and check the status of the services.

## Directory Structure

```
└── Discraft/
    ├── discord_bot.py
    ├── makefile
    ├── requirements.txt
    └── .env_template
```

## Setup and Installation

### Prerequisites

*   Python 3.x
*   `screen` command-line utility
*   A Minecraft server JAR file (the `makefile` is pre-configured for `fabric-server-launch.jar`)

### 1. Clone the Repository

```bash
git clone https://github.com/iloudaros/iloudaros-discraft.git
cd iloudaros-discraft
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# Create and activate the virtual environment
make create_venv
source venv/bin/activate
```

This will install the necessary Python packages listed in `requirements.txt`.

### 3. Configure Environment Variables

Create a `.env` file from the template and fill in your specific details.

```bash
cp .env_template .env
```

Now, edit the `.env` file with your information:

```ini
BOT_TOKEN=[your_discord_bot_token]
SCREEN_SESSION_NAME_SERVER='mserver'
SCREEN_SESSION_NAME_BOT='discordbot'
ALLOWED_ROLE_NAME='Staff'
```

| Variable                   | Description                                                                                                                                                            |
| :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BOT_TOKEN`                | Your Discord bot token. You can get this from the Discord Developer Portal.                                                                                            |
| `SCREEN_SESSION_NAME_SERVER` | The name for the `screen` session that will run the Minecraft server.                                                                                                |
| `SCREEN_SESSION_NAME_BOT`  | The name for the `screen` session that will run the Discord bot.                                                                                                       |
| `ALLOWED_ROLE_NAME`        | The **exact**, case-sensitive name of the Discord role that is allowed to execute commands.                                                                               |

## Usage

### Starting the Services

To start both the Minecraft server and the Discord bot in their respective `screen` sessions, use the `make` command:

```bash
make start
```

### Checking Service Status

You can verify that the `screen` sessions have been created and are running with:

```bash
make check
```

You should see output listing the two screen sessions you defined in your `.env` file (e.g., `mserver` and `discordbot`).

### Using the Discord Bot

Once the bot is running and has been invited to your Discord server, you can execute commands on your Minecraft server.

1.  Make sure the user has the role defined in `ALLOWED_ROLE_NAME`.
2.  In a Discord channel, type `/` to bring up the command list and select `mserverexec`.
3.  In the `command` argument, type the Minecraft command you wish to execute.

**Example:**

`/mserverexec command:say Hello to all players from Discord!`

The bot will confirm the command execution with an ephemeral message, visible only to you.

## File Descriptions

*   **`discord_bot.py`**: The core Python script that runs the Discord bot, handles events, and processes commands.
*   **`makefile`**: An automation script with commands (`start`, `check`, `create_venv`) to simplify the setup and management of the services.
*   **`requirements.txt`**: A list of the Python dependencies required for the project.
*   **`.env_template`**: A template file for you to create your own `.env` configuration file.

