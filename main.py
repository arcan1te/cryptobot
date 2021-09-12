import discord
import requests

# getting crypto data
def getCryptoPrices(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  r = requests.get(url=URL)
  data = r.json()

  # putting the cryptocurrencies and their prices in db
  for i in range(len(data)):
    db[data[i]['id']] = data[i]['current_price']

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

# check if a cryptocurrency is supported in this bot
def isCryptoSupported(crypto):
  if crypto in db.keys():
    return True
  else:
    return False

client = discord.Client()

@client.event
async def on_ready():
  print(f'You have logged in as {client.user}')
  channel = discord.utils.get(client.get_all_channels(),name='crypto')
  await client.get_channel(channel.id).send('bot is now online!')

# called when there is a message in the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  # send crypto price directly 
  if message.content.lower() in db.keys():
    await message.channel.send(f'The current price of {message.content} is: {getCryptoPrices(message.content.lower())} USD')

  # list all the available coins
  if message.content.startswith('$list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)

  # check whether a coin is being supported
  if message.content.startswith('$support '):
    cryptoToBeChecked = message.content.split('$support ',1)[1].lower()
    await message.channel.send(isCryptoSupported(cryptoToBeChecked))

keep_alive()
BOT_TOKEN = 'TOKEN HERE'
client.run(BOT_TOKEN)