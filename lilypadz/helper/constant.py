"""This file holds the necessary constants for the project."""
import colorlover

# Toad name and their corresponding hop numbers.
TOAD_HOP = {
    "Atlas": [
        5, 8, 9, 13, 14, 18, 19, 20, 21, 25, 26, 36, 43, 44
    ],
    "Fortuna": [
        2, 5, 7, 9, 11, 13, 14, 15, 16, 18, 20, 21, 23, 25, 26, 29, 31, 32,
        37, 39, 40, 42, 43, 45, 53
    ],
    "Gelos": [
        2, 3, 10, 11, 13, 14, 15, 16, 17, 18, 19, 22, 23, 26, 30, 32, 35, 37,
        38, 39, 42, 43, 44, 45, 47, 48, 50
    ],
    "Talos": [
        9, 15, 16, 17, 18, 20, 21, 24, 31, 32, 33, 38, 41, 42, 44, 45, 46, 50,
        52, 53, 54
    ],
    "Zeus": [
        1, 4, 5, 8, 11, 14, 16, 19, 20, 23, 28, 33, 35, 36, 38, 41, 42, 43, 44,
        45, 46, 47, 48, 49
    ]
}

# Toad name and their corresponding color scale.
TOAD_COLOR = {
    "Atlas": colorlover.interp(colorlover.scales["5"]["seq"]["Purples"], 7),
    "Fortuna": colorlover.interp(colorlover.scales["5"]["seq"]["Blues"], 7),
    "Gelos": colorlover.interp(colorlover.scales["5"]["seq"]["Oranges"], 7),
    "Talos": colorlover.interp(colorlover.scales["5"]["seq"]["Greens"], 7),
    "Zeus": colorlover.interp(colorlover.scales["5"]["seq"]["Reds"], 7)
}

# Color to distinguish blink and sight.
SIGHT_BLIND_COLOR = {
    "Sighted": colorlover.scales["3"]["qual"]["Set2"][0],
    "Blind": colorlover.scales["3"]["qual"]["Set2"][1],
    "Unknown": colorlover.scales["3"]["qual"]["Set2"][2]
}
