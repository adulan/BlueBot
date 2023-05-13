import discord
import embeds
import os
import random
import re

# Define the Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Define the Discord client
client = discord.Client(intents=intents)

# Define the regular expression pattern to match hexadecimal color codes
hex_pattern = re.compile(r"#[0-9A-Fa-f]{6}")

def is_shade_of_blue(hex_code):
    """
    Determines if a given hex code is a shade of blue.

    Args:
        hex_code (str): A hexadecimal color code string.

    Returns:
        bool: True if the hex code is a shade of blue, False otherwise.
    """
    if hex_code[:1] == "#":
        hex_code = hex_code[1:]
    elif hex_code[:2] == "0x":
        hex_code = hex_code[2:]

    # Convert hex code to RGB values
    try:
        red, green, blue = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    except:
        print("Unable to determine if blue")
        return False
    return blue > red and blue > green

# Function to create a message that says the color is not blue
# Include insults to the original author
def is_not_blue_message():
    responses = [
        "That's not a shade of blue, you idiot.",
        "That's not a shade of blue, you moron.",
        "That's not a shade of blue, you fool.",
        "That's not a shade of blue, you buffoon.",
        "That's not a shade of blue, you dunce.",
        "That's not a shade of blue, you imbecile.",
        "That's not a shade of blue, you simpleton.",
        "That's not a shade of blue, you nincompoop."
    ]
    return responses[random.randint(0, len(responses) - 1)]


# Define an event handler for when the client connects to Discord
@client.event
async def on_ready():
    print("Logged in as {0.user}.".format(client))

# Define an event handler for when a message is sent in a channel
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Find all hexadecimal color codes in the message
    hex_codes = hex_pattern.findall(message.content)
    
    # Check if any of the hex codes are shades of blue
    for hex_code in hex_codes:
        try:
            if is_shade_of_blue(hex_code):
                # Send an embeded message with the color swatch
                embedded_message = embeds.Embeds(hex_code).get_embed()
                await message.channel.send(embed = embedded_message)
            else:
                await message.reply(is_not_blue_message())
        except:
            print("Unable to send message")

# Run the client with the Discord API token
client.run(os.environ.get("DISCORD_TOKEN"))
