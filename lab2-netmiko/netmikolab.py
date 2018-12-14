from netmiko import ConnectHandler
import re

############################################################
#### CONFIG
############################################################
conn_params = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.122.92',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',     # optional, defaults to ''
}

c = ConnectHandler(**conn_params)
c.enable()

params = {
    'hostname': 'R1-masaki',
    'motd': 'This is Masaki\'s router',
    'ntp_server': '193.40.5.113',
    'syslog_server': '192.168.122.1'
}

############################################################
#### FUNCTIONS
############################################################
def send_cfg_command(command):
    cfg_commands = [command]
    return c.send_config_set(cfg_commands)

def is_ip_address(value):
    return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",value)

def is_ospf_neighbor_id(value):
    return re.match(r"^\d{1}\.\d{1}\.\d{1}\.\d{1}$",value)

def get_hostname():
    output = c.send_command('sh run | s hostname')
    output_line_arr = output.split()
    hostname = output_line_arr[1]
    return hostname

def set_hostname(hostname):
    send_cfg_command('hostname ' + hostname)

def get_motd():
    output = c.send_command('sh run | s banner')
    output_line_arr = output.split()
    motd = []
    inSpace = False

    for i in range(len(output_line_arr)):
        target = output_line_arr[i]
        if(re.search('\^C', target) is not None and inSpace is False):
            inSpace = True
        
        if(inSpace):
            motd.append(target)

    return ' '.join(motd)

def set_motd(motd):
    send_cfg_command('banner motd \$ ' + motd + ' \$')

def get_ntp_server():
    output = c.send_command('sh run | s ntp')
    output_line_arr = output.split()
    if(len(output_line_arr) == 0):
        return None
    return output_line_arr[len(output_line_arr) - 1]

def set_ntp_server(ntp_server):
    send_cfg_command('ntp server ' + ntp_server)

def get_syslog_server():
    output = c.send_command('sh run | s logging')
    output_line_arr = output.split()
    if(len(output_line_arr) == 0):
        return None

    target = None
    for i in range(len(output_line_arr)):
        target = output_line_arr[i]
        if(is_ip_address(target)):
            break
    return target

def set_ospf(network, wildcardmask):
    cfg_commands = ['router ospf 1', 'network ' + network + ' ' + wildcardmask + ' area 0']
    c.send_config_set(cfg_commands)

def get_ospf_neighbor_ids():
    output = c.send_command('sh ip ospf neighbor ')
    output_line_arr = output.split()
    
    neighbors = []
    for i in range(len(output_line_arr)):
        target = output_line_arr[i]
        if(is_ospf_neighbor_id(target)):
            neighbors.append(target)
    
    return neighbors
            


############################################################
#### BASIC CONFIG
############################################################

correct_hostname = params['hostname']
hostname = get_hostname()
if(hostname == correct_hostname):
    print 'Hostname: ' + hostname
else:
    print 'Incorrect hostname : ' + hostname
    set_hostname(correct_hostname)
    hostname = get_hostname()
    print 'Updated hostname : ' + hostname 

correct_motd = params['motd']
motd = get_motd()
if(re.search(params['motd'], motd) is not None):
    print 'Motd: ' + motd
else:
    print 'Incorrect motd : ' + motd
    set_motd(correct_motd)
    motd = get_motd()
    print 'Updated motd : ' + motd 

correct_ntp_server = params['ntp_server']
ntp_server = get_ntp_server()
if(ntp_server is not None):
    print 'NTP server: ' + ntp_server
else:
    print 'Incorrect NTP server : ' + 'None'
    set_ntp_server(correct_ntp_server)
    ntp_server = get_ntp_server()
    print 'Updated NTP server : ' + ntp_server 

correct_syslog_server = params['syslog_server']
syslog_server = get_syslog_server()
if(syslog_server is not None):
    print 'Syslog server: ' + syslog_server
else:
    print 'Incorrect syslog server : ' + 'None'
    set_ntp_server(correct_syslog_server)
    syslog_server = get_syslog_server()
    print 'Updated syslog server : ' + syslog_server 

############################################################
#### OSPF
############################################################
set_ospf('10.0.2.0', '0.0.0.3')
set_ospf('10.0.3.0', '0.0.0.3')
set_ospf('1.1.1.1', '0.0.0.255')

neighbors = get_ospf_neighbor_ids()
print 'OSPF neighbors: '
for i in range(len(neighbors)):
    neighbor_id = neighbors[i]
    print neighbor_id
