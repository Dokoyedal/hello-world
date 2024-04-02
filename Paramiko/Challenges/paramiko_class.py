class Device:
    def __init__(self, ip=None, port='22', username=None, password=None):
       self.ip = ip
       self.port = port
       self.username = username
       self.password = password


    def connect(self):
        import paramiko
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh_client.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password,
                           look_for_keys=False, allow_agent=False)


    def get_shell(self):
        self.shell = self.ssh_client.invoke_shell()


    def execute(self, cmd, timeout=0.5):
        import time
        print(f'Executing {cmd} ...', end=' ')
        self.shell.send(f'{cmd}\n')
        time.sleep(timeout)
        print(f'Done')


    def execute_from_file(self, file, timeout=0.7):
        with open(file) as f:
            commands = f.read().splitlines()
            for cmd in commands:
                self.execute(cmd, timeout)

    def show(self, n=10000):
        output = self.shell.recv(n)
        return output.decode()


    def close(self):
        self.ssh_client.close()


    def method1(self):
        print('se executa method1() in Device')
        return 100



class Linux(Device):
    def execute(self, cmd, timeout=0.5, root=False):
        import time
        if root == False:
            print(f'Executing "{cmd}":')
            self.stdin, self.stdout, self.stderr = self.ssh_client.exec_command(cmd, get_pty=True)
        else:
            print(f'Executing "{cmd}" as root:')
            self.stdin, self.stdout, self.stderr = self.ssh_client.exec_command(f'sudo {cmd}', get_pty=True)
            p = input('Enter password:')
            self.stdin.write(f'{p}\n')
            time.sleep(timeout)

    def show(self):
        output = self.stdout.read().decode()
        return output


    def method2(self):
        x = super().method1()
        print(f'apelare method2() in Linux class {x}')



#########################
# from getpass import getpass
# r1_info = {'ip':'192.168.122.10', 'username':'u1', 'password':'cisco'}
# r1 = Device(**r1_info)
#
# r1.connect()
# r1.get_shell()
# r1.execute('enable')
# # p = getpass.getpass('Enter password:')
# # p = getpass('Enter password:')
# r1.execute('cisco')
# # r1.execute(p + '\n')
# r1.execute('terminal length 0')
# r1.execute('show version')
# output = r1.show()
# print(output)
#
# r1.execute_from_file('a.txt')
# output = r1.show()
# print(output)
# r1.close()

######################

l1 = Linux(ip='127.0.0.1', port='2222', username='stud', password='cmastud')
l1.method2()

l1.connect()
l1.execute('tail -n 5 /etc/shadow', root=True)
print(l1.show())