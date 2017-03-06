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
    chatWith(robot,'hello,{}.you\'re so lucky that you\'ve been choosed to help ideago test his auto-guess-constellation script.'.format(name),name)
    chatWith(robot,'下面小呆会给你发送四张图片,你要仔细观察四张图片里哪几张含有你的星座，然后把你的结果发送给小呆就可以。举个例子，如果你的星座只有第一和第二张有那就发送12就可以，123都有就发送123,14有就发14,不要发任何多余的字符哦，小呆是没法识别的……[呲牙]',name)
    # 发送图片
    for i in range(4):
        who.send_image("imgs/star{}.png".format(str(i + 1)))

    chatWith(robot,
             '图片发送已完成，请仔细观察后，告诉小呆结果，它就能猜出你的星座了。',name)

    #注册猜星座逻辑
    @robot.register(who)
    def reply_my_friend(msg):
        if msg.type == 'Text':
            m = re.match(r'(\b1?2?3?4?\b)', msg.text)
            res = m.group()
            dict = {'1':1,'2':2,'3':4,'4':8}
            if res != '':
                index = 0
                signs = ['白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座','摩羯座','水瓶座','双鱼座']
                for i in range(len(res)):
                    index += int(dict[res[i]])
                return '小呆知道你的星座了，你的星座是{}--{}---{}，小呆很聪明吧……[得意][偷笑][得意]'.format(signs[index-1],res,index)
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


