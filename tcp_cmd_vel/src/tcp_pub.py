#! /usr/bin/env python

import rospy
import asyncore
import socket
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist
HOST_NAME = ''
HOST_PORT = 5060

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1024)
        
        if not data:
            self.close()
        
        data = data.decode('utf-8')
        dataMessage = data.split(' ')
        
        if dataMessage[0] != 'x':
            return
        if dataMessage[3] != 'x':
            return
        
        X = int(dataMessage[1])
        Y = int(dataMessage[2])
        Xoutput = abs(X-50)*2
        Youtput = abs(Y-50)*2

        #command = dataMessage[1]
        #self.send(command.encode('utf-8'))

        pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
        rospy.init_node('tcp_pub_cmd_vel')
        #rospy.init_node('tcp_pub_cmd_vel', anonymous=True)
        #rate = rospy.Rate(10) # 10hz
        twist = Twist()
        twist.linear.x = (float(dataMessage[1]))/1000; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = (float(dataMessage[2]))/1000
        pub.publish(twist)

    def handle_close(self):
        self.close()

class EchoServer(asyncore.dispatcher):
    def __init__(self, ip, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(1)

    def handle_accept(self):
        sock, addr = self.accept()
        print ("Connection from", addr)
        EchoHandler(sock)

s = EchoServer(HOST_NAME, HOST_PORT)
asyncore.loop()