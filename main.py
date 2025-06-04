import network
import socket
from time import sleep
import machine
import rp2
import sys
import l76x
import MicropyGPS

ssid = "*******"
password = "******"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

connect()


UARTx = 0

BAUDRATE = 9600

gnss_l76b=l76x.L76X(uartx=UARTx,_baudrate = BAUDRATE)

gnss_l76b.l76x_exit_backup_mode()

gnss_l76b.l76x_send_command(gnss_l76b.SET_SYNC_PPS_NMEA_ON)

parser = MicropyGPS(location_formatting='dd')

sentence = ''

while True:
    if gnss_l76b.uart_any():
        sentence = parser.update(chr(gnss_l76b.uart_receive_byte()[0]))
        if sentence:
            
            print('WGS84 Coordinate:Latitude(%c),Longitude(%c) %.9f,%.9f'%(parser.latitude[1],parser.longitude[1],parser.latitude[0],parser.longitude[0]))
            print('copy WGS84 coordinates and paste it on Google map web https://www.google.com/maps')

            gnss_l76b.wgs84_to_bd09(parser.longitude[0],parser.latitude[0])
            print('Baidu Coordinate: longitude(%c),latitudes(%c) %.9f,%.9f'%(parser.longitude[1],parser.latitude[1],gnss_l76b.Lon_Baidu,gnss_l76b.Lat_Baidu))
            print('copy Baidu Coordinate and paste it on the baidu map web https://api.map.baidu.com/lbsapi/getpoint/index.html')
            
            print('UTC Timestamp:%d:%d:%d'%(parser.timestamp[0],parser.timestamp[1],parser.timestamp[2]))
            
            print('Fix Status:', parser.fix_stat)
            
            print('Altitude:%d m'%(parser.altitude))
            print('Height Above Geoid:', parser.geoid_height)
            print('Horizontal Dilution of Precision:', parser.hdop)
            print('Satellites in Use by Receiver:', parser.satellites_in_use)
            print('')


