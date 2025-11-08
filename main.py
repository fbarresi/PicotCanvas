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
    print("Connecting to", ssid)
    wlan.connect(ssid, secrets['WIFI_PASSWORD'])
    print("wait up to 20 seconds for connection...")
    for x in range(20):
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

print("init completed")

# web application
import asyncio
from microdot import Microdot, send_file
from connectivity import conn_app
from upload import upload_app

def create_app():
    app = Microdot()
    app.mount(conn_app, url_prefix='/wlan')
    app.mount(upload_app, url_prefix='/upload')
    return app

main_app = create_app()

@main_app.route('/')
async def index(request):
    return send_file('static/index.html')


main_app.run(port=80, debug=True)
#async def run_server():
#    main_app.run(port=80, debug=True)
    
#asyncio.create_task(run_server())