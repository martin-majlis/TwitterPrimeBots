import json
import math
import os
import random
import tweepy

# Constants
FILE_CREDENTIALS = 'credentials.json'
FILE_STATE = 'state.json'
KEY_NUM = 'num'
KEY_BOT = 'bot'
KEY_ID = 'id'
BOT_NAMES = ['@AlicePrimes', '@BobPrimes']


def find_next_prime(act):
    while True:
        act += 1
        is_prime = True
        for i in range(2, (int)(math.sqrt(act)) + 2):
            if act % i == 0:
                is_prime = False
                break
        if is_prime:
            return act


if not os.path.isfile(FILE_CREDENTIALS):
    print('Credential file "%s" does not exist!!!' % FILE_CREDENTIALS)
    exit(1)

with open(FILE_CREDENTIALS) as credentials_file:
    credentials = json.load(credentials_file)

# I have started conversation manually
# https://twitter.com/AlicePrimes/status/899195226459426816
state = {KEY_BOT: 0, KEY_NUM: 2, KEY_ID: '899195226459426816'}
if os.path.isfile(FILE_STATE):
    with open(FILE_STATE) as state_file:
        state = json.load(state_file)

print("Current state: " + repr(state))
next_prime = find_next_prime(state[KEY_NUM])
print("Next prime will be: " + (str)(next_prime))

# Pick next bot
next_bot = state[KEY_BOT] ^ 1

# Authenticate
act_c = credentials[next_bot]
auth = tweepy.OAuthHandler(
    act_c['consumer_key'],
    act_c['consumer_secret']
)
auth.set_access_token(
    act_c['access_token'],
    act_c['access_token_secret']
)
api = tweepy.API(auth)

# like previous status
api.create_favorite(state[KEY_ID])

# Construct tweet
tweet = ""
tweet += random.choice([
    'Not bad',
    'Good try',
    'Wow,',
    'I didn\'t expected that',
    'You were lucky'
])

tweet += " "
tweet += BOT_NAMES[state[KEY_BOT]]
tweet += ". "
tweet += random.choice([
    'Try beat ',
    'I am saying ',
    'You cannot beat ',
    'My wining number is '
])
tweet += (str)(next_prime)
tweet += " (https://prime-numbers.info/number/" + (str)(next_prime) + ")."

tweet += " #math #mathchat #primes #bot"
print(
    "Tweeting as " +
    BOT_NAMES[next_bot] +
    " (" + (str)(len(tweet)) + "): " +
    tweet
)

# Tweet
result = api.update_status(
    status=tweet,
    in_reply_to_status_id=state[KEY_ID]
)

# Update state
with open(FILE_STATE, 'w') as state_file:
    json.dump(
        {
            KEY_BOT: next_bot,
            KEY_NUM: next_prime,
            KEY_ID: result.id_str
        },
        state_file
    )
