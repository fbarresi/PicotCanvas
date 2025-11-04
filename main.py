print("Start!")

# wlan connectivity

import network
import time

try:
    from secrets import secrets
    ssid = secrets['WIFI_SSID']
    wlan = network.WLAN(network.WLAN.IF_STA)
    print("Connecting to", ssid)
    wlan.connect(ssid, secrets['WIFI_PASSWORD'])
    print("wait up to 60 seconds for connection...")
    for x in range(10):
        if wlan.isconnected():
            break
        else:
            time.sleep(1)
    if wlan.isconnected():
        print("Connected to", ssid)
        ip, nm = wlan.ipconfig('addr4')
        print(f"Listening on http://{ip}:80")
    else:
        raise Exception("unable to connect")
except (ImportError, Exception) as e:
    print("Error:", e)
    print("no secrets found or unable to connect: start in AP mode")
    ap = network.WLAN(network.WLAN.IF_AP)
    ap.config(ssid='RP2-AP', key='Picot42')
    ap.active(True)        

print("init completed")

# web application

from microdot import Microdot
from connectivity import conn_app

def create_app():
    app = Microdot()
    app.mount(conn_app, url_prefix='/wlan')
    return app

main_app = create_app()

@main_app.route('/')
async def index(request):
    return 'Hello, world!'

#main_app.run(port=80, debug=True)

