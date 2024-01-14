#variables for source folder
SRC = portfolio_optimisation
BOT_MODULE = $(SRC).bot
start-bot:
	python3 -m $(BOT_MODULE).bot
start-api:
	python3 -m $(SRC).api.app