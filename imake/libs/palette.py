from ..dataclasses import HSV

SKIN_PALETTE = [
    HSV(h=15, s=35, v=100),
    HSV(h=25, s=35, v=100),
    HSV(h=35, s=35, v=100),
    HSV(h=25, s=40, v=75),
    HSV(h=25, s=50, v=70),
]

COLOR_PALETTE = [
    HSV(h=41, s=74, v=55),
    HSV(h=40, s=51, v=86),
    HSV(h=15, s=45, v=82),
    HSV(h=77, s=53, v=70),
    HSV(h=177, s=16, v=85),
    HSV(h=28, s=72, v=38),
    HSV(h=315, s=27, v=69),
    HSV(h=14, s=21, v=89),
    HSV(h=210, s=12, v=91),
    HSV(h=217, s=71, v=45),
    HSV(h=25, s=73, v=28),
    HSV(h=20, s=81, v=58),
    HSV(h=33, s=74, v=76),
    HSV(h=214, s=57, v=64),
    HSV(h=1, s=56, v=62),
    HSV(h=9, s=80, v=27),
    HSV(h=334, s=69, v=75),
    HSV(h=195, s=55, v=41),
    HSV(h=138, s=44, v=32),
    HSV(h=180, s=4, v=32),
]

DARK_PALETTE = [
    HSV(h=0, s=0, v=0),  # black
    HSV(h=240, s=51, v=23),
    HSV(h=28, s=72, v=38),
    HSV(h=25, s=73, v=28),
    HSV(h=9, s=80, v=27),
    HSV(h=0, s=0, v=100),  # white
    HSV(h=0, s=100, v=82),
    HSV(h=60, s=100, v=100),
    HSV(h=200, s=100, v=100),
]

PALETTE = {
    "skin": SKIN_PALETTE,
    "color": COLOR_PALETTE,
    "dark": DARK_PALETTE,
}
