from wxpy import *
import os
import  sys,getopt
import time
import datetime
import re
from IPython  import embed

global stop

def showFriends(robot):
    print('chats : %s' % robot.friends().stats_text())
    # print('friends: %s' % robot.friends())
    for friend in robot.friends():
        print(friend.display_name)

def chatWith(robot,text,who):
    chatter = robot.friends().search(who)[0]
    chatter.send(text)

def reply(robot,text,who):
    chatter = robot.friends().search(who)[0]
    @robot.register(chatter)
    def reply_my_friend(msg):
        return 'received: {} ({})'.format(msg.text, msg.type)

def tuling_reply(robot,tuling,who):
    chatter = robot.friends().search(who)[0]
    @robot.register(chatter,TEXT)
    def tuling_reply(msg):
        tuling.do_reply(msg)


def ff(robot,name):
    chatter = robot.friends().search(name)[0]
    return chatter

def fg(robot,name):
    g = ensure_one(robot.groups().search(name))
    g.update_group(True)
    return g

def caixingzuo(robot,name):
    who = ff(robot,name)
    # 发送图片
    for i in range(4):
        who.send_image("imgs/star{}.png".format(str(i + 1)))

    #注册猜星座逻辑
    @robot.register(who)
    def reply_my_friend(msg):
        if msg.type == 'Text':
            m = re.match(r'(1?2?3?4?)', msg.text)



        else:
            return '请按格式输入你的结果'



def tiaoxi(robot,first_msg,who):
    chatWith(robot,first_msg,who)
    chatter = robot.friends().search(who)[0]
    @robot.register(chatter)
    def reply_my_friend(msg):
        if msg.type == 'Text':
            if msg.text == '爸爸':
                return '哈哈，儿子乖，爸爸明天给你买棒棒糖……[阴险]'
            else:
                return '快点叫爸爸，2个字，不要多说一个字……[猪头]'
        else:
            return '爸爸文字控，别发图片表情之类的,看不懂'
        # return 'received: {} ({})'.format(msg.text, msg.type)


def flowers(robot,whoo):
    chatWith(robot, 'hello,非空想家派我来给您送肉了,每隔30秒多送一头哦,肉肉正在传输中，请耐心等待……(*^__^*)', whoo)
    n = 1
    while (True):
        now = datetime.datetime.now() + datetime.timedelta(seconds=30)
        msg = '现在时间: %s,这是我第%s次送肉.' % (now.strftime('%H:%M:%S'), str(n))
        delay_msg(robot,30,whoo,msg)
        # 送花
        flower = ''
        for i in range(n):
            flower += '[猪头]'
        chatWith(robot, flower, whoo)
        n += 1

def delay_msg(robot,delay,who,text):
    time.sleep(delay)
    chatWith(robot,text,who)


def main():
    robot = Robot(save_path='data')
    tuling = Tuling('a9f9aad2e3cb49a88615364568e60770')
    tuling_reply(robot,tuling,'林飞')
    tuling_reply(robot, tuling, 'Miss-翢瑒')
    # tiaoxi(robot,'谁说我不能自己说话了,叫爸爸,快点','xl')
    # flowers(robot,'xl')
    robot.start(block=False)
    embed(header='console')
    robot.logout()

if __name__ == "__main__":
    main()


