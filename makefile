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

test:
	screen -dmS test_session
	screen -S test_session -X stuff "echo 'Hello, World!' \n"
	
start_minecraft:
	screen -dmS ${SCREEN_SESSION_NAME_SERVER}
	screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "cd ../ && java -jar fabric-server-launch.jar\n"

restart_minecraft:
	screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "stop\n"
	sleep 10
	screen -S ${SCREEN_SESSION_NAME_SERVER} -X stuff "cd ../ && java -jar fabric-server-launch.jar\n"
	
start_discord_bot:
	screen -dmS ${SCREEN_SESSION_NAME_BOT}
	screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "source venv/bin/activate && python3 discord_bot.py\n"

restart_discord_bot:
	screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "\x03"  # Send Ctrl+C to stop the bot
	sleep 5
	screen -S ${SCREEN_SESSION_NAME_BOT} -X stuff "source venv/bin/activate && python3 discord_bot.py\n"	

start: start_minecraft start_discord_bot

restart: restart_minecraft restart_discord_bot

check:
	screen -ls