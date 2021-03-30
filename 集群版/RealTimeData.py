# encoding: utf-8
"""
Author: ty
CreateTime: 2020-3-26
Info: 简单监控的CPU利用率、CPU平均负载、硬盘使用率、内存使用率 和 各个端口的开启状况
"""
import socket
import os


def getinfo():
    # 获取IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]

    # 获取端口信息
    portMsg = '服务状态：'
    result = os.popen("netstat -nultp | grep java | awk '{print $4}' | sed 's/.*:\(.*\)/\\1/' | grep 9645").read().strip()
    if len(result) <= 0:
        portMsg = portMsg + '\nportal服务挂了，快去修复哈'
    else:
        portMsg = portMsg + '\nportal服务正常'

    result = os.popen("netstat -nultp | grep java | awk '{print $4}' | sed 's/.*:\(.*\)/\\1/' | grep 9648").read().strip()
    if len(result) <= 0:
        portMsg = portMsg + '\nmonitor服务挂了，快去修复哈'
    else:
        portMsg = portMsg + '\nmonitor服务正常'

    result = os.popen("netstat -nultp | grep java | awk '{print $4}' | sed 's/.*:\(.*\)/\\1/' | grep 9744").read().strip()
    if len(result) <= 0:
        portMsg = portMsg + '\nbussiness-rule服务挂了，快去修复哈'
    else:
        portMsg = portMsg + '\nbussiness-rule服务正常'

    result = os.popen("netstat -nultp | grep java | awk '{print $4}' | sed 's/.*:\(.*\)/\\1/' | grep 9391").read().strip()
    if len(result) <= 0:
        portMsg = portMsg + '\neditor服务挂了，快去修复哈' + '\ntemplate-editor服务挂了，快去修复哈'
    else:
        portMsg = portMsg + '\neditor服务正常' + '\ntemplate-editor服务正常'
    # CPU利用率
    f = os.popen("top -bi -n 1 | awk '{print $4}'").read().split('\n')[2]
    cpuUsedMsg = "CPU利用率:" + str(f) + "%"
    # CPU平均负载
    f = os.popen("uptime | sed 's/,//g' | awk '{print $8,$9,$10}'")
    str_aver_load = f.read().strip().split(":")[1].strip()
    CPUaverLoadMsg = "CPU平均负载: {:.2%}".format(float(str_aver_load))
    # 获取磁盘使用率
    disk_val = os.popen("df -h | head -2 | tail -1 |awk '{print $5}'").read().strip()
    diskUsedMsg = "磁盘使用率:" + disk_val
    # 获取内存使用率
    f = os.popen("free -m |grep Mem |awk '{print $3/$2}'")
    str_men = f.read().strip()
    memUsedmSG = "内存使用率: {:.2%}".format(float(str_men))
    # 获取全部内存
    f = os.popen("free -g |grep Mem |awk '{print $2}'")
    memtotal = f.read().strip()
    memtotalMsg = "全部内存:" + memtotal + "G"
    # 获取已使用内存
    f = os.popen("free -g |grep Mem |awk '{print $3}'")
    memused = f.read().strip()
    memusedMsg = "已使用内存:" + memused + "G"
    # 获取未使用内存
    f = os.popen("free -g |grep Mem |awk '{print $4}'")
    memfree = f.read().strip()
    memfreeMsg = "未使用内存:" + memfree + "G"

    return 'IP为' + ip + '的服务器：' + \
           '\n' + diskUsedMsg + '\n' + memUsedmSG + \
           '\n' + cpuUsedMsg + '\n' + CPUaverLoadMsg + \
           '\n' + memtotalMsg + '\n' + memusedMsg + \
           '\n' + memfreeMsg + '\n' + portMsg + '\n'


if __name__ == '__main__':
    msg = getinfo()
    print(msg)


