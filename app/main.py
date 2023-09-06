import socket
import wakeonlan
import binascii
import os

###########################################
# 使用wakeonlan的lib来实现wake on lan
def wake_on_lan(mac, ip, port=9):
    '''
    mac: mac address of the target machine
    ip: 机器所在IP的广播，如果是192.168.0.24，那么广播就是192.168.0.255
    port: 默认是9, 一般不用改, 可选是7
    '''
    wakeonlan.send_magic_packet(mac, ip_address=ip, port=port)


#############################################
# socket实现wake on lan
'''
格式化mac地址，生成魔法唤醒包，然后发送。
mac格式： mac = A1B2C3D4E5F6
唤醒包格式： send_data = binascii.unhexlify('FF'*6 + str(mac)*16)
'''
# 将mac地址中可能存在的':'或者'-'去掉
def preprocess_mac(mac): 
    mac = mac.replace(':', '')
    mac = mac.replace('-', '')
    return mac

def generate_magic_packet(mac):
    mac = preprocess_mac(mac)
    if len(mac) != 12: # mac地址长度为12位
        raise ValueError('Incorrect MAC address format')
    magic_packet = 'FF'*6 + str(mac)*16
    send_data = binascii.unhexlify(magic_packet)   # 返回由十六进制字符串 hexstr 表示的二进制数据, 也就是16进制转换成二进制
    #print(type(send_data))                                 # <class 'bytes'>, bytes类型
    return mac,send_data

def transfer(ip):
    ip_list = ip.split('.')
    broadcast_ip = ip_list[0] + '.' + ip_list[1] + '.' + ip_list[2] + '.255'
    return broadcast_ip

def send_magic_packet(mac, ip, port):
    # 将IP转换到整个广播区域
    broadcast_ip = transfer(ip)
    print(f'转换ip地址到广播地址{broadcast_ip}')
    # 生成唤醒包
    formatted_mac, send_data = generate_magic_packet(mac)
    print(f'为{formatted_mac}生成唤醒包,发送唤醒包，端口为{port}')
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # 将数据发送到指定地址
    s.sendto(send_data, (broadcast_ip, port))
    # 关闭socket
    s.close()
    print('发送完成')

if __name__ == "__main__":  # 这个相当于main函数，但当这个文件被其他文件import的时候，这个main函数不会被执行
    print("hello, docker")
    #your_mac = "11:22:33:44:55:66"
    #your_ip = '192.168.5.255' #needs to be broadcast address
    #port = 9
    #wake_on_lan(your_mac, your_ip, port)
    # --- above is another way to wake on lan ---
    print('start to run wake on lan...')
    mac = os.environ.get('mac','a1b2c3d4e5f6')
    ip = os.environ.get('ip','255.255.255.255')
    port = os.environ.get('port',9)

    send_magic_packet(mac,ip,port)