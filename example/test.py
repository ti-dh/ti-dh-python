from typing import Optional
from fastapi import FastAPI
from fastapi import Form
import json, sys
sys.path.append('../')

import dh as model

app = FastAPI()


# YOU can get a client in ti-dh-php/example
# It's a client via PHP curl, very easy to use
# or maybe you can write a python client


@app.get("/getdhbasedata")
def init():
    o_dh = model.Dh()
    dh_map = o_dh.init()

    # storage necessary data to a cache
    # in production env, usually KV like redis is best
    # when exchange over, the data can be remove
    o_file = open("./data.log", "w+")
    o_file.write(json.dumps(dh_map))

    d_ret = {'p': dh_map['p'], 'g': dh_map['g'], 'server_number': dh_map['processed_server_number']}
    return json.dumps(d_ret)

@app.post("/postdhclientdata")
def exec(client_number: str = Form(...)):

    # fetch the necessary data from cache
    # the calculate the key with compute_share_key method
    o_file = open("./data.log", "r")
    dh_map_json = o_file.read()
    dh_map = json.loads(dh_map_json)

    o_dh = model.Dh()
    # DONT return key to client in production!!!!!!!
    # this is just for example below, it's just convenient for you to verify
    # the key in server and the key in client
    key = o_dh.compute_share_key(client_number, dh_map["server_number"], dh_map["p"])
    return json.dumps({"key":key})