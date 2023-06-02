import os, random, re
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

LINK_URL = "https://coolors.co/"
COLOR_API_URL = "https://www.thecolorapi.com/id?hex="
COLOR_IMG_API_URL = "https://singlecolorimage.com/get/"
GUILD_ID = int(os.getenv("GUILD_ID"))
BOT_CHANNEL_ID = int(os.getenv("POLL_CHANNEL_ID"))

# BLUE OF THE WEEK - Variable, but too important to be lower case
if os.getenv("BOTW") != None:
    BLUE_OF_THE_WEEK = os.getenv("BOTW")
else:
    BLUE_OF_THE_WEEK = "#0000FF"

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


def is_not_blue_message():
    responses = [
        "That's not a shade of blue, you idiot.",
        "That's not a shade of blue, you moron.",
        "That's not a shade of blue, you fool.",
        "That's not a shade of blue, you buffoon.",
        "That's not a shade of blue, you dunce.",
        "That's not a shade of blue, you imbecile.",
        "That's not a shade of blue, you simpleton.",
        "That's not a shade of blue, you nincompoop.",
        "That's not a shade of blue, you dolt.",
        "That's not a shade of blue, you ignoramus.",
        "That's not a shade of blue, you douchenozzle.",
        "That's not a shade of blue, you jackass."
    ]
    return responses[random.randint(0, len(responses) - 1)]


def schedule_poll(poll):
    # Nominations posts Sunday 00:00 EDT
    # Nominations closes Friday 23:59 EDT
    # Polls posted Saturday 00:00 EDT = Saturday 04:00 UTC
    
    # time values
    day_of_the_week = "sat"
    hour = "04"
    minute = "00"

    scheduler = AsyncIOScheduler()
    scheduler.add_job(poll.post_poll, CronTrigger(day_of_week=day_of_the_week, hour=hour, minute=minute))
    scheduler.start()
    

def schedule_poll_result(poll):
    # Polls close Saturday 23:45 EDT = Sunday 03:45 UTC
    # time values
    day_of_the_week = "sun"
    hour = "03"
    minute = "45"

    scheduler = AsyncIOScheduler()
    scheduler.add_job(poll.complete_poll, CronTrigger(day_of_week=day_of_the_week, hour=hour, minute=minute))
    scheduler.start()