import  paramiko


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname= '192.168.122.8', port='22', username='nat', password='test', look_for_keys=False, allow_agent=False)


print(ssh_client.get_transport().is_active())






