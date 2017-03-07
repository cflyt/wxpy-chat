import itchat
itchat.auto_login(hotReload=True)

@itchat.msg_register(['Picture','Recording','Attachment','Video'])
def download_files(msg):
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']), msg['FromUserName'])
    return '%s received' % msg['Type']


