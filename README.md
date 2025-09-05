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
git clone https://github.com/iloudaros/discraft.git
cd discraft
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

| Variable | Description |
| :--- | :--- |
| `BOT_TOKEN` | Your Discord bot token. You can get this from the Discord Developer Portal. |
| `SCREEN_SESSION_NAME_SERVER` | The name for the `screen` session that will run the Minecraft server. |
| `SCREEN_SESSION_NAME_BOT` | The name for the `screen` session that will run the Discord bot. |
| `ALLOWED_ROLE_NAME` | The **exact**, case-sensitive name of the Discord role that is allowed to execute commands. |

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

## Contributing and Feature Requests

We welcome contributions and feedback from the community! If you encounter a bug or have an idea for a new feature, please open an issue on our GitHub repository.

[**Open an Issue on GitHub**](https://github.com/iloudaros/discraft/issues)

*   **For Bug Reports:** Please provide a clear description of the issue, steps to reproduce it, the expected behavior, and the actual behavior.
*   **For Feature Requests:** Describe the feature you would like to see and explain how it would be beneficial to the project.

## Roadmap to Public Version

The current version of Discraft is designed for self-hosting. The long-term vision is to create a public, multi-tenant version that any server owner can easily invite and connect to their Minecraft server. Here are the planned phases to achieve this:

### Phase 1: Core Refactoring for Scalability 

- [ ]  **Containerization:** Transition from `screen` and `makefile` to Docker for creating scalable and isolated environments for each connected server.
- [ ]  **Secure Configuration Management:** Move from a static `.env` file to a secure database for managing multiple server configurations and secrets.
- [ ]   **Centralized Logging:** Implement a robust logging system to monitor the health and performance of all bot instances.

### Phase 2: User-Friendly Configuration

- [ ] **Web Dashboard:** Develop a web-based interface for users to register, invite the bot, and configure all settings without touching a command line.
- [ ] **Dynamic Linking:** Create a system where users can link their Discord server to their Minecraft server details via the dashboard.
- [ ] **Flexible Permissions:** Enhance the role-based access control to be fully configurable through the web dashboard.

### Phase 3: Infrastructure and Deployment

- [ ] **Cloud Deployment:** Deploy the bot and its backend services to a scalable cloud provider.
- [ ] **Database Integration:** Set up and integrate a production-grade database to manage all user and server data.
- [ ] **High Availability:** Ensure the infrastructure is resilient and can handle a large number of concurrent users and servers.

### Phase 4: Public Launch
- [ ] **Official Release:** Launch the public version of the bot.
- [ ] **Community Support:** Create a dedicated Discord server for community support and announcements.
- [ ] **Public Documentation:** Publish comprehensive documentation to guide users through the setup and usage of the public bot.

## File Descriptions

*   **`discord_bot.py`**: The core Python script that runs the Discord bot, handles events, and processes commands.
*   **`makefile`**: An automation script with commands (`start`, `check`, `create_venv`) to simplify the setup and management of the services.
*   **`requirements.txt`**: A list of the Python dependencies required for the project.
*   **`.env_template`**: A template file for you to create your own `.env` configuration file.

