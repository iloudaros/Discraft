include .env

.PHONY: start_minecraft start_discord_bot start check printenv

printenv:
	@echo ${SCREEN_SESSION_NAME_BOT}
	@echo ${SCREEN_SESSION_NAME_SERVER}

create_venv:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

activate_venv:
	@echo "To activate the virtual environment, run:"
	@echo "source venv/bin/activate"
	

# Minecraft server management	
start_minecraft:
	@echo "Starting Minecraft server..."
	@screen -dmS ${SCREEN_SESSION_NAME_SERVER}
	@screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "cd ../ && java -jar fabric-server-launch.jar\n"
	@echo "Minecraft server started in screen session: ${SCREEN_SESSION_NAME_SERVER}."

stop_minecraft:
	@echo "Stopping Minecraft server..."
	@screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "stop\n"
	@sleep 10
	@-screen -S ${SCREEN_SESSION_NAME_SERVER} -X quit
	@echo "Minecraft server stopped."

restart_minecraft: stop_minecraft start_minecraft
	

# Discord bot management	
start_discord_bot:
	@echo "Starting Discord bot..."
	@screen -dmS ${SCREEN_SESSION_NAME_BOT}
	@screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "source venv/bin/activate && python3 discord_bot.py\n"
	@echo "Discord bot started in screen session: ${SCREEN_SESSION_NAME_BOT}."

stop_discord_bot:
	@echo "Stopping Discord bot..."
	@screen -S ${SCREEN_SESSION_NAME_BOT} -X quit
	@echo "Discord bot stopped."

restart_discord_bot: stop_discord_bot start_discord_bot


# Combined commands
start: start_minecraft start_discord_bot

stop: stop_minecraft stop_discord_bot

restart: restart_minecraft restart_discord_bot

check:
	screen -ls