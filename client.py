import socket,pickle,random
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
x= 113.9965
y= 22.599
for i  in range(10):
    la = x + i*0.001*random.random()
    lo = y + i*0.001*random.random()
    data = tuple([la,lo])
    # 发送数据:
    s.sendto(pickle.dumps(data), ('0.0.0.0', 12345))
    # 接收数据:
    # print(s.recv(1024).decode('utf-8'))
s.close()