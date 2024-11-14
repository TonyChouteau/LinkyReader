# LinkyReader
Read the linky log with a RaspberryPi3B and the PTInfo module

# Connection

Linky I1 & I2 must be connected to the PtInfo module. The PtInfo module must be connected to the GPIO pin of the RaspberryPi3B.

# Configuration

Open the config file : `sudo nano /boot/config.txt`. \
Add the following line in the file : `dtoverlay=disable-bt`. \
Reboot the RaspberryPi : `sudo reboot`. \

Configure the RaspberryPi : `sudo raspi-config`
- Go to Interfacing Options → Serial.
- Set the Serial Login Shell to No and ensure that Serial Port Hardware is set to Yes.
- Save and reboot the Raspberry Pi.

# Run the python script

`python3 /path/to/LinkyReader/linky-reader.py`

# Logging

- ADCO : Identifiant du compteur

L'adresse d'identification du concentrateur (Groupe "ADCO") est codée sur 12 caractères
numériques.

- OPTARIF : Option tarifaire (type d’abonnement)

BASE => Option Base.
HC.. => Option Heures Creuses.
EJP. => Option EJP.

- ISOUSC : Intensité souscrite
- BASE : Index si option = base (en Wh)

Si Heures creuses :
- HCHC : Index heures creuses si option = heures creuses (en Wh)
- HCHP : Index heures pleines si option = heures creuses (en Wh)

Si EJP
- EJP HN : Index heures normales si option = EJP (en Wh)
- EJP HPM : Index heures de pointe mobile si option = EJP (en Wh)
- PEJP : Préavis EJP si option = EJP 30mn avant période EJP

Si Tempo
- BBR HC JB : Index heures creuses jours bleus si option = tempo (en Wh)
- BBR HP JB : Index heures pleines jours bleus si option = tempo (en Wh)
- BBR HC JW : Index heures creuses jours blancs si option = tempo (en Wh)
- BBR HC JW : Index heures pleines jours blancs si option = tempo (en Wh)
- BBR HC JR : Index heures creuses jours rouges si option = tempo  (en Wh)
- BBR HP JR : Index heures pleines jours rouges si option = tempo (en Wh)
- DEMAIN : Couleur du lendemain si option = tempo

- PTEC : Période tarifaire en cours

TH.. => Toutes les Heures.
HC.. => Heures Creuses.
HP.. => Heures Pleines.
HN.. => Heures Normales.
PM.. => Heures de Pointe Mobile

- IINST : Intensité instantanée (en ampères)
- ADPS : Avertissement de dépassement de puissance souscrite (en ampères)
- IMAX : Intensité maximale (en ampères)
- PAPP : Puissance apparente (en Volt.ampères)
- HHPHC : Groupe horaire si option = heures creuses ou tempo
- MOTDETAT : Mot d’état (autocontrôle)

# Sources

Récupérer la téléinformation Linky depuis un Raspberry Pi avec Python, InfluxDB et Grafana : https://www.hleroy.com/2023/02/recuperer-la-teleinformation-linky-depuis-un-raspberry-pi-avec-python-influxdb-et-grafana/
Téléinfo EDF – Suivi conso de votre compteur électrique (màj 08/2016) : https://www.magdiblog.fr/gpio/teleinfo-edf-suivi-conso-de-votre-compteur-electrique/