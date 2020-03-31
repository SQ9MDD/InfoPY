#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import serial
import time
import datetime
import platform
from ax25lib import ax25lib
from aprs_parser import aprs_parser
import sqlite3

# 
callsign = 'SQ9MDD-1'
path = 'RFONLY'
host = "10.9.48.5"
port = 8002
debug = False
database = "InfoPyBASE.db"
infopyVer = "InfoPy v.1.0. ALPHA"

parser=aprs_parser()

def create_connection(conn):
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    return conn
    
def add_frame(conn,callsign,path,data,date_time):
    cur = conn.cursor()
    cur.execute("INSERT into historian (callsign,path,data,date_time) VALUES(?,?,?,?)",(callsign,path,data,date_time,))  
    cur.fetchall()
    return

def get_sys():
    msg_data = platform.platform()
    return(msg_data)

def dane(dane):
    global callsign,path,infopyVer
    znak = ""
    comment = ""
    global call_list
    global icon_list
            
    if dane['data'][0] == ":":                            # sprawdzamy tylko wiadmosci
        znak = dane['source'].replace("*","")
        znak_count = len(znak)        
        comment = dane['data'][1:] 
        comment_arr = comment.split(":")
        if(debug):
            print(znak + "," + comment)
            
        if(str(comment_arr[0]).strip() == str(callsign)):           # reagujemy tylko na wiadomości do mnie
            if(debug):
                print(znak + ">" + str(comment_arr[1]))
            ack_sign = str(comment_arr[1]).rfind('{')
            time.sleep(5)
            
            noop = ''
            for i in range (znak_count,9):
                noop = noop + " "              
            
            if(ack_sign >= 1):
                ack_sign = ack_sign + 1
                if(debug):
                    print(str(comment_arr[1])[ack_sign:])
                    print('sending ack')
                msg = ":" + znak + noop + ":ack" + str(comment_arr[1])[ack_sign:]
                ax25.send(source=callsign,destination="APZIPY",rpt=path,message=msg)               
                time.sleep(5)
                
            if(str(comment_arr[1])[:5] == "?APRS"):
                if(debug):
                    print('odpowiadam na ?APRS')
                msg_data = "Support: ?APRS ?DATE ?VER"
                msg = ":" + znak + noop + ":" + msg_data
                ax25.send(source=callsign,destination="APZIPY",rpt=path,message=msg)
                
            elif(str(comment_arr[1])[:4] == "?VER"):
                if(debug):
                    print('odpowiadam na ?VER')
                msg_data = infopyVer + "," + get_sys()
                msg = ":" + znak + noop + ":" + msg_data
                ax25.send(source=callsign,destination="APZIPY",rpt=path,message=msg)    

            elif(str(comment_arr[1])[:5] == "?DATE"):   
                if(debug):
                    print('odpowiadam na ?DATE')
                now = datetime.datetime.now()             
                msg_data = now.strftime("%Y-%m-%d %H:%M:%S")
                msg = ":" + znak + noop + ":" + msg_data
                ax25.send(source=callsign,destination="APZIPY",rpt=path,message=msg)   

            else:
                if(debug):
                    print('odpowiadam na ?APRS')
                msg_data = "Not supported try: ?APRS"
                msg = ":" + znak + noop + ":" + msg_data
                ax25.send(source=callsign,destination="APZIPY",rpt=path,message=msg)            
            

def main():
    while True:
        time.sleep(1)

# let's dance
callsign = callsign.upper() #set to upper letters
ax25 = ax25lib(type="tcp",host=host,port=port,callback=dane)
main()