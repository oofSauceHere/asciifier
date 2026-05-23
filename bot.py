import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import cv2
import numpy as np
import math
import sys
import requests
from io import BytesIO

SPECTRUM = " .:-=+*#%@"
IMG_SPECTRUM = [cv2.cvtColor(cv2.imread(f"util/font{i}.png"), cv2.COLOR_RGB2RGBA) for i in range(0, 10)]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

def convert_img(url, pixel_size, bg_color, invert_color):
    response = requests.get(url)
    img_stream = BytesIO(response.content)
    img_stream.seek(0)
    file_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    h, w = img.shape
    pix = pixel_size
    small = cv2.resize(img, (w // pix, h // pix))

    white = bg_color == "n"
    invert = invert_color != "n"

    new_h = (h // pix) * 5
    new_w = (w // pix) * 5

    text = np.zeros((new_h, new_w, 4), np.uint8)
    for i in range(0, new_h):
        for j in range(0, new_w):
            text[i][j] = [0, 0, 0, 255]

    with open("test.txt", "w") as f:
        for i in range(0, h // pix):
            line = ""
            for j in range(0, w // pix):
                for k in range(0, 5):
                    for l in range(0, 5):
                        if(IMG_SPECTRUM[int((small[i][j] / 256) * 10)][k][l][3] != 0):
                            text[i*5 + k][j*5 + l] = IMG_SPECTRUM[int((small[i][j] / 256) * 10)][k][l]
                line += SPECTRUM[int((small[i][j] / 256) * 10)]
            f.write(line + "\n")

    colors_rgb = cv2.imread("util/colors.png")
    colors = cv2.cvtColor(colors_rgb, cv2.COLOR_RGB2RGBA)
    for i in range(0, new_h):
        for j in range(0, new_w):
            if not invert:
                if not (text[i][j] == [0, 0, 0, 255]).all():
                    # text[i][j] = img2_fix[i][j]
                    text[i][j] = colors[math.floor((i / new_h) * 256)][math.floor((j / new_w) * 256)]
                elif white:
                    text[i][j] = [255, 255, 255, 255]
            else:
                if (text[i][j] == [0, 0, 0, 255]).all():
                    # text[i][j] = img2_fix[i][j]
                    text[i][j] = colors[math.floor((i / new_h) * 256)][math.floor((j / new_w) * 256)]
                elif not white:
                    text[i][j] = [0, 0, 0, 255]

    # cv2.imwrite(f"out/ac_{filename}", text)
    success, buf = cv2.imencode(".png", text)
    return BytesIO(buf)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        await self.tree.sync()

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'[bot] Logged in as {client.user}')

# image could be url too?
@client.tree.command()
async def convert(interaction: discord.Interaction, image: discord.Attachment, pixel_size: int, bg_color: str, invert_color: str):
    await interaction.response.defer(thinking=True)
    img_stream = convert_img(image.url, pixel_size, bg_color, invert_color)
    img_stream.seek(0)
    await interaction.followup.send(file=discord.File(fp=img_stream, filename="asciified.png"))

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()