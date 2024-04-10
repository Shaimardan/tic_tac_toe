from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import json

from tic_tac_toe_game.logic import TicTacToe
from tic_tac_toe_game.player_type import Player

app = FastAPI()


board = TicTacToe()


async def update_board(manager, data):
    ind = int(data['cell']) - 1
    data['init'] = False
    if not board.board[ind]:
        board.board[ind] = data['player']
        if board.check_winner(data['player'], ind):
            data['message'] = "won"
        else:
            data['message'] = "move"
    else:
        data['message'] = "choose another one"
    await manager.broadcast(data)
    if data['message'] in ['draw', 'won']:
        manager.connections = []


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        if len(self.connections) >= 2:
            await websocket.accept()
            await websocket.close(4000)
        else:
            await websocket.accept()
            self.connections.append(websocket)
            if len(self.connections) == 1:
                await websocket.send_json({
                    'init': True,
                    'player': Player.Player_X.value,
                    'message': 'Waiting for another player',
                })
            else:
                await websocket.send_json({
                    'init': True,
                    'player': Player.Player_O.value,
                    'message': 'Your turn!',
                })
                await self.connections[0].send_json({
                    'init': True,
                    'player': Player.Player_X.value,
                    'message': 'Your turn!',
                })

    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_json(data)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            print(data)
            await update_board(manager, data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except:
        pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)