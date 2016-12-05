import pickle

with open('valid_ip.txt', 'rb') as file:
    ip_port_list = pickle.load(file)

for ip in ip_port_list:
    print('[%s]' % ip)
