import nextcord

from dotenv import load_dotenv
from getpass import getuser
from json import load
from nextcord import Embed
from nextcord.ext import commands
from os import environ, path
from random import choice, randint, shuffle
from sys import path as syspath
from typing import Union
from uuid import uuid4

# get environment vars
load_dotenv()

# get preset boards
boards = load(
	open(
		path.join(
			syspath[0], 'assets', 'boards.json'
		), 'tr'
	)
)

# get letter scores
scores = load(
	open(
		path.join(
			syspath[0], 'assets', 'scores.json'
		), 'tr'
	)
)

# get emoji codes
emojis = load(
	open(
		path.join(
			syspath[0], 'assets', 'emojis.json'
		), 'tr'
	)
)

# get words list
list_of_words = open(
	path.join(
		syspath[0], 'assets', 'words.txt'
	), 'tr'
).read().split('\n')

# find word score, anagrams, and contained words
def details(word_to_check: str) -> dict:
	sorted_word = ''.join(sorted(word_to_check))
	anagrams = contains = []
	for word in list_of_words:
		if len(word) > len(word_to_check):
			continue
		elif sorted_word == ''.join(sorted(word)):
			anagrams.append(word)
		elif set(word).issubset(set(sorted_word)):
			contains.append(word)
		else:
			continue
	return {
		'anagrams': sorted(
			anagrams,
			key=lambda x: sum(scores(char) for char in x)
		),
		'contains': sorted(
			contains,
			key=lambda x: sum(scores(char) for char in x)
		),
		'score': sum(scores[char] for char in word_to_check)
	}

# calculate word iq
def calculate_word_iq(played_word, best_word) -> float:
	return details(played_word)['score'] / details(best_word)['score'] * 200

# define client
version = ''
client = commands.Bot(
	command_prefix = '/',
	description = 'QuarrelBot' + (f' {version}' if version else ''),
	intents = nextcord.Intents.default()
)

@client.event
async def on_ready() -> None:
	print(f'Running from {dirname}\nLogged in as {client.user} (ID: {client.user.id})') # type: ignore
	await client.change_presence(
		activity = nextcord.Streaming(
			name = version + ('[local]' if getuser() in environ['LOCAL_USER'].split(',') else ''),
			url = 'https://twitch.tv/turnipguy30'
		), status = nextcord.Status.do_not_disturb
	)
