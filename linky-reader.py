import serial
import time
from datetime import datetime
import psycopg2
from datetime import datetime

# Connect to your PostgreSQL database
with open("db_login.txt") as f:
    lines = f.readlines()
    conn = psycopg2.connect(
        dbname=lines[0].replace("\n", ""),    # Replace with your database name
        user=lines[1].replace("\n", ""),      # Replace with your username
        password=lines[2].replace("\n", ""),  # Replace with your password
        host=lines[3].replace("\n", ""),      # Replace with your host, if different
        port=lines[4].replace("\n", "")       # Replace with your PostgreSQL port, if different
    )

# Configure the serial port (ensure it matches your setup)
ser = serial.Serial('/dev/ttyAMA0', 1200, timeout=1)
ser.bytesize = 7       # Set the data bits to 7
ser.parity = serial.PARITY_EVEN  # Set even parity
ser.stopbits = serial.STOPBITS_ONE  # Set stop bits to 1

# Log file where the TIC data will be saved
log_file = '/home/pi/tic_data.log'

linky_code = {
    "ADCO": {
        "name": "Identifiant du compteur",
        "format": lambda data: data.split(" ")[1]
    },  # The meter's address (a unique identifier for the meter)
    "OPTARIF": {
        "name": "Option tarifaire choisie",
        "format": lambda data: data.split(" ")[1]
    },  # The selected tariff option (e.g., HC/HP, EJP, Tempo)
    "ISOUSC": {
        "name": "Intensité souscrite",
        "format": lambda data: data.split(" ")[1]
    },  # The subscribed intensity (maximum power limit)
    # "BASE": "Index option Base",        # The base consumption index (for standard tariff)
    "HCHC": {
        "name": "Index Heures Creuses",
        "format": lambda data: data.split(" ")[1]
    },   # The consumption index for off-peak hours (Heures Creuses)
    "HCHP": {
        "name": "Index Heures Pleines",
        "format": lambda data: data.split(" ")[1]
    },  # The consumption index for peak hours (Heures Pleines)
    # "EJPHN": "Index option EJP Heures Normales",     # The index for EJP normal hours
    # "EJPHPM": "Index option EJP Heures de Pointe Mobile",    # The index for EJP peak mobile hours
    # "BBRHCJB": "Index option Tempo Heures Creuses Jours Bleus",  # Tempo blue days off-peak index
    # "BBRHPJB": "Index option Tempo Heures Pleines Jours Bleus",  # Tempo blue days peak index
    # "BBRHCJW": "Index option Tempo Heures Creuses Jours Blancs",  # Tempo white days off-peak index
    # "BBRHPJW": "Index option Tempo Heures Pleines Jours Blancs",  # Tempo white days peak index
    # "BBRHCJR": "Index option Tempo Heures Creuses Jours Rouges",  # Tempo red days off-peak index
    # "BBRHPJR": "Index option Tempo Heures Pleines Jours Rouges",  # Tempo red days peak index
    # "PEJP": "Préavis Début EJP",      # Notification for the beginning of the EJP (Electricité Jour de Pointe) period
    "PTEC": {
        "name": "Période Tarifaire en cours",
        "format": lambda data: data.split(" ")[1]
    },  # The current active tariff period (e.g., full hours or part of it)
    # "DEMAIN": "Couleur du lendemain",  # Color of the next day (for the Tempo tariff, indicating the next day’s type)
    "IINST": {
        "name": "Intensité Instantanée",
        "format": lambda data: data.split(" ")[1]
    },  # The instantaneous intensity (current power usage)
    # "ADPS": "Avertissement de Dépassement De Puissance Souscrite",  # Warning for exceeding the subscribed power limit
    "IMAX": {
        "name": "Intensité maximale appelée",
        "format": lambda data: data.split(" ")[1]
    },  # The maximum intensity (current highest power demand)
    "PAPP": {
        "name": "Puissance apparente",
        "format": lambda data: data.split(" ")[1]
    },  # Apparent power (combination of active and reactive power)
    "HHPHC": {
        "name": "Horaire Heures Pleines Heures Creuses",
        "format": lambda data: data.split(" ")[1]
    },  # The time schedule for peak and off-peak hours
    "MOTDETAT": {
        "name": "Mot d'état du compteur",
        "format": lambda data: data.split(" ")[1]
    }   # Meter status message (e.g., normal operation or fault)
}

values = []

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
            value = None
            key = None
            for _key in linky_code:
                if _key in data_decoded:
                    tag_found += 1
                    key = _key
                    tag = linky_code[key]["name"]
                    value = linky_code[key]["format"](data_decoded)
            if tag is None:
                tag = "N/A"
                value = None
                key = None

            if key == "ADCO" and len(values) == 22:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO linky_data (
                        ADCO, ADCO_timestamp,
                        OPTARIF, OPTARIF_timestamp,
                        ISOUSC, ISOUSC_timestamp,
                        HCHC, HCHC_timestamp,
                        HCHP, HCHP_timestamp,
                        PTEC, PTEC_timestamp,
                        IINST, IINST_timestamp,
                        IMAX, IMAX_timestamp,
                        PAPP, PAPP_timestamp,
                        HHPHC, HHPHC_timestamp,
                        MOTDETAT, MOTDETAT_timestamp
                    ) 
                    VALUES (
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s
                    );
                """

                # Execute the query with the provided values
                cur.execute(insert_query, values)

                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cur.close()
                # conn.close()

                values = []
            else:
                values = []

            values.append(value)
            values.append(datetime.now())

            log_entry = f"[{len(values)}] {tag} : {value} | {timestamp} - {data_decoded}"
            log.write(log_entry)

            # Print to console as well
            print(log_entry)

        # Sleep to prevent high CPU usage
        time.sleep(1)
