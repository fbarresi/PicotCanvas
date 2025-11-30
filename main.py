print("Start!")

# wlan connectivity

import network
import time
import machine

network.hostname("PicotCanvas")

led = machine.Pin("LED", machine.Pin.OUT)
led.value(0)

try:
    from secrets import secrets
    ssid = secrets['WIFI_SSID']
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    wlan_scan = [name.decode('utf-8') for name, *args in wlan.scan()]
    print("Connecting to", ssid)
    wlan.connect(ssid, secrets['WIFI_PASSWORD'])
    print("wait up to 60 seconds for connection...")
    for x in range(60):
        if wlan.isconnected():
            break
        else:
            time.sleep(1)
            led.value(x%2)
    if wlan.isconnected():
        print("Connected to", ssid)
        ip, nm = wlan.ipconfig('addr4')
        print(f"Listening on http://{ip}:80")
        print(f"Listening on http://{network.hostname()}.local")
    else:
        raise Exception("unable to connect")
except (ImportError, Exception) as e:
    print("Error:", e)
    print("no secrets found or unable to connect: start in AP mode")
    ap = network.WLAN(network.WLAN.IF_AP)
    ap.config(ssid='RP2-AP', key='Picot421')
    ap.active(True)
    print(f"Listening on http://{network.hostname()}/")

led.value(0)
print("init completed")

def get_wlan_list(self):
    return wlan_scan

# e-paper display

import epd

screen = epd.EPD()

# web application
import os
import asyncio
from microdot import Microdot, send_file
setattr(Microdot, 'get_wlan_list', get_wlan_list)

from connectivity import conn_app
from upload import upload_app
from files import static_app


def create_app():
    app = Microdot()
    app.mount(conn_app, url_prefix='/wlan')
    app.mount(upload_app, url_prefix='/upload')
    app.mount(static_app, url_prefix='/static')
    return app

main_app = create_app()

@main_app.route('/')
async def index(request):
    return send_file('static/index.html')

@main_app.route('/clear')
async def clear(request):
    try:
        os.remove("static/image-preview.jpg")
    except OSError:
        pass
    try:
        os.remove("images/image.bin")
    except OSError:
        pass
    screen.init()
    screen.clear()
    time.sleep(1)
    screen.sleep()
    return "display cleared"

@main_app.route('/update')
async def update(request):
    try:
        with open("images/image.bin", "rb") as f:
            pass
    except OSError:
        return "no image found"
    screen.init()
    screen.display_image()
    time.sleep(1)
    screen.sleep()
    return "display updated"


main_app.run(port=80, debug=True)
#async def run_server():
#    main_app.run(port=80, debug=True)
    
#asyncio.create_task(run_server())