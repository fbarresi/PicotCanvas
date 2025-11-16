from microdot import Microdot, send_file

conn_app = Microdot()

@conn_app.get('/')
async def get_connections(request):
    return send_file('static/wlan.html')

@conn_app.post('/connect')
async def connect_to(request):
    ssid = request.form.get('ssid')
    password = request.form.get('password')
    with open("secrets.py", "w") as text_file:
        text_file.write("secrets = {{'WIFI_SSID': '{ssid}','WIFI_PASSWORD': '{password}'}}".format(ssid=ssid, password=password))
    return 'We have received your data, please restart.'

@conn_app.get('/list')
async def connect_to(request):
    return conn_app.get_wlan_list()

print("connectivity wlan-list:", conn_app.get_wlan_list())