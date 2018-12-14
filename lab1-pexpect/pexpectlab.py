import pexpect
import re

conn = pexpect.spawn('telnet 192.168.122.39')
conn.expect('sername:')
conn.sendline('admin')
conn.expect('assword:')
conn.sendline('password')
conn.expect('>')
conn.sendline('en')
conn.expect('assword:')
conn.sendline('cisco')
conn.expect('#')
conn.sendline('conf t')
conn.expect('#')

conn.sendline('do show run | s hostname')
conn.expect('#')
output = conn.before
if(not re.search('R1-masaki', output)):
	conn.sendline('host R1-masaki'):
	conn.expect('#')
	print('Hostname Set')
else:
	print('Hostname OK')

conn.sendline('do show run | s ntp')
conn.expect('#')
output = conn.before
lines = output.splitlines()

if(not re.search('193.40.5.113', output)):
	if(len(lines) > 2):
		for i in range(1, len(lines) - 1):
			serverIp = lines[i].split()[2]
			conn.sendline('no ntp server ' + serverIp)
			conn.expect('#')
		conn.sendline('ntp server 193.40.5.113')
		conn.expect('#')
		print('NTP server set')
	else:
		print('NTP server is not set')
		conn.sendline('ntp server 193.40.5.113')
		conn.expect('#')
		print('NTP server set successfully')
else:
	if(len(lines) > 3):
		for i in range(1, len(lines) - 1):
			if(not re.search('193.40.5.113', lines[i])):
				serverIp = lines[i].split()[2]
				conn.sendline('no ntp server ' + serverIp)
				conn.expect('#')
			else:
				continue
		print('Removed extra NTP servers')
	else:
		print('NTP OK')


conn.sendline('do show run | s banner')
conn.expect('#')
output = conn.before
if(not re.search('Masaki owns this rotuer', output)):
	conn.sendline('banner motd \$ Masaki owns this rotuer \$')
	conn.expect('#')
	print('Banner Set')
else:
	print('Banner Ok')

conn.sendline('do show run | s logging host')
conn.expect('#')
output = conn.before
lines = output.splitlines()
if(not re.search('', output)):
	if(len(lines) > 2):
		for i in range(1, len(lines) - 1):
			serverIp = lines[i].split()[2]
			conn.sendline('no logging host ' + serverIp)
			conn.expect('#')
		conn.sendline('logging host 192.168.122.1')
		conn.expect('#')
		print('Logging Host Set')
	else:
		print('Logging Host is not set')
		conn.sendline('logging host 192.168.122.1')
		conn.expect('#')
		print('Logging Host set successfully')
else:
	if(len(lines) > 3):
		for i in range(1, len(lines) - 1):
			if(not re.search('192.168.122.1', lines[i])):
				serverIp = lines[i].split()[2]
				conn.sendline('no logging host ' + serverIp)
				conn.expect('#')
			else:
				continue
		print('Removed extra Logging Hosts')
	else:
		print('Logging host OK')

conn.sendline('end')
conn.expect('#')
conn.sendline('copy run st')
conn.expect('startup')
conn.sendline('\n')
result = conn.expect('\[OK]')
print(result)
