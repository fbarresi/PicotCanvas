from microdot import Microdot, send_file, Request

upload_app = Microdot()
Request.max_content_length = 512 * 1024 # 500kB

@upload_app.post('/image')
async def upload(request):
    # obtain the filename and size from request headers
    filename = request.headers['Content-Disposition'].split(
        'filename=')[1].strip('"')
    size = int(request.headers['Content-Length'])
    print("received:",filename, size)
    # sanitize the filename
    filename = filename.replace('/', '_')
    
    imagename = 'image.bin'

    # write the file to the files directory in 1K chunks
    with open('images/' + imagename, 'wb') as f:
        while size > 0:
            chunk = await request.stream.read(min(size, 1024))
            f.write(chunk)
            size -= len(chunk)

    print('Successfully saved file: ' + filename)
    return 'Image successfully saved'
