# Bibliotheque lié à l'envoie et la structure de donnée

from influxdb import InfluxDBClient
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Gestion de la reception de donnée et traitement
import serial
import struct

import binascii

# permettant de hash le mot de passe de la premiere verification
import blake3

# Mise en place de la connexion Série
ser = serial.Serial('/dev/serial0', 9600)

#Mise en place de la connexion à InfluxDB
URL = "http://<ip>:8086"
USER = ''
PASS = ''
ORG = ''
BUCKET = 's'

# requete pour etablir la liaison
client = influxdb_client.InfluxDBClient(url=URL, username=USER, password=PASS)

# creation du hash
mdp = input("Entrez une valeur : ")
mdp_hash = blake3.blake3(mdp.encode()).hexdigest()

# Initialisation du nombres de tentative
tentative = 5
"""Programme pour le traitement et l'envoie de donnée"""

while tentative != 0 :
    if mdp_hash == '9d1c4d2aae8dbdf4f90e47e129f3396e0c6ea8a27632a0504130bf26f4770fd8' : # le champ mdp doit recevoir P@ss.Word pour obtenir le hash 9d1c4d2aae8dbdf4f90e47e129f3396e0c6ea8a27632a0504130bf26f4770fd8
        while True:
            line = ser.readline()

            #Si line vide continue le programme quand meme
            if not line:
                continue

            #Si la ligne commence par 'Te'
            if line.startswith(b'Te'):
                data = line[2:]

                # Données incomplètes, passer à la prochaine itération
                if len(data) < 17:
                    continue

                else :
                    #Récupération des données respectives
                    data_sans_checksum = line[2:15]
                    temp = struct.unpack('f', data[0:4])[0]
                    hum = struct.unpack('f', data[4:8])[0]
                    pression = struct.unpack('f', data[8:12])[0]
                    tor = struct.unpack('?', data[12:13])[0]
                    checksum = struct.unpack('i', data[13:17])[0]
                    
                    # XOR entre l'inversion et la valeur initiale de data_sans_checksum
                    xor = 0
                    
                    for byte in data_sans_checksum:
                        xor ^= byte
                    verif_checksum = xor ^ 0x55555555

                    # si checksum valide, envoyer requete
                    if verif_checksum == checksum :
                        write_api = client.write_api(write_options=SYNCHRONOUS)
                        query = f"""
                            pressure,sensor=bmp280,type=sensor value={pression}
                            temperature,sensor=280,type=sensor value={temp}
                            humidite,sensor=htu21df,type=sensor value={pression}
                            tor,sensor=lever,type=sensor value={tor}
                            """
                        write_api.write(BUCKET, ORG, query)
                        print("Données envoyées à InfluxDB")
    else :
        #gestion nombres de tentatives
        tentative -= 1
        print('Mot de passe faux ! , plus que ',tentative,'tentatives')

        if tentative > 0 :
            champ_mdp=input('Entrer le mot de passe :')
