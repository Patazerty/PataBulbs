import sys
import argparse
from yeelight import Bulb

def valid_color(s):
    if s[0] == '#':
        s = s.lstrip('#')
    if len(s) == 6:
        try:
            return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
        except:
            raise argparse.ArgumentTypeError("Color is not in a valid hex type")
    else:
        raise argparse.ArgumentTypeError("Color must be in hex")

parser = argparse.ArgumentParser(description='Manage yeelight bulbs')
parser.add_argument('bulbs', type=str, nargs='+', help='address[es] of bulb[s]')
parser.add_argument('-s', '--switch', help='toggle the light', action="store_true")
parser.add_argument('-b', '--brightness', help='set the brightness', type=int)
onoff = parser.add_mutually_exclusive_group()
onoff.add_argument('--on', help='turn on the light', action="store_true")
onoff.add_argument('--off', help='turn off the light', action="store_true")
colors = parser.add_mutually_exclusive_group()
colors.add_argument('-t', '--temp', help='set the white color temp', type=int)
colors.add_argument('-c', '--color', help='set the rgb color', type=valid_color)
args = parser.parse_args()

for bulbaddr in args.bulbs:
    bulb = Bulb(bulbaddr)
    if args.switch:
        status = bulb.get_properties()
        if status['power'] == "off":
            bulb.turn_on()
        else:
            bulb.turn_off()
    if args.on:
        bulb.turn_on()
    elif args.off:
        bulb.turn_off()
    if args.brightness is not None:
        bulb.set_brightness(args.brightness)
    if args.temp is not None:
        bulb.set_color_temp(args.temp)
    elif args.color is not None:
        bulb.set_rgb(args.color[0], args.color[1], args.color[2])
    
