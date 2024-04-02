from netmiko import ConnectHandler
linux = {
       'device_type': 'linux',
       'host': '192.168.0.50',
       'username': 'u1',
       'password': 'pass123',
       'port': 22,             # optional, default 22
       'secret': 'pass123',     # this is the sudo password
       'verbose': True         # optional, default False
       }
connection = ConnectHandler(**linux)

# becoming root
connection.enable() # sudo su

output = connection.send_command('apt update && apt install -y apache2')

print('Closing connection')
connection.disconnect()