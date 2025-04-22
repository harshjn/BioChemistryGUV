# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:12:11 2024

@author: Leica-Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:25:26 2024

@author: Leica-Admin
"""
import nidaqmx
from nidaqmx.system import System
from datetime import datetime,timedelta
# import serial
import time
import numpy as np

# Initialize the system to get the list of devices
system = System.local()

# List all connected devices
print("Available NI-DAQmx devices:")
for device in system.devices:
    print(f"Device Name: {device.name}, Product Type: {device.product_type}")

filename='E:/Harsh/Harsh/April25/today/analog_data1.txt'


#%%
import nidaqmx
from nidaqmx.constants import TerminalConfiguration
device_name = 'Dev1'
channel_name = f"{device_name}/ai0"
samples_to_read = 1000  # Number of samples you want to read
sample_rate = 10000     # Samples per second

import time
start_time = datetime.now()

with nidaqmx.Task() as task:
    # Add an analog input channel (this part stays the same)
    task.ai_channels.add_ai_voltage_chan(
        channel_name,
        terminal_config=TerminalConfiguration.RSE,
        min_val=-10.0,
        max_val=10.0
    )
    
    # NEW: Configure timing to read multiple samples
    task.timing.cfg_samp_clk_timing(rate=sample_rate, 
                                   samps_per_chan=samples_to_read)
    timestart = time.time()
    
    # Read multiple samples at once
    values = task.read(number_of_samples_per_channel=samples_to_read)
    
    # Print the results
   
    
    # Process and write each sample in the buffer
    for i, voltage in enumerate(values):
        # Calculate timestamp for each sample
        sample_timestamp = start_time + timedelta(seconds=i * (1.0 / sample_rate));
        
        # Format data
        data_line = f"{sample_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}, {voltage:.5f}\n"
        
        # Write to file and console
        print(data_line, end='\r')
   
    print(f"--- %s seconds ---",(time.time() - timestart))

#%%

# file.write("Timestamp, Raw Value, Voltage\n")  # Write header
device_name = 'Dev1'
channel_name = f"{device_name}/ai0"
samples_to_read = 1000  # Number of samples you want to read
sample_rate = 10000     # Samples per second

with open(filename, 'a') as file:
    try: 
        while True:
            start_time = datetime.now()
            timestart = time.time()
        
            with nidaqmx.Task() as task:
                # Add an analog input channel (this part stays the same)
                task.ai_channels.add_ai_voltage_chan(
                    channel_name,
                    terminal_config=TerminalConfiguration.RSE,
                    min_val=-10.0,
                    max_val=10.0
                )
            
                task.timing.cfg_samp_clk_timing(rate=sample_rate, 
                                           samps_per_chan=samples_to_read)
            
            
            # Read multiple samples at once
                values = task.read(number_of_samples_per_channel=samples_to_read)
            
                # Print the results
            
                # Process and write each sample in the buffer
                for i, voltage in enumerate(values):
                    # Calculate timestamp for each sample
                    sample_timestamp = start_time + timedelta(seconds=i * (1.0 / sample_rate));
                    
                    # Format data
                    data_line = f"{sample_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}, {voltage:.5f}\n"
            
                    #print(data_with_timestamp)  # Print to console
                    file.write(data_line)  # Write to file
                    file.flush()  # Ensure data is written to file
                    
                    
            with open('E:/Harsh/Harsh/April25/today/DisplayVoltsData.txt', 'w') as file2:
                meanVal = np.mean(values);
                stdVal = np.std(values);
                file2.write(f"{meanVal}\n{stdVal}")
                file2.flush()
            print(f"--- %s seconds ---" % (time.time() - timestart))
            print(f"mean is {meanVal:.5f} & std is {stdVal:.5f}")

    except KeyboardInterrupt:
        print("Data collection stopped by user")
    