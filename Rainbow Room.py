import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from time import sleep
import threading


"""

-------------------------------------------------------------------------------------------

"""


# header

SPEECH_OUT = 1314
SPEECH_IN = "1446"     # don't forget the ""
MODIFY_FURNI = 2880
CLEAR_ID = 1752

# commands

HELP_COMMAND = ":rhelp"
SET_DELAI = ":r "      # don't forget the space
START_COMMAND = ":r on"
DISABLE_COMMAND = ":r off"
SET_ID = ":rset"


"""

-------------------------------------------------------------------------------------------

"""


extension_info = {
    "title": "Rainbow Background",
    "description": "`"+HELP_COMMAND+"`",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


cd = 0.2
on = False
idd = ""
set_id = False


def speech(message):
    (text, color, index) = message.packet.read('sii')
    global cd
    global on
    global idd
    global set_id

    if text == SET_ID:
        message.is_blocked = True
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Modify the background to save the id"}{i:0}{i:1}{i:0}{i:0}')
        set_id = True
        return

    if text == HELP_COMMAND:
        message.is_blocked = True
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"`'+SET_ID+'` and save the background to save the id"}{i:0}{i:1}{i:0}{i:0}')
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"`'+START_COMMAND+'` turn on / `'+DISABLE_COMMAND+'` turn off"}{i:0}{i:1}{i:0}{i:0}')
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"`'+SET_DELAI+' <num>` set the interval"}{i:0}{i:1}{i:0}{i:0}')
        return

    if text == START_COMMAND:
        message.is_blocked = True
        if idd:
            on = True
            thread = threading.Thread(target=main)
            thread.start()
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Rainbow on !"}{i:0}{i:1}{i:0}{i:0}')
        else:
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Pls use `'+SET_ID+'`"}{i:0}{i:1}{i:0}{i:0}')
        return

    if text == DISABLE_COMMAND:
        message.is_blocked = True
        on = False
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Rainbow off !"}{i:0}{i:1}{i:0}{i:0}')
        return

    elif text.startswith(SET_DELAI):
        message.is_blocked = True
        try:
            arg = float(text[(len(SET_DELAI)):])
            cd = arg
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Interval set to: '+str(arg)+'"}{i:0}{i:1}{i:0}{i:0}')
        except:
            ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Only number available"}{i:0}{i:1}{i:0}{i:0}')


def main():
    global cd
    global idd
    while on:
        for i in range(256):
            if on:
                ext.send_to_server('{l}{h:'+str(MODIFY_FURNI)+'}{i:'+str(idd)+'}{i:'+str(i)+'}{i:128}{i:128}')
                sleep(cd)


def save_id(message):
    global idd
    global set_id
    if set_id:
        (furni_id, _, _, _) = message.packet.read("iiii")
        idd = str(furni_id)
        ext.send_to_client('{l}{h:'+SPEECH_IN+'}{i:0}{s:"Id save ( '+idd+' )"}{i:0}{i:1}{i:0}{i:0}')
        set_id = False


def clear(message):
    global idd
    global on
    on = False
    idd = ""


ext.intercept(Direction.TO_SERVER, speech, SPEECH_OUT)
ext.intercept(Direction.TO_SERVER, save_id, MODIFY_FURNI)
ext.intercept(Direction.TO_SERVER, clear, CLEAR_ID)
