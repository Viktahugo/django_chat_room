import asyncio
from urllib import response
import websockets, json, os
from binance.client import Client
from binance.enums import *
from threading import Thread
from time import sleep
import sqlite3


connected = set()
wss = []

module_dir = os.path.dirname(__file__)
db_file = os.path.join(module_dir, 'db.sqlite3')


def get_message():
    messages = None
    try:
        sqliteConnection = sqlite3.connect(db_file)
        print("Database is Successfully Connected to SQLite")
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT id, username, msg_type, message, date_added FROM chatApp_message order by strftime('%s', date_added) desc")
        messages = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        if not messages is None:
            return json.dumps(messages)
        

async def consumer_handler(websocket, path):
    task = []
    
    async for message in websocket:
        data = json.loads(message)
        # print(f"Path: {path}")
        if data['type'] == 'new':
            resp = None
            try:
                sqliteConnection = sqlite3.connect(db_file)
                cursor= sqliteConnection.cursor()
                print("Database Connected...")
                print(f"SELECT message FROM chatApp_message where id = '{data['id']}' ")
                cursor.execute(f"SELECT username, message, msg_type FROM chatApp_message where id = '{data['id']}' ")
                row= cursor.fetchone()
                if row[2] == '0':
                    msg = (row[1]).replace("\n", "<br>")
                    resp = {
                        'type':'render_new',
                        'message':str('<div class="d-flex w-100"><div class="col-auto pe-2"><b>'+row[0]+':</b></div><div class="col-auto flex-shrink flex-grow-1 w-min-content mb-0">'+msg+"</div></div>"),
                        'id' : data['id']
                    }
                elif row[2] == '1':
                    resp = {
                        'type':'render_new',
                        'message':str("<p class='mb-0 text-center text-muted'><b>"+row[0]+":</b> joined the conversation</p> "),
                        'id' : data['id']
                    }
                elif row[2] == '2':
                    resp = {
                        'type':'render_new',
                        'message':str("<p class='mb-0 text-center text-muted'><b>"+row[0]+":</b> has left the room</p> "),
                        'id' : data['id']
                    }
                cursor.close()
            except:
                resp = None
            if not resp is None:
                for ws in connected:
                    task.append(asyncio.create_task(ws.send(json.dumps(resp))))
                    await asyncio.wait(task)
async def message_feed(websocket, path):
    while(True):
        try:
            resp = json.dumps({"type":"is_message","message":"test"})
            task = asyncio.create_task(websocket.send(resp))
            await asyncio.wait([task])
        except Exception as err:
            print(err)
            break

        await asyncio.sleep(1)


async def server(websocket, path):
    #Register
    connected.add(websocket)
    print("Websocket : ",websocket," registered")
    try:
        consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
        # feeds = asyncio.ensure_future(message_feed(websocket, path))
        done, pending = await asyncio.wait([consumer_task])
        for task in pending:
            task.cancel()
    except Exception as ex:
        # print(ex)
        print("Task Future Done")
    finally:
        # Unregister.
        connected.remove(websocket)
        print("Websocket : ",websocket," unregistered")


start_server = websockets.serve(server, "localhost", 6023)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(start_server)
    loop.run_forever()
except KeyboardInterrupt as ex:
    print("KeyboardInterrupt: Server Closed.")
finally:
    try:
        for task in asyncio.all_tasks():
            print(task)
            task.cancel()
    except RuntimeError as re:
        # print(re)
        print("Runtime Error:")
    except Exception as ex:
        print("Exception Error")
        # print(ex)

    
