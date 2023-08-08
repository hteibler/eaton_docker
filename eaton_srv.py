#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from datetime import datetime
import json
import sys
import traceback
from xComfortAPI import xComfortAPI
from data.parameter import *

def do_actor(pa):
    global my_house

    params = {x[0] : x[1] for x in [x.split("=") for x in pa[0:].split("&") ]}
    actor = params["actor"]

    if actor[0:3] != "xCo":
        actor = f'xCo:{params["actor"]}_u0'
    state = params["set"]
    try:
        hz = params["hz"]
    except:
        hz = HOMEZONE

    #print("actor:",actor,state)
    result=my_house.switch(hz, actor, state)
    print(15*"-",'hz', actor, "S:"+state+" res:",result)
    if result == False or result == [{}]:
        my_house._get_session_id()
        print(my_house)
        result=my_house.switch(hz, actor, state)

    print(15*" ",hz, actor, "S:"+state+" res:",result)
    #self.wfile.write(json.dumps(result).encode('utf-8'))
    #                self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    return(result)

def do_list():
    global my_house
    try:
        result=my_house.get_zone_devices()
    except Exception as e:
        my_house._get_session_id()
        result=my_house.get_zone_devices()

    #self.wfile.write(json.dumps(result[0]).encode('utf-8'))
    #                for zone in result:
    #                    for dev in zone["devices"]:
    #                        print('"',dev["id"],'"  ',dev["id"]," ",dev["name"],sep="")#,dev["value"])

    actors=[]
    for zone in result:
        zoneId=zone["zoneId"]
        for dev in zone["devices"]:
            actor={}
            actor["id"]=dev["id"]
            actor["name"]=dev["name"]
            actor["type"]=""
            actor["zone"]=zoneId
            actor["floor"]=""
            actor["group"]=""
            actor["room"]=""
            actors.append(actor)

    return(actors)

def do_set(pa):
    result=[]
    params = {x[0] : x[1] for x in [x.split("=") for x in pa[0:].split("&") ]}
    set = params["set"]
    del params["set"]
    for key, value in params.items():
        print("kv",key, value)
    
    for a in actors:
        if a[set] == key:
            do_pa = f'actor={a["id"]}&set={value}&hz={a["zone"]}'
            r= do_actor(do_pa)
            result.append(r)

    return result

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        global my_house
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        #self.wfile.write("Result <br>".encode('utf-8'))
        p=self.path
        print(now,"path",p)
        try:
            if p.find("favicon.ico") == True:
                #print("favicon")
                #self.wfile.write("ok")
                return True
            if p.find("?") == -1:
                #print("error no command")
                return False
            pa = p.split("?")[1]
            uu = p.split("?")[0][1:]

            if uu == "actor":  ret= do_actor(pa)
            if uu == "list":
                ret= do_list()
                print("done list")
                # self.wfile.write(json.dumps(ret).encode('utf-8'))

            if uu == "set":  ret= do_set(pa)

            if uu == "scene":  # not finished !!
                params = {x[0] : x[1] for x in [x.split("=") for x in pa[0:].split("&") ]}
                scene = f'xCo:{params["scene"]}_u0'
                state = params["set"]
                #result=my_house.switch('hz_1', actor, state)
                #print(15*" ",'hz_1', actor, "S:"+state+" res:",result["status"])
                self.wfile.write(json.dumps(result).encode('utf-8'))
                # self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

            if uu == "err": x = 1/0

            self.wfile.write(json.dumps(ret).encode('utf-8'))


        except Exception as e:
            print("GET:",type(e))
            print("GET:",e.args)
            traceback.print_exc()
            result={}
            result["status"]="error"
            result["error"]=str(e)
            if str(e)== "Zone":
                my_house = xComfortAPI(shcurl, username, password, verbose=False)

            print(15*" ","ERROR:",result)
            self.wfile.write(json.dumps(result).encode('utf-8'))

            pass


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))

        print (post_data.decode('utf-8'),"*****")

        #self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def log_message(self, format, *args):
        return


def run(server_class=HTTPServer, handler_class=S, port=9997):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd... at ',port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("main:",e)
    httpd.server_close()
    print('Stopping httpd...')

if __name__ == '__main__':

    actors = {}
    actors_file = './data/actors.json'
    try:
        if os.path.isfile(actors_file):
            with open('./data/actors.json') as f:
                actors = json.load(f)

    except Exception as error:
        print(80*"-")
        print("somethings wrong with actors.json")
        print("Error:",error)
        print(80*"-")
        actors = {}
        pass
    # get this list from http://192.168.0.95:9999/list?
    # build your groups and floors


    #actors=a #json.loads(a)

    my_house = xComfortAPI(shcurl, username, password, verbose=False)
    #my_house._get_session_id()

    #print (actors)

    run()
