import serial
import time

# Configure the serial port (ensure it matches your setup)
ser = serial.Serial('/dev/ttyAMA0', 1200, timeout=1)
ser.bytesize = 7       # Set the data bits to 7
ser.parity   = serial.PARITY_EVEN  # Set even parity
ser.stopbits = serial.STOPBITS_ONE # Set stop bits to 1

# Log file where the TIC data will be saved
log_file = '/home/pi/tic_data.log'

linky_code = {
    "ADCO": "Adresse du compteur",      # The meter's address (a unique identifier for the meter)
    "OPTARIF": "Option tarifaire choisie",   # The selected tariff option (e.g., HC/HP, EJP, Tempo)
    "ISOUSC": "Intensité souscrite",    # The subscribed intensity (maximum power limit)
    "BASE": "Index option Base",        # The base consumption index (for standard tariff)
    "HCHC": "Index Heures Creuses",     # The consumption index for off-peak hours (Heures Creuses)
    "HCHP": "Index Heures Pleines",     # The consumption index for peak hours (Heures Pleines)
    "EJPHN": "Index option EJP Heures Normales",     # The index for EJP normal hours
    "EJPHPM": "Index option EJP Heures de Pointe Mobile",    # The index for EJP peak mobile hours
    "BBRHCJB": "Index option Tempo Heures Creuses Jours Bleus",  # Tempo blue days off-peak index
    "BBRHPJB": "Index option Tempo Heures Pleines Jours Bleus",  # Tempo blue days peak index
    "BBRHCJW": "Index option Tempo Heures Creuses Jours Blancs",  # Tempo white days off-peak index
    "BBRHPJW": "Index option Tempo Heures Pleines Jours Blancs",  # Tempo white days peak index
    "BBRHCJR": "Index option Tempo Heures Creuses Jours Rouges",  # Tempo red days off-peak index
    "BBRHPJR": "Index option Tempo Heures Pleines Jours Rouges",  # Tempo red days peak index
    "PEJP": "Préavis Début EJP",      # Notification for the beginning of the EJP (Electricité Jour de Pointe) period
    "PTEC": "Période Tarifaire en cours",      # The current active tariff period (e.g., full hours or part of it)
    "DEMAIN": "Couleur du lendemain",    # Color of the next day (for the Tempo tariff, indicating the next day’s type)
    "IINST": "Intensité Instantanée",     # The instantaneous intensity (current power usage)
    "ADPS": "Avertissement de Dépassement De Puissance Souscrite",  # Warning for exceeding the subscribed power limit
    "IMAX": "Intensité maximale appelée",      # The maximum intensity (current highest power demand)
    "PAPP": "Puissance apparente",      # Apparent power (combination of active and reactive power)
    "HHPHC": "Horaire Heures Pleines Heures Creuses",     # The time schedule for peak and off-peak hours
    "MOTDETAT": "Mot d'état du compteur"   # Meter status message (e.g., normal operation or fault)
}


# Open the log file for appending data
with open(log_file, 'a') as log:
    while True:
        # Read a line of data from the serial port
        data = ser.readline()

        # If data is received, log it
        if data:
            data_decoded = data.decode('ascii', errors='ignore').replace('\n', '')
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            tag_found = 0
            tag = None
            for key in linky_code:
                if key in data_decoded:
                    tag_found += 1
                    tag = linky_code[key]
            if tag is None:
                tag = "N/A"
            log_entry = f"{timestamp} - {data_decoded} # [{tag_found}] {tag}"
            log.write(log_entry)

            # Print to console as well
            print(log_entry)

        # Sleep to prevent high CPU usage
        time.sleep(1)
