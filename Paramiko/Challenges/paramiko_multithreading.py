import paramiko
import time
import threading

def connect(server_ip, server_port, user, passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {server_ip}')
    ssh_client.connect(hostname=server_ip, port=server_port, username=user, password=passwd,
                       look_for_keys=False, allow_agent=False)
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command, timout=1):
    print(f'Sending command: {command}')
    shell.send(command + '\n')
    time.sleep(timout)


### SOLUTION ###
def send_from_file(shell, file_name):
    with open(file_name) as f:
        commands = f.read().splitlines()

    for cmd in commands:
        send_command(shell, cmd)


def show(shell, n=10000):
    output = shell.recv(n)
    return output.decode()

def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        print('Closing connection')
        ssh_client.close()

## SOLUTION
# this function will get executed by each thread
def target_function(router):
    ssh_client = connect(server_ip=router['server_ip'], server_port=router['server_port'], user=router['user'],
                             passwd=router['passwd'])

    shell = get_shell(ssh_client)
    send_from_file(shell, router['config'])
    output = show(shell)
    print(output)

if __name__ == '__main__':
    router1 = {'server_ip': '192.168.122.10', 'server_port': '22', 'user':'u1', 'passwd':'cisco', 'config':'ospf.txt'}
    router2 = {'server_ip': '192.168.122.20', 'server_port': '22', 'user': 'u1', 'passwd': 'cisco', 'config':'eigrp.txt'}
    router3 = {'server_ip': '192.168.122.30', 'server_port': '22', 'user': 'u1', 'passwd': 'cisco', 'config':'router3.conf'}

    devices = [router1, router2, router3]

    my_threads = list()
    for router in devices:
        th = threading.Thread(target=target_function, args=(router,))
        my_threads.append(th)

    for th in my_threads:
        th.start()

    for th in my_threads:
        th.join()




