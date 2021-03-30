# encoding: utf-8
"""
Author: ty
CreateTime: 2021-3-26
Info: 简单监控的CPU利用率、CPU平均负载、硬盘使用率、内存使用率 和 各个端口的开启状况
"""

import socket
import os
import time
import itchat
import paramiko
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def serviceGetinfo():
	# 获取IP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	ip = s.getsockname()[0]

	# 获取端口信息
	portMsg='服务状态：'
	result = os.popen("netstat -nultp | grep java | awk '{print $4}' | sed 's/.*:\(.*\)/\\1/' | grep 9443").read().strip()
	if len(result) <=0:
		portMsg = portMsg + '\n主程序服务挂了，快去修复哈'
	else:
		portMsg = portMsg + '\n主程序服务正常'
	result = os.popen("netstat -nultp | grep java | awk '{print $4}' | sed 's/.*:\(.*\)/\\1/' | grep 9444").read().strip()
	if len(result)<=0:
		portMsg = portMsg + '\nStream服务挂了，快去修复哈'
	else:
		portMsg = portMsg + '\nStream服务正常'

	# CPU利用率
	f = os.popen("top -bi -n 1| awk '{print $4}'").read().split('\n')[2]
	cpuUsedMsg = "CPU利用率:"+str(f)+ "%"
	# CPU平均负载
	f = os.popen("uptime | sed 's/,//g' | awk '{print $8,$9,$10}'")
	str_aver_load = f.read().strip().split(":")[1].strip()
	CPUaverLoadMsg ="CPU平均负载: {:.2%}".format(float(str_aver_load))
	# 获取磁盘使用率
	disk_val = os.popen("df -h | head -2 | tail -1 |awk '{print $5}'").read().strip()
	diskUsedMsg ="磁盘使用率:"+disk_val
	# 获取内存使用率
	f = os.popen("free -m |grep Mem |awk '{print $3/$2}'")
	str_men = f.read().strip()
	memUsedmSG ="内存使用率: {:.2%}".format(float(str_men))
	#获取全部内存
	f = os.popen("free -g |grep Mem |awk '{print $2}'")
	memtotal = f.read().strip()
	memtotalMsg = "全部内存:" + memtotal+"G"
	# 获取已使用内存
	f = os.popen("free -g |grep Mem |awk '{print $3}'")
	memused = f.read().strip()
	memusedMsg = "已使用内存:" + memused+"G"
	# 获取未使用内存
	f = os.popen("free -g |grep Mem |awk '{print $4}'")
	memfree = f.read().strip()
	memfreeMsg = "未使用内存:" + memfree + "G"

	return 'IP为' + ip + '的服务器：' + \
		   '\n'+diskUsedMsg+'\n'+memUsedmSG+'\n'+cpuUsedMsg+'\n'+CPUaverLoadMsg+'\n'+memtotalMsg+'\n'+memusedMsg+'\n'+memfreeMsg+'\n'+portMsg+'\n'

def ssh(ip,username,passwd,cmd):
    RealTimeDataMsg=''
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            #屏幕输出
            for o in out:
                #print(o)
                RealTimeDataMsg=RealTimeDataMsg+o
                ssh.close()
    except :
        RealTimeDataMsg=('%s\tError\n'%(ip))
    return RealTimeDataMsg

def RealTimeDataGetinfo():
	cmd = ['python /opt/RealTimeData.py']  # 你要执行的命令列表
	username = "root"  # 用户名
	passwd = "edoc2"  # 密码
	ip = "192.168.251.80"
	RealTimeDataMsg = ssh(ip, username, passwd, cmd)
	return RealTimeDataMsg

def SendChatRoomsMsg(gname,context):
    # 获取群组所有的相关信息（注意最好群聊保存到通讯录）
    myroom = itchat.get_chatrooms(update=True)
    # 传入指定群名进行搜索，之所以搜索，是因为群员的名称信息也在里面
    myroom = itchat.search_chatrooms(name=gname)
    for room in myroom:
        # 遍历所有NickName为键值的信息进行匹配群名
        if room['NickName'] == gname:
            username = room['UserName']
            # 得到群名的唯一标识，进行信息发送
            itchat.send_msg(context,username)
        else:
            print('未找到群聊')

if __name__ == '__main__':
	#window使用enableCmdQR=False，Linux使用enableCmdQR=2
	itchat.auto_login(enableCmdQR=2, hotReload=True)

	serviceMsg = serviceGetinfo()
	RealTimeDataMsg = RealTimeDataGetinfo()
	msg = serviceMsg+'\n'+RealTimeDataMsg
	while 1:
	      print(msg)
	      SendChatRoomsMsg(u'服务状态监控', msg)
	      time.sleep(60 * 360)
	itchat.run()
