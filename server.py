import json

with open('index.html', 'rb') as fp:
    html = fp.read()

house = {}


async def application(scope, receive, send):
    if scope['type'] == 'websocket':
        event = await receive()
        if event['type'] != 'websocket.connect':
            return
        await send({'type': 'websocket.accept'})
        event = await receive()
        data = json.loads(event['text'])
        if data['type'] != 'EnterRoom' or not data['id'] or not data['room']:
            await send({'type': 'websocket.close', 'code': 403})
            return
        room_id = data['room']
        user_id = data['id']
        if room_id not in house:
            house[room_id] = {
                'black': None,
                'white': None,
                'visitors': [],
                'pieces': [],
                'sends': [],
            }
        room = house[room_id]
        room['sends'].append(send)
        old = False
        if room['black'] == user_id or room['white'] == user_id:
            old = True
        else:
            if room['black'] is None:
                room['black'] = user_id
            elif room['white'] is None:
                room['white'] = user_id
            else:
                room['visitors'].append(user_id)
        visiting = room['black'] != user_id and room['white'] != user_id
        await send({'type': 'websocket.send', 'text': json.dumps({
            'type': 'InitializeRoomState',
            'pieces': room['pieces'],
            'visitors': len(room['visitors']),
            'visiting': visiting,
            'black': room['black'] == user_id if not visiting else bool(len(room['pieces']) % 2),
            'ready': bool(room['black'] and room['white']),
        })})
        if not old and (room['black'] == user_id or room['white'] == user_id):
            for _send in room['sends']:
                if _send == send:
                    continue
                await _send({'type': 'websocket.send', 'text': json.dumps({
                    'type': 'AddPlayer',
                    'ready': bool(room['black'] and room['white']),
                })})
        while True:
            event = await receive()
            if event['type'] == 'websocket.disconnect':
                print(len(room['sends']))
                room['sends'].remove(send)
                print(len(room['sends']))
                break
            data = json.loads(event['text'])
            if data['type'] == 'ChangeRoom':
                pass
            elif data['type'] == 'ApplyChange':
                pass
            elif data['type'] == 'AcceptChange':
                pass
            elif data['type'] == 'RejectChange':
                pass
            elif data['type'] == 'DropPiece':
                room['pieces'].append((data['x'], data['y']))
                for _send in room['sends']:
                    if _send == send:
                        continue
                    await _send({'type': 'websocket.send', 'text': json.dumps({
                        'type': 'DropPiece',
                        'x': data['x'],
                        'y': data['y'],
                    })})
    elif scope['type'] == 'http':
        request = await receive()
        if request['type'] == 'http.request':
            await send({'type': 'http.response.start', 'status': 200})
            await send({'type': 'http.response.body', 'body': html})
