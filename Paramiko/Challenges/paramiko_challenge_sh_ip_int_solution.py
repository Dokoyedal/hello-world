import paramiko
import time

# creating an ssh client object
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('Connecting to 10.1.1.10')
ssh_client.connect(hostname='192.168.122.10', port='22', username='u1', password='cisco',
                   look_for_keys=False, allow_agent=False)


shell = ssh_client.invoke_shell()

shell.send('terminal length 0\n') ## needed to display the entire output at once
shell.send('show ip int brief\n')
time.sleep(1)

output = shell.recv(100000).decode()
print(output)


if ssh_client.get_transport().is_active():
    print('Closing connection')
    ssh_client.close()