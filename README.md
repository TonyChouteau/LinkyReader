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

# Sources

You can find more information here : https://www.hleroy.com/2023/02/recuperer-la-teleinformation-linky-depuis-un-raspberry-pi-avec-python-influxdb-et-grafana/
