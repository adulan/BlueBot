import discord
import embeds, utils, polls
import asyncio, os, datetime

# Define the Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

poll = polls.Poll(client)


# Define an event handler for when the client connects to Discord
@client.event
async def on_ready():
    print("Logged in as {0.user}.".format(client))
    print(datetime.datetime.now())

# Define an event handler for when a message is sent in a channel
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Find all hexadecimal color codes in the message
    hex_codes = utils.hex_pattern.findall(message.content)
    
    # Check if any of the hex codes are shades of blue
    for hex_code in hex_codes:
        try:
            if utils.is_shade_of_blue(hex_code):
                # Send an embeded message with the color swatch
                embedded_message = embeds.Embeds(hex_code).get_embed()
                await message.channel.send(embed = embedded_message)
            else:
                await message.reply(utils.is_not_blue_message())
        except:
            print("Unable to send message")

# Run the client with the Discord API token
client.run(os.environ.get("DISCORD_TOKEN"))
