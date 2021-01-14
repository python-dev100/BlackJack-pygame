from PIL import Image
from os import remove
import numpy


"""
This game comes with a processor because originally the names of the cards were numbers from 1 to 52
and the images came with a size of (3000, 4200).
"""
values = ["Ace", "King", "Queen", "Jack", 10, 9, 8, 7, 6, 5, 4, 3, 2]
suits = ["clubs", "spades", "hearts", "diamonds"]

val_num = -1

for i in range(52):
    img = Image.open(str(i + 1) + ".png")
    suit = suits[i % len(suits)]
    if suit == suits[0]:
        val_num += 1
    value = values[val_num % len(values)]
    img = img.resize((100, 140))
    img.save(str(value) + " of " + suit + ".png")
    remove(str(i + 1) + ".png")
back = Image.open("back.png")
back = back.resize((100, 140))
back.save("back.png")

icon = Image.open("King of hearts.png")
icon = icon.resize((32, 32))
icon.save("icon.png")