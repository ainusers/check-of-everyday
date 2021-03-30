#coding:utf-8
import itchat
import time
import psutil
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 发送群聊消息
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


# 获取服务器资源信息
def getinfo():
    mem = psutil.virtual_memory()
    memtotal = mem.total
    memfree = mem.free
    memused = mem.used
    return '全部内存：'+str(round((memtotal * 1.0) / 1073741824,2))+'G ， 已使用内存：'+ str(round((memused * 1.0) / 1073741824,2))+'G ， 未使用内存：'+ str(round((memfree * 1.0) / 1073741824,2))+'G'


# 主函数
if __name__ == '__main__':
    # window使用enableCmdQR=False，Linux使用enableCmdQR=2
    itchat.auto_login(enableCmdQR=False, hotReload=True)
    msg = getinfo()
    while 1:
        SendChatRoomsMsg(u'188服务状态监控',msg)
        time.sleep(60 * 30)
    itchat.run()