import serial
import time

# Configure the serial port (ensure it matches your setup)
ser = serial.Serial('/dev/ttyAMA0', 1200, timeout=1)
ser.bytesize = 7       # Set the data bits to 7
ser.parity   = serial.PARITY_EVEN  # Set even parity
ser.stopbits = serial.STOPBITS_ONE # Set stop bits to 1

# Log file where the TIC data will be saved
log_file = '/home/pi/tic_data.log'

# Open the log file for appending data
with open(log_file, 'a') as log:
    while True:
        # Read a line of data from the serial port
        data = ser.readline()

        # If data is received, log it
        if data:
            data_decoded = data.decode('ascii', errors='ignore')
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            log_entry = f"{timestamp} - {data_decoded}"
            log.write(log_entry)

            # Print to console as well
            print(log_entry)

        # Sleep to prevent high CPU usage
        time.sleep(1)
