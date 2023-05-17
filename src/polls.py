import discord, os, urllib
import utils
from datetime import datetime, timedelta


# BLUE OF THE WEEK
BLUE_OF_THE_WEEK = "#71A6D2" # Variable, but too important to be lower case
BOT_CHANNEL_ID = int(os.getenv("POLL_CHANNEL_ID"))

# Nominations posts Sunday 00:00
# Nominations closes Friday 23:59
# Polls posted Saturday 00:00
# Polls close Saturday 23:45

class Poll:
    def __init__(self, client):
        self.title = "Blue of the Week Poll"
        self.api_url = "https://singlecolorimage.com/get/"
        self.polls = []
        self.client = client

    async def post_poll(self, choices):
        embed = discord.Embed(title=self.title,
                        description="Vote for your favorite shade of blue!",
                        colour=int(BLUE_OF_THE_WEEK.replace("#", "0x"), 16),
                        timestamp=datetime.utcnow())

        fields = [("Options", "\n".join([f"{choice}" for choice in choices]), False),
                    ("Instructions", "React to cast a vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        message = await self.client.get_guild(utils.GUILD_ID).get_channel(BOT_CHANNEL_ID).send(embed=embed)

        # add a reaction to the message for each choice
        # check if the emoji already exists in the guild
        # if not, create it
        # add the emoji to the message
        for choice in choices:
            emoji = await self.check_emoji(choice)
            if not emoji:
                emoji = await self.post_emoji(choice, self.api_url + choice[1:] + "/100x100.png")
            else:
                print(f"Found emoji {emoji.name}")
            await message.add_reaction(emoji)
        self.polls.append((message.channel.id, message.id))

        # self.bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now()+timedelta(seconds=hours),
        #                             args=[message.channel.id, message.id])

    # a function to create an emoji and post it to the discord guild
    async def post_emoji(self, name, url):
        try:
            image = urllib.request.urlretrieve(url, f"{name}.png")
            image = open(f"/usr/src/app/{name}.png", "rb")
            emoji = await self.client.get_guild(utils.GUILD_ID).create_custom_emoji(name=name[1:], image=image.read())
            print(emoji)
            print(f"Created new emoji {emoji.name}")
        except discord.HTTPException as e:
            print("Unable to create emoji" + e.text + " - " + str(e.code))
            return False
        return emoji

    # a function to check if an emoji exists in the guild
    async def check_emoji(self, name):
        for emoji in self.client.get_guild(utils.GUILD_ID).emojis:
            if emoji.name == name:
                return emoji
        return False
    
    # a function to get all votes
    # searches the BOT_CHANNEL_ID for any messages containing a blue hex code posted in the last week
    # returns an array of the hex codes
    async def get_votes(self):
        votes = []
        guild = self.client.get_guild(utils.GUILD_ID)
        channel = guild.get_channel(BOT_CHANNEL_ID)

        async for message in channel.history(limit=100):
            if message.author.bot:
                continue
            if message.created_at.timestamp() < (datetime.utcnow() - timedelta(days=7)).timestamp():
                continue
             # Find all hexadecimal color codes in the message
            hex_codes = utils.hex_pattern.findall(message.content)

            # Check if any of the hex codes are shades of blue
            for hex_code in hex_codes:
                if utils.is_shade_of_blue(hex_code) and hex_code not in votes:
                    votes.append(hex_code)
        return votes
