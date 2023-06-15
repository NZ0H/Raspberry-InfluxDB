# Raspberry-InfluxDB

## En Français :
Le programme récupère les données envoyées sur une liaison série (avec une carte Arduino). Il vérifie que la trame commence par "Te" pour être sûr que c'est bien la trame des capteurs qu'il reçoit. Après cela, il décompose la trame en récupérant les valeurs respectives qui sont placées dans des variables. Il vérifie le checksum en le recalculant de la même manière que dans le programme Arduino (XOR avec les bits de rang pair inversés). Si le checksum est bon, il envoie la requête au serveur InfluxDB sur la base de données choisie avec les noms de colonnes correspondants.

## In English :

The program retrieves data sent over a serial connection (using an Arduino board). It checks that the frame starts with "Te" to ensure that it is indeed the sensor frame being received. After that, it decomposes the frame by retrieving the respective values, which are stored in variables. It verifies the checksum by recalculating it in the same way as in the Arduino program (XOR with the inverted even-position bits). If the checksum is correct, it sends the request to the InfluxDB server on the chosen database with the corresponding column names.
