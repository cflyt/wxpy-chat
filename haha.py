from wxpy import *
import os
import  sys,getopt
import time
import datetime

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


def tiaoxi(robot,first_msg,who):
    chatWith(robot,first_msg,who)
    chatter = robot.friends().search(who)[0]
    @robot.register(chatter)
    def reply_my_friend(msg):
        if msg.type == 'Text':
            if msg.text == '大叔是好人':
                return '哈哈，小妮子乖，大叔明天给你买棒棒糖……[阴险]'
            else:
                return '说大叔是好人，5个字，不要多说一个字……[猪头]'
        else:
            return '大叔文字控，别发图片表情之类的,看不懂'
        # return 'received: {} ({})'.format(msg.text, msg.type)


def flowers(robot,whoo):
    chatWith(robot, 'hello,非空想家派我来给您送花了,每隔1分钟多送一朵哦,鲜花正在传输中，请耐心等待……(*^__^*)', whoo)
    n = 1
    while (true):
        now = datetime.datetime.now() + datetime.timedelta(seconds=60)
        msg = '现在时间: %s,这是我第%s次送花.' % (now.strftime('%H:%M:%S'), str(n))
        delay_msg(robot,60,whoo,msg)
        # 送花
        flower = ''
        for i in range(n):
            flower += '[玫瑰]'
        chatWith(robot, flower, whoo)
        n += 1

def delay_msg(robot,delay,who,text):
    time.sleep(delay)
    chatWith(robot,text,who)

def main():
    robot = Robot(save_path='data.txt')
    tuling = Tuling('a9f9aad2e3cb49a88615364568e60770')
    tuling_reply(robot,tuling,'林飞')
    tuling_reply(robot, tuling, 'xl')
    robot.start()

if __name__ == "__main__":
    main()


