from microdot import Microdot

conn_app = Microdot()

@conn_app.get('/')
async def get_connections(request):
    # return all customers
    pass

@conn_app.post('/connect')
async def connect_to(request):
    with open("secrets.py", "w") as text_file:
        text_file.write("secrets = %s" % str(request.json))
    pass
