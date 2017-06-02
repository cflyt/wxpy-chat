#!/usr/bin/env python
# -*- coding=utf8 -*-
from wxpy import *
import os
import  sys,getopt
import time
import datetime
import re
import logging
import logging.config
import time
#from IPython  import embed

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(name)-12s %(asctime)s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'wxpy.api.bot': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': 'haha.log'
        },
        
    },

    'root': {
        'handlers': ['wxpy.api.bot', ],
        'level': 'DEBUG',
    },

    'loggers': {
        'wxpy.api.bot': {
            'handlers': ['wxpy.api.bot', ],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


global stop

def showFriends(robot):
    # print('friends: %s' % robot.friends())
    for friend in robot.friends():
        print friend.name, friend.nick_name, friend.remark_name, friend.sex

def showFriendInfo(robot, who): 
    friend = robot.friends().search(who)[0]
    print friend.name, friend.nick_name, friend.remark_name, friend.sex

def chatWith(robot,text,who):
    chatter = robot.friends().search(who)[0]
    chatter.send(text)

def showPublic(robot, who):
    mp = robot.mps().search(who)[0]
    print mp.name

def chatWithMp(robot, autobot, who):
    mp = robot.mps().search(who)[0]
    @robot.register(mp,TEXT)
    def tuling_reply(msg):
        logging.info(msg.text)
        msg.province = '广东'
        msg.city = '广州'
        #logging.info(type(msg.province))
        #logging.info(type(msg.city))
        time.sleep(15)
        autobot.do_reply(msg)
        #tuling.do_reply(msg)


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
    chatWith(robot,u'下面小呆会给你发送四张图片,你要仔细观察四张图片里哪几张含有你的星座，然后把你的结果发送给小呆就可以。举个例子，如果你的星座只有第一和第二张有那就发送12就可以，123都有就发送123,14有就发14,不要发任何多余的字符哦，小呆是没法识别的……[呲牙]',name)
    # 发送图片
    for i in range(4):
        who.send_image("imgs/star{}.png".format(str(i + 1)))

    chatWith(robot,
             u'图片发送已完成，请仔细观察后，告诉小呆结果，它就能猜出你的星座了。',name)

    #注册猜星座逻辑
    @robot.register(who)
    def reply_my_friend(msg):
        if msg.type == 'Text':
            m = re.match(r'(\b1?2?3?4?\b)', msg.text)
            res = m.group()
            dict = {'1':1,'2':2,'3':4,'4':8}
            if res != '':
                index = 0
                signs = [u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座',u'摩羯座',u'水瓶座',u'双鱼座']
                for i in range(len(res)):
                    index += int(dict[res[i]])

                if index > 12 : return u'小呆虽然智商低，但眼睛还是很雪亮的，你这个组合根本不可能，你再好好看看图，是不是看错了呢 ……[抠鼻]'

                return u'小呆知道你的星座了，你的星座是{}，小呆很聪明吧……[得意][偷笑][得意]'.format(signs[index-1])
        else:
            return u'请按格式输入你的结果'



def tiaoxi(robot,first_msg,who):
    chatWith(robot,first_msg,who)
    chatter = robot.friends().search(who)[0]
    @robot.register(chatter)
    def reply_my_friend(msg):
        if msg.type == 'Text':
            if msg.text == '非空想家很帅':
                return u'哈哈，谢谢夸奖我爸爸，我替我爸爸给你送花……[玫瑰]'
            else:
                return u'快点夸非空想家很帅，6个字，不要多说一个字……[猪头]'
        else:
            return u'小呆是文字控，别发图片表情之类的,看不懂'
        # return 'received: {} ({})'.format(msg.text, msg.type)


def flowers(robot,whoo):
    chatWith(robot, u'hello,非空想家派我来给您送肉了,每隔30秒多送一头哦,肉肉正在传输中，请耐心等待……(*^__^*)', whoo)
    n = 1
    while (True):
        now = datetime.datetime.now() + datetime.timedelta(seconds=30)
        msg = u'现在时间: %s,这是我第%s次送肉.' % (now.strftime('%H:%M:%S'), str(n))
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


def recieve_picture(robot,who):
    chatter = robot.friends().search(who)[0]
    if who == None: chatter = robot.self
    @robot.register(chatter,except_self=False)
    def print_message(msg):
        if  msg.type == 'Picture':
            now = datetime.datetime.now()
            msg.get_file('wximgs/{}.png'.format(now))


def main():
    robot = Bot(cache_path='data', console_qr=2)
    tuling = Tuling('863b6f8cc148497e93f3a57231f931e1')
    xiaoi = XiaoI('PX9hvCMy1UEy', 'OaH6Axntn1XQR6f4bc18')

    #robot.self.add()
    #robot.self.accept()
    showFriends(robot)
    showFriendInfo(robot, u'为你写诗')
    showFriendInfo(robot, u'喵')
    tuling_reply(robot,tuling,u'喵')
    #showPublic(robot, u'中国联通')
    #chatWithMp(robot, tuling, u'机器人')
    #chatWithMp(robot, xiaoi, u'机器人')
    #chatWith(robot, 'aaaa', 'bluefish')
    #caixingzuo(robot, 'bluefish')
    #recieve_picture(robot,None)
    #tuling_reply(robot,tuling,'bluefish')
    #tuling_reply(robot, tuling, 'Miss-翢瑒')
    #tiaoxi(robot,u'谁说我不能自己说话了,叫爸爸,快点','bluefish')
    ## flowers(robot,'xl')
    #robot.start(block=False)
    embed()
    #robot.join()
    #embed(header='console')
    #robot.logout()

if __name__ == "__main__":
    main()


