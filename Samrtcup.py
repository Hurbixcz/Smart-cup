import threading      
from tkinter import *
import tkinter as tk
import serial
import serial.tools.list_ports
import time
from datetime import datetime
import requests

temp = 0
value= 0

api_key = "NIU01Z86I7887S1S"

ports = serial.tools.list_ports.comports()

arduino_ports = [port.device for port in ports if 'USB-SERIAL' in port.description] #kontrola zda je zařízení zapojeno
if len(arduino_ports)>0:
    message_print = arduino_ports[0]
else:
    exit()


def validate_enetry(number):
    if not number:
        return True
    try:
        number = int(number)
        pass
    except VauleError:
        return False
    return number <= 70  and number >= 10 #vymezení hodnot




port = arduino_ports[0]
ser = serial.Serial(port, 115200,timeout=3)
root = Tk()
validate_cmd = root.register(validate_enetry)
root.title("SmartCup")
root.resizable(False, False)
panel = Entry(root, width=35, borderwidth=5,validate="key", validatecommand=(validate_cmd,"%P"))
panel.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
panel.insert(0,value)

def task():
    while True:  
        global urlt
        global ser
        try:  
            ser.reset_output_buffer()
            ser.write(("write;").encode('utf-8'))
            time.sleep(0.1)
            if(ser.in_waiting > 0):
                temp = ser.read_until('a')
                temp = temp.decode('utf-8')
                temp = temp.replace('a', '')
                url = f"https://api.thingspeak.com/update?api_key={api_key}&field1={temp}&field2={value}"
                response = requests.get(url)
            time.sleep(60)
        except:
            print("chyba")
t = threading.Thread(target=task)
t.start()




def button_click(number): #funkce pro zvyšování a snižování teploty
        global value
        cache=int(number)
        value=(value + cache)
        if value > 70:
            value = 70
        if value < 10:
            value = 10
        panel.delete(0, END)
        panel.insert(0,value)

def button_reset(): #funkce na reset panelu
    global value
    value = 10
    panel.delete(0, END)
    panel.insert(0,value)



def button_send(): #funkce pro odeslání hodnot
    global value
    global port
    ser.write(("set "+str(value)+";").encode('utf-8'))
    url = f"https://api.thingspeak.com/update?api_key={api_key}&field1={temp}&field2={value}"
    response = requests.get(url)





 
button_1 = tk.Button(root, text="+1", padx= 40, pady= 20, command=lambda:button_click(1)) #teplota +1
button_2 = tk.Button(root, text="+10", padx= 40, pady= 20, command=lambda:button_click(10))#teplota +10
button_3 = tk.Button(root, text="-1", padx= 40, pady= 20, command=lambda:button_click(-1))#teplota -1
button_4 = tk.Button(root, text="-10", padx= 40, pady= 20, command=lambda:button_click(-10))#teplota -10
button_Send = tk.Button(root, text="Send", padx= 79, pady= 20, command=lambda:button_send())#teplota odeslat
button_Reset = tk.Button(root, text="Reset", padx= 40, pady= 20, command=lambda:button_reset())#teplota reset

#velikost a umístění tlačítek
button_1.grid(row=1, column=0)
button_2.grid(row=1, column=1)
button_Reset.grid(row=1, column=2)
button_3.grid(row=1, column=3)
button_4.grid(row=1, column=4)

button_Send.grid(row=3, column=1, columnspan=3)


 

root.mainloop()

