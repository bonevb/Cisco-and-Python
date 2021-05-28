#The script will check if ip address behind b2bftp.apple.com is changed and
#if it is it will add the new address in cisco asa objec-group

import socket
import filecmp
import os
import sqlite3


DB_NAME = 'ip.db'
db = sqlite3.connect(DB_NAME)
c = db.cursor()


def check_dns():
    host = 'b2bftp.apple.com'
    result =  socket.gethostbyname(host)
    return result

ip = check_dns()
print(ip)

def check_ip(ip):
    c.execute('SELECT  *  FROM IP WHERE ADDR = ?', (ip,))
    try:
        for i in c.fetchone():
            return i
    except:
        return None


def save_to_db(ip):
    c.execute('INSERT INTO IP VALUES(?)', (ip,))
    db.commit()
    print(ip + 'saved')

#print('the ip address is: ', check_ip(ip))

if check_ip(ip) is None:
    #print('ip is not into DB')
    save_to_db(ip)


    with open('dns', 'w') as file:
        line = ip
        file.write('network-object host '+ line)

    os.system('ansible-playbook lines_asa_apple.yaml')


