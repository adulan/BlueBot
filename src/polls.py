import discord, time, os, urllib
import utils
from datetime import datetime, timedelta


class Poll:
    def __init__(self, client):
        self.title = "Blue of the Week Poll"
        self.api_url = "https://singlecolorimage.com/get/"
        self.active_poll_id = 0
        self.client = client
        self.nominations = []

    async def post_poll(self):
        embed = discord.Embed(title=self.title,
                        description="Vote for your favorite shade of blue!",
                        colour=int(utils.BLUE_OF_THE_WEEK.replace("#", "0x"), 16),
                        timestamp=datetime.utcnow())
        
        choices = await self.get_votes()
        self.nominations = choices

        fields = [("Options", "\n".join([f"{choice}" for choice in choices]), False),
                    ("Instructions", "React to cast a vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        message = await self.client.get_guild(utils.GUILD_ID).get_channel(utils.BOT_CHANNEL_ID).send(embed=embed)
        await time.sleep(60) # prevent double posting of poll

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
            if emoji:
                await message.add_reaction(emoji)
                self.active_poll_id = message.id


    # a function to create an emoji and post it to the discord guild
    async def post_emoji(self, name, url):
        try:
            image = urllib.request.urlretrieve(url, f"{name}.png")
            image = open(f"/usr/src/app/{name}.png", "rb")
            try:
                emoji = await self.client.get_guild(utils.GUILD_ID).create_custom_emoji(name=name[1:], image=image.read())
            except discord.HTTPException as e:
                print("Unable to create emoji" + e.text + " - " + str(e.code))
                return False
            image.close() 
            print(emoji)
            print(f"Created new emoji {emoji.name}")
        except discord.HTTPException as e:
            print("Unable to create emoji" + e.text + " - " + str(e.code))
            return False
        return emoji

    # a function to check if an emoji exists in the guild
    async def check_emoji(self, name):
        for emoji in self.client.get_guild(utils.GUILD_ID).emojis:
            if emoji.name == name[1:]:
                return emoji
        return False
    
    # a function to get all votes
    # searches the BOT_CHANNEL_ID for any messages containing a blue hex code posted in the last week
    # returns an array of the hex codes
    async def get_votes(self):
        votes = []
        guild = self.client.get_guild(utils.GUILD_ID)
        channel = guild.get_channel(utils.BOT_CHANNEL_ID)

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

    async def complete_poll(self):
        try:
            channel = self.client.get_guild(utils.GUILD_ID).get_channel(utils.BOT_CHANNEL_ID)
            message = await channel.fetch_message(self.active_poll_id)
        except discord.HTTPException as e:
            print("Unable to fetch poll" + e.text + " - " + str(e.code))
            return
        message_id = message.id
        
        # get the reactions from the message and sort them by count - highest to lowest
        reactions = message.reactions
        reactions.sort(key=lambda x: x.count, reverse=True)

        # get the top reaction
        top_reaction = reactions[0]  

        await message.delete()
        await self.post_result(top_reaction.emoji.name)
        self.active_poll_id = 0


    async def post_result(self, hex_code):
        embed = discord.Embed(title="Blue of the Week",
                        description=f"The winner is #{hex_code}!",
                        colour=int(hex_code.replace("#", "0x"), 16),
                        url=utils.LINK_URL + hex_code,
                        timestamp=datetime.utcnow())
        embed.set_image(url=utils.COLOR_IMG_API_URL + hex_code + "/400x400")
        embed.set_author(name="BlueBot", url=utils.LINK_URL + hex_code, icon_url=utils.LINK_URL + hex_code)
        embed.set_footer(text="Brought to you by Deez Nutz")

        utils.BLUE_OF_THE_WEEK = hex_code
        try:
            await self.client.get_guild(utils.GUILD_ID).get_channel(utils.BOT_CHANNEL_ID).send(embed=embed)
            await time.sleep(60)
        except discord.HTTPException as e:
            print("Unable to post result" + e.text + " - " + str(e.code))
        await self.delete_emojis()



    async def delete_emojis(self):
        guild = self.client.get_guild(utils.GUILD_ID)
        for emoji in guild.emojis:
            if "#"+emoji.name in self.nominations:
                try:
                    await emoji.delete()
                except discord.HTTPException as e:
                    print("Unable to delete emoji" + e.text + " - " + str(e.code))
                print(f"Deleted emoji {emoji.name}")
