import json
import os
import random

import discord
from discord.ext import commands

from settings import *
async def get_momma_jokes():
    with open(os.path.join(DATA_DIR, "jokes.json")) as joke_file:
        jokes = json.load(joke_file)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult