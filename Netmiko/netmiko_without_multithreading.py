from netmiko import ConnectHandler

import time
start = time.time()

with open('devices.txt') as f:
    devices = f.read().splitlines()

for ip in devices:

    cisco_device = {
           'device_type': 'cisco_ios',
           'host': ip,
           'username': 'u1',
           'password': 'cisco',
           'port': 22,             # optional, default 22
           'secret': 'cisco',      # this is the enable password
           'verbose': True         # optional, default False
           }
    connection = ConnectHandler(**cisco_device)
    print('Entering the enable mode...')
    connection.enable()

    output = connection.send_command('show run')
    # print(output)
    prompt = connection.find_prompt()
    hostname = prompt[0:-1]
    # print(hostname)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day


    filename = f'{hostname}_{year}-{month}-{day}_backup.txt'
    with open(filename, 'w') as backup:
        backup.write(output)
        print(f'Backup of {hostname} completed successfully')
        print('#' * 30)


    print('Closing connection')
    connection.disconnect()

end = time.time()
print(f'Total execution time:{end-start}')