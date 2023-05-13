import discord
import requests


class Embeds:

    _LINK_URL = "https://coolors.co/"
    _COLOR_API_URL = "https://www.thecolorapi.com/id?hex="
    _COLOR_IMG_API_URL = "https://singlecolorimage.com/get/"


    def __init__(self, color):
        self.color = color
        self.url = self._LINK_URL + self.color[1:]
        self.title = self.get_color_name()
        self.description = self.color
        self.image = self._COLOR_IMG_API_URL + self.color[1:] + "/400x400"
        self.author = "BlueBot"
        self.footer = "Brought to you by Deez Nutz"
        

    # A function that makes an API cann to thecolorapi.com to get the color information
    def get_color_name(self):
        response = requests.get("https://www.thecolorapi.com/id?hex=" + self.color[1:])
        return response.json()["name"]["value"]
    
    # Replace the hex prefix with 0x and convert the hex code to an integer
    def get_color_with_hex_prefix(self):
        print(int(self.color.replace("#", "0x"),16))
        return int(self.color.replace("#", "0x"), 16)

    # Initialize the discord EmbedBuilder
    def get_embed(self):
        try:
            embed = discord.Embed(title=self.title, color=self.get_color_with_hex_prefix(), url=self.url, description=self.description)
        except TypeError:
            embed = discord.Embed(title=self.title)
            print("Unable to make embed")

        embed.set_image(url=self.image)
        embed.set_author(name=self.author, url=self.url, icon_url=self.url)
        embed.set_footer(text=self.footer)

        return embed