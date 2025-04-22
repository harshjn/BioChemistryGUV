from datetime import datetime
import serial
import time
import tkinter as tk
from tkinter import ttk

filename = 'E:/Harsh/Harsh/April25/today/control_data1.txt'

# Configure the serial connection
ser = serial.Serial(
    port='COM7',
    baudrate=115200,
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

# Initialize serial communication
send_command('VER')
send_command('echo on')
time.sleep(1)
send_command('rsave off')

# Flag to track if an operation is in progress
operation_in_progress = False

# Function to handle withdrawing - non-blocking version
def withdraw(volume, speed, filename=filename):
    global operation_in_progress
    if operation_in_progress:
        return  # Don't start another operation if one is already running
    
    operation_in_progress = True
    wrateNum = speed
    
    # Update status display
    status_var.set("Status: Withdrawing...")
    operation_progress_var.set(f"Progress: 0/{volume} μl")
    progress_bar["maximum"] = float(volume)
    progress_bar["value"] = 0
    
    # Initial setup
    send_command(f'wrate a {wrateNum} ul/min')
    send_command('cvolume a')
    send_command(f'tvolume a {volume} ul')
    print(f'target volume set as {volume} ul')
    send_command('wrun a')
    
    # Schedule the first check
    check_withdraw_progress(volume)

# Function to periodically check withdraw progress
def check_withdraw_progress(target_volume):
    global operation_in_progress
    
    with open(filename, 'a') as file:
        # Send the command and get the response
        response = send_command('wvolume a')
        
        # Extract the volume from the response
        volume = "0"
        lines = response.split('\n')
        for line in lines:
            if 'A:' in line:
                volume = line.split(' ')[1]  # Extract the volume value
                current_volume = float(volume)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                print(f"{timestamp}, {volume}")
                file.write(f"{timestamp}, w{speed_var.get()}, {volume}\n")
                file.flush()
                
                # Update progress display
                operation_progress_var.set(f"Progress: {volume}/{target_volume} μl")
                progress_bar["value"] = current_volume
    
    # Check if we've reached the target volume
    if str(target_volume) == volume:
        operation_in_progress = False
        status_var.set("Status: Withdraw complete")
        print("Withdraw operation complete")
    else:
        # Schedule the next check
        window.after(100, lambda: check_withdraw_progress(target_volume))

# Function to handle infusing - non-blocking version
def infuse(volume, speed, filename=filename):
    global operation_in_progress
    if operation_in_progress:
        return  # Don't start another operation if one is already running
    
    operation_in_progress = True
    irateNum = speed
    
    # Update status display
    status_var.set("Status: Infusing...")
    operation_progress_var.set(f"Progress: 0/{volume} μl")
    progress_bar["maximum"] = float(volume)
    progress_bar["value"] = 0
    
    # Initial setup
    send_command(f'irate a {irateNum} ul/min')
    send_command('cvolume a')
    send_command(f'tvolume a {volume} ul')
    print(f'target volume set as {volume} ul')
    send_command('irun a')
    
    # Schedule the first check
    check_infuse_progress(volume)

# Function to periodically check infuse progress
def check_infuse_progress(target_volume):
    global operation_in_progress
    
    with open(filename, 'a') as file:
        # Send the command and get the response
        response = send_command('ivolume a')
        
        # Extract the volume from the response
        volume = "0"
        lines = response.split('\n')
        for line in lines:
            if 'A:' in line:
                volume = line.split(' ')[1]  # Extract the volume value
                current_volume = float(volume)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                print(f"moving forward {timestamp}, {volume} ul")
                file.write(f"{timestamp}, i{speed_var.get()}, {volume} \n")
                file.flush()
                
                # Update progress display
                operation_progress_var.set(f"Progress: {volume}/{target_volume} μl")
                progress_bar["value"] = current_volume
    
    # Check if we've reached the target volume
    if str(target_volume) == volume:
        operation_in_progress = False
        status_var.set("Status: Infuse complete")
        print("Infuse operation complete")
    else:
        # Schedule the next check
        window.after(100, lambda: check_infuse_progress(target_volume))

# Create the main window
window = tk.Tk()
window.title('Syringe Control')
window.geometry("300x500")  # Made window taller to accommodate new elements

# Speed input setup
speed_var = tk.IntVar(value=100)
speed_label = ttk.Label(window, text='Speed:')
speed_label.grid(row=0, column=0, padx=20, pady=20)
speed_entry = ttk.Entry(window, textvariable=speed_var, width=10)
speed_entry.grid(row=0, column=1, padx=20, pady=20)

# Volume input setup
volume_var = tk.IntVar(value=15)  # Default volume is 15
volume_label = ttk.Label(window, text='Volume (ul):')
volume_label.grid(row=1, column=0, padx=20, pady=20)
volume_entry = ttk.Entry(window, textvariable=volume_var, width=10)
volume_entry.grid(row=1, column=1, padx=20, pady=20)

# Forward button
forward_button = ttk.Button(window, text="infuse >>>>", 
                            command=lambda: infuse(volume_var.get(), speed_var.get()))
forward_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

# Backward button
backward_button = ttk.Button(window, text="withdraw <<<<", 
                             command=lambda: withdraw(volume_var.get(), speed_var.get()))
backward_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

# Add status display
status_var = tk.StringVar(value="Status: Ready")
status_label = ttk.Label(window, textvariable=status_var, font=("Arial", 10, "bold"))
status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Add operation progress display
operation_progress_var = tk.StringVar(value="Progress: 0/0 μl")
operation_progress_label = ttk.Label(window, textvariable=operation_progress_var)
operation_progress_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Add progress bar
progress_bar = ttk.Progressbar(window, orient="horizontal", length=250, mode="determinate")
progress_bar.grid(row=6, column=0, columnspan=2, padx=20, pady=10)

# StringVars to dynamically display mean and standard deviation voltage
mean_voltage_var = tk.StringVar(value="Mean Voltage: Loading...")
std_voltage_var = tk.StringVar(value="Std Voltage: Loading...")

# Labels to display mean and standard deviation voltage
mean_voltage_label = ttk.Label(window, textvariable=mean_voltage_var)
mean_voltage_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

std_voltage_label = ttk.Label(window, textvariable=std_voltage_var)
std_voltage_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Function to read voltage data from file and update the display
def load_voltage_data():
    try:
        with open('E:/Harsh/Harsh/April25/today/DisplayVoltsData.txt', 'r') as file:
            lines = file.readlines()
            meanVoltage = float(lines[0].strip())
            stdVoltage = float(lines[1].strip())

            # Update the display if values have changed
            mean_voltage_var.set(f"Mean Voltage: {meanVoltage:.4f}")
            std_voltage_var.set(f"Std Voltage: {stdVoltage:.4f}")

    except (IndexError, ValueError, FileNotFoundError) as e:
        mean_voltage_var.set("Mean Voltage: Error")
        std_voltage_var.set("Std Voltage: Error")
        print("Error loading voltage data:", e)

    # Schedule the function to run again after 0.1 second
    window.after(100, load_voltage_data)

# Function to close the serial port when the window is closed
def on_closing():
    ser.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the periodic data loading
load_voltage_data()

window.mainloop()