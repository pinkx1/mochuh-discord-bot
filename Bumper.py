# v 0.01
def bump_function():
    import http.client
    from codecs import encode
    import os
    
    conn = http.client.HTTPSConnection("2ch.hk")
    cookie = os.getenv('cookie')
    boundary = os.getenv('boundary')
    usercode = os.getenv('usercode')
    thread_link = os.getenv('thread_link')
    thread_id = os.getenv('thread_id')

    dataList = []

    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=task;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("post"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=board;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("ch"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=thread;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(thread_id))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=usercode;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(usercode))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=captcha_type;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("2chcaptcha"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=formimages[];'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("(binary)"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=comment;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("bump"))
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'scheme': 'https',
        'path': '/user/posting?nc=1',
        'method': 'POST',
        'authority': '2ch.hk',
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': thread_link,
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cookie': cookie,
        'origin': 'https://2ch.hk',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }

    conn.request("POST", "/user/posting?nc=1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))