import os
import re
from time import sleep
import random
import asyncio


# button
from digitalio import DigitalInOut, Direction, Pull
import keypad
import board

# wifi
import wifi
import socketpool

# server
from adafruit_binascii import a2b_base64, b2a_base64 
from adafruit_httpserver import HTTPServer, HTTPResponse

# lights
from Lights import Lights

SSID = "Hat_Control_192_168_4_1"
PORT = 80
TIMEOUT = None
BACKLOG = 2
MAXBUF = 2048
BUTTON_PIN = board.A2

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)
lights = Lights()
button = keypad.Keys((BUTTON_PIN,), value_when_pressed=False, pull=True)


def _getBanner() -> str:
    msg = """
█████   █████            █████         █████████                       █████                       ████ 
░███   ░░███            ░░███         ███░░░░░███                     ░░███                       ░░███ 
░███    ░███   ██████   ███████      ███     ░░░   ██████  ████████   ███████   ████████   ██████  ░███ 
░███████████  ░░░░░███ ░░░███░      ░███          ███░░███░░███░░███ ░░░███░   ░░███░░███ ███░░███ ░███ 
░███░░░░░███   ███████   ░███       ░███         ░███ ░███ ░███ ░███   ░███     ░███ ░░░ ░███ ░███ ░███ 
░███    ░███  ███░░███   ░███ ███   ░░███     ███░███ ░███ ░███ ░███   ░███ ███ ░███     ░███ ░███ ░███ 
█████   █████░░████████  ░░█████     ░░█████████ ░░██████  ████ █████  ░░█████  █████    ░░██████  █████
░░░░░   ░░░░░  ░░░░░░░░    ░░░░░       ░░░░░░░░░   ░░░░░░  ░░░░ ░░░░░    ░░░░░  ░░░░░      ░░░░░░  ░░░░░ 
                                                                                                        
Welcome to Hat Control. Come visit us in the Exploit Village.

Type   help   to see a list of commands.                                                                                             
    """
    return msg

def _gethelp() -> str:
    msg = """List of command:
color [color]   - sets color of lights. 
                    Choose from red, orange, yellow, green, blue, ...
method [method] - sets animation of lights.
                    Choosee from random, sparkle, wheel, pulse, ...
bright [level]  - sets brightness of lights.
                    Choose from low, medium, high
help            - shows this list

Console allows tab completion and listing choices with [command] <double tab>
"""
    return msg

@server.route("/","POST")
def handleForm(request):
    print("POST request")
    raw_text = request.raw_request.decode("utf8")
    lines = raw_text.split('\r\n')
    cmds = lines[-1].split('&')
    resp = ''
    for cmd in cmds:
        print(cmd)
        key, val = cmd.split('=')
        if key == "command":
            if str.lower(val) == 'help':
                resp = _gethelp()
            elif str.lower(val) == 'banner':
                resp = _getBanner()
        elif key == "color":
            color = str.lower(val)
            lights.currentColorMap = color
            resp = f"set color to {color}"
        elif key == "method":
            method = str.lower(val)
            lights.currentMethod = method
            resp = f"set method to {method}"
        elif key == "bright":
            level = str.lower(val)
            if level == "low":
                lights.pixels.brightness = 0.05
            elif level == "medium":
                lights.pixels.brightness = 0.1
            elif level == "high":
                lights.pixels.brightness = 0.3
            resp = f"set brightness to {level}"

    return HTTPResponse(body=resp)

@server.route("/", "GET")
def base(request):  
    print("connection request")
    return HTTPResponse(filename="/index.html")

def init_wifi_ap():
    # at this point, the ESP32-S2 is running as a station (init default), and if desired can connect to any AP
    # the following two lines are not new APIs, but they are useful to test in combination with mode changes:
    wifi.radio.enabled = False  # turns wifi off, mode is retained or can be changed while not enabled
    wifi.radio.enabled = True  # turns wifi back on
    print("Wi-Fi Enabled?", wifi.radio.enabled)
    print("Stopping the (default) station...")
    wifi.radio.stop_station()  # now the device is in NONE mode, neither Station nor Access Point
    # start the AP, `channel` of your choosing, `authmode` of your choosing:
    # The Access Point IP address will be 192.168.4.1
    # ...if that collides with your LAN, you may need to isolate the external station from your LAN
    print("Starting AP...")
    wifi.radio.start_ap(SSID)
    print("AP IP Address:", wifi.radio.ipv4_address_ap)
    print("      Gateway:", wifi.radio.ipv4_gateway_ap)
    print("       Subnet:", wifi.radio.ipv4_subnet_ap)

async def handleLights():
    while True:
        await lights.run()

async def handleServer():
    while True:
        server.poll() 
        await asyncio.sleep(0.5)

async def handleButtonPress():
    while True:
        event = button.events.get()
        if event:
            if event.pressed:
                lights.currentColorMap = random.choice(list(lights.colormaps.keys()))
                lights.currentMethod = random.choice(list(lights.methods.keys()))
                button.events.clear()
        await asyncio.sleep(0.5)

async def main():
    lights_task = asyncio.create_task(handleLights())
    server_task = asyncio.create_task(handleServer())  
    button_task = asyncio.create_task(handleButtonPress())
    await asyncio.gather(lights_task, server_task, button_task)

if __name__ == "__main__":
    init_wifi_ap()
    server.request_buffer_size = MAXBUF
    server.start(str(wifi.radio.ipv4_address_ap))
    asyncio.run(main())
    
    
    