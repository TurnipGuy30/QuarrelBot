from dotenv import load_dotenv
from flask import Flask
from os import environ
from threading import Thread

from game import client

load_dotenv()

app = Flask('')
@app.route('/')
def home() -> str:
	return 'Running!'
def run() -> None:
	app.run(port = int(environ.get('PORT', 33507)))
def keep_alive() -> None:
	Thread(target = run).start()

if __name__ == '__main__':
	keep_alive()
	client.run(environ['DISCORD_TOKEN'])
