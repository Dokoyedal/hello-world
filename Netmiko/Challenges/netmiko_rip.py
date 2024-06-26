from netmiko import ConnectHandler

cisco_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.122.10',
    'username': 'u1',
    'password': 'cisco',
    'port': 22,
    'secret': 'cisco',
    'verbose': True
}

connection = ConnectHandler(**cisco_device)

print('Entering the enable mode ...')
connection.enable()

print('Sending commands from file ...')
output = connection.send_config_from_file('rip.txt')
print(output)


print(f'Disconnecting from {cisco_device["host"]}')
connection.disconnect()