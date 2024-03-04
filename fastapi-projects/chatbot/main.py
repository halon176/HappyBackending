from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from assets import links, base_url

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_json({"titolo": "Benvenuto, sono Lucilla! Come posso aiutarti?"})
    while True:
        try:
            data = await websocket.receive_text()
            data = data.lower()
            links_to_send = []
            for link in links:
                for tag in link["tags"]:
                    if tag in data:
                        links_to_send.append({"titolo": link["titolo"], "url": base_url + link["url"]})
                        break
            if links_to_send:
                r = {"titolo": "Questi link ti potrebbero essere utili:", "links": links_to_send}
                await websocket.send_json(r)
            else:
                await websocket.send_json({"titolo": "Non ho trovato nulla, verrai messo in contatto con un operatore"})
                with open("fallimenti.txt", "a") as f:
                    data = data.replace("\n", " ")
                    f.write(f"{datetime.now()} - {data}\n")
        except WebSocketDisconnect:
            break
