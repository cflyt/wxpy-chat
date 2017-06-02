#!/usr/bin/env python
# -*- coding=utf8 -*-

import  sys

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

# 初始化机器人
chatbot = ChatBot(
            'Ron Obvious',
                trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
                )
chatbot.set_trainer(ChatterBotCorpusTrainer)

# 这里先使用该库现成的中文语料库训练
chatbot.train("chatterbot.corpus.chinese")  

chatbot.set_trainer(ListTrainer)
chatbot.train([
        u"讲个笑话",
        u"一天和同学出去吃饭，买单的时候想跟服务员开下玩笑。“哎呀，今天没带钱出来埃”“你可以刷卡。”“可是我也没带卡出来的埃”“那你可以刷碗“",
            ])

def main(argv):
    #参数长度为1
    if  len(argv) == 1:
        cmd = argv[0]
        if cmd == 'showFriendList':
            print('showFriendList')
            return

        if cmd == 'showFriendSurvey':
            print('showFriendSurvey')
            return

        print('unknow cmd')


if __name__ == "__main__":
    question = raw_input("请和我聊天: ") 
    while question:
        anser = chatbot.get_response(question.decode('utf8'))
        print anser.text
        question = raw_input() 
