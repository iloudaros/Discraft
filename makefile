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
	screen -dmS ${SCREEN_SESSION_NAME_SERVER}
	screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "cd ../ && java -jar fabric-server-launch.jar\n"

restart_minecraft:
	@echo "Restarting Minecraft server..."
	@screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "stop\n"
	@sleep 10
	@screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "cd ../ && java -jar fabric-server-launch.jar\n"
	@echo "Minecraft server restarted."
	

# Discord bot management	
start_discord_bot:
	screen -dmS ${SCREEN_SESSION_NAME_BOT}
	screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "source venv/bin/activate && python3 discord_bot.py\n"

restart_discord_bot:
	@echo "Restarting Discord bot..."
	@screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "\x03"  # Send Ctrl+C to stop the bot
	@sleep 5
	@screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "source venv/bin/activate && python3 discord_bot.py\n"	
	@echo "Discord bot restarted."


# Combined commands
start: start_minecraft start_discord_bot

restart: restart_minecraft restart_discord_bot

check:
	screen -ls