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
    utils.schedule_poll(poll)
    await patch_poll_emoji(poll)
    utils.schedule_poll_result(poll)

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

async def patch_poll_emoji(poll):
    choices = await poll.get_votes()
    try:
        message = await client.get_guild(utils.GUILD_ID).get_channel(utils.BOT_CHANNEL_ID).fetch_message(poll.active_poll_id)
    except discord.HTTPException as e:
        print("Unable to fetch message" + e.text + " - " + str(e.code))
        return
    for choice in choices:
        emoji = await poll.check_emoji(choice)
        if not emoji:
            emoji = await poll.post_emoji(choice, poll.api_url + choice[1:] + "/100x100.png")
        else:
            print(f"Found emoji {emoji.name}")
        if emoji:
            await message.add_reaction(emoji)

# Run the client with the Discord API token
client.run(os.environ.get("DISCORD_TOKEN"))
