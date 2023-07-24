# How to

## run localy

just do 
`python3 eaton_srv.py`

if this works, you can update the code as you need
then build you own docker image

## bulid your own docker
run
`docker build -t eaton_srv . `

then
`docker-compose up -d`

## how to use

first edit ./data/parameters.py do your SHC credentials

then you can switch an actor with

http://your-ip:9997/actor?actor=ID&set=COMMAND

http://your-ip:9997/actor?actor=ID&set=COMMAND&hz=HOMEZONE

eg:
http://192.168.0.95:9997/actor?actor=xCo:2902174_u0&set=off

COMMANDS depending on device : 

states=["on","off","toggle","stepOpen","stepClose","open", "close", "stop","directSetLock","directReleaseLock","directSwitchOn","directSwitchOff"]

with eg:
http://192.168.0.95:9997/list?

you get a list of your devices

## here a feature to send multiple commands 

edit this output and replace actors.json

(see example_actors.json)

then it would be possible to do something like this
send a command to all devices with ( see actors.json)

set=   "type"  "zone"  "floor"  "group"  "room"

value=  eg "Keller"

command= eg "on"


http://192.168.0.95:9997/set?set=floor&Keller=off


try it, but not everything yet full implemented
