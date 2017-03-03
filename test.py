import  sys

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
    main(sys.argv[1:])