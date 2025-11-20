from microdot import Microdot, send_file

static_app = Microdot()

@static_app.route('/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)