import random, re

LINK_URL = "https://coolors.co/"
COLOR_API_URL = "https://www.thecolorapi.com/id?hex="
COLOR_IMG_API_URL = "https://singlecolorimage.com/get/"

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
        "That's not a shade of blue, you nincompoop."
    ]
    return responses[random.randint(0, len(responses) - 1)]
