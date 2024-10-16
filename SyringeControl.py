
# In this experiment, I can infuse water or glucose. 
# I can continuously vary the osmolarity at a slow speed and observe my vesicle. 
# Flows can be slow enough. If I start with 500 mOsm/l glucose buffer and initial concentration
# as 100 ul, then I can continuously vary it to 250 and eventually 62.5. 
# If I start with 100 ul, then final concentration should be 1000 ul or more. 
# After finishing this, I can withdraw. There's also the issue of upstream 
# diffusion that I need to prevent. 


# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:22:17 2024

@author: Leica-Admin
"""

from datetime import datetime
import serial
import time

import tkinter as tk
from tkinter import ttk
#%%

# Configure the serial connection
ser = serial.Serial(
    port='COM7',
    baudrate=115200,  # Adjust this to match your device's baud rate
    timeout=1
)

def send_command(command):
    # Send the command
    ser.write((command + '\r\n').encode())
    
    # Read the response
    response = ""
    while True:
        line = ser.readline().decode().strip()
        if line:
            response += line + "\n"
        else:
            # No more data received, assume response is complete
            break
    
    # Print the response
    print(f"Response for '{command}':")
    print(response)
    return response


send_command('VER')

# Send 'echo on' command
send_command('echo on')
time.sleep(1)

# Wait a bit between commands

# Send 'rsave off' command
send_command('rsave off')
#%%
filename='control_data_16Oct1.txt'
#%% Withdraw & write the data
#Withdraw

def withdraw(speed,filename=filename):
    Displacements=[15];#,20,20,10,10,10]
    wrateNum=speed;
    send_command(f'wrate a {wrateNum} ul/min')
    # send_command('wrate b')
    
    # send_command('wvolume b')
    
    # send_command('wvolume b')
    # send_command('tvolume b')
    # send_command('tvolume b')
    
    
    for disp in Displacements:
        send_command('cvolume a')
        send_command(f'tvolume a {disp} ul')
        print(f'target volume set as {disp} ul')
        send_command('wrun a')
    
        volume=0;
    
        while str(disp) != volume:
            with open(filename, 'a') as file:
                # Send the command and get the response
                response = send_command('wvolume a')
                
                # Extract the volume from the response
                lines = response.split('\n')
                for line in lines:
                    if 'A:' in line:
                        volume = line.split(' ')[1]  # Extract the volume value
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Current time up to milliseconds
                        print(f"{timestamp}, {volume}")  # Print to console
                        file.write(f"moving backward {timestamp}, w{wrateNum}, {volume}\n")  # Write to file
                        file.flush()  # Ensure data is written to file
                
#                time.sleep(0.01)  # Adjust this to your needs
 #       time.sleep(5)  # Adjust this to your needs
    
        #%% Infuse & write the data

def infuse(speed,filename=filename):
    Displacements=[15]
    
    #Infuse
    irateNum=speed;
    send_command(f'irate a {irateNum} ul/min')
    # send_command('irate b')
    
    # send_command('wvolume b')
    
    # send_command('wvolume b')
    # send_command('tvolume b')
    # send_command('tvolume b')
    
    
    for disp in Displacements:
        send_command('cvolume a')
        send_command(f'tvolume a {disp} ul')
        print(f'target volume set as {disp} ul')
        send_command('irun a')
    
        volume=0;
    
        while str(disp) != volume:
            with open(filename, 'a') as file:
                # Send the command and get the response
                response = send_command('ivolume a')
                
                # Extract the volume from the response
                lines=response.split('\n')
                for line in lines:
                    if 'A:' in line:
                        volume = line.split(' ')[1]  # Extract the volume value
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Current time up to milliseconds
                        print(f"moving forward {timestamp}, {volume} ul")  # Print to console
                        file.write(f"{timestamp}, i{irateNum}, {volume} \n")  # Write to file
                        file.flush()  # Ensure data is written to file
                
#            time.sleep(0.01)  # Adjust this to your needs
 #   time.sleep(5)  # Adjust this to your needs

#%%
window = tk.Tk()
window.title('Syringe Control')

speed_var = tk.IntVar(value=100)
speed_label= ttk.Label(window,text = 'Speed:')
speed_label.grid(row=0,column=0,padx = 5, pady = 5)
speed_entry = ttk.Entry(window,textvariable=speed_var,width=5)
speed_entry.grid(row=0,column=1,padx=5,pady=5)

#forward button
forward_button = ttk.Button(window,text=">>>>",command = lambda: infuse(speed_var.get()))
forward_button.grid(row=1,column =0, columnspan =2, padx=5,pady=5)

#backward button
backward_button = ttk.Button(window,text="<<<<",command = lambda: withdraw(speed_var.get()))
backward_button.grid(row=2,column =0, columnspan =2, padx=5,pady=5)



window.mainloop()






#%%
ser.close()  # Close the serial connection
