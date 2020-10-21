with open('index.html', 'rb') as fp:
    html = fp.read()

house = {}


async def application(scope, receive, send):
    if scope['type'] == 'websocket':
        room = scope['path']
        event = await receive()
        if event['type'] == 'websocket.connect':
            if room not in house:
                house[room] = {'count': 1, 'sends': [send]}
                room = house[room]
                await send({'type': 'websocket.accept'})
            elif house[room]['count'] == 1:
                room = house[room]
                room['count'] = 2
                room['sends'].append(send)
                await send({'type': 'websocket.accept'})
                await room['sends'][0]({'type': 'websocket.send', 'text': 'black'})
                await room['sends'][1]({'type': 'websocket.send', 'text': 'white'})
            else:
                await send({'type': 'websocket.close', 'code': 403})
                return
            while True:
                event = await receive()
                if event['type'] == 'websocket.disconnect':
                    break
                elif event['type'] == 'websocket.receive':
                    for _send in room['sends']:
                        if _send is not send:
                            await _send({'type': 'websocket.send', 'text': event['text']})
    elif scope['type'] == 'http':
        request = await receive()
        if request['type'] == 'http.request':
            with open('index.html', 'rb') as fp:
                html = fp.read()
            await send({'type': 'http.response.start', 'status': 200})
            await send({'type': 'http.response.body', 'body': html})
