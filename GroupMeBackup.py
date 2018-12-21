import requests
import sys
import os
import urllib.request as req

class Backup:
    def __init__(self, input):
        self.accessToken = input
        self.messageIndex = []
    
    def write(self):
        a = False
        u = False
        t = False
        f = False
        attachmentNum = 0
        print('Options:', '    (u)sername: prints usernames before message', '    (t)ime: prints the absolute time out', '    (f)avorites: prints out number of favorites on message', '    (a)ttachments: saves all attachments to folder', '    (e)verything: all options true', sep='\n')
        options = input('Choose any options you want (i.e. \'u t\'): ').split()
        if 'a' in options or 'e' in options:
            a = True
            attachmentNum = 1
            try:
                os.mkdir(self.title+'/Attachments')
            except OSError:
                option = input('Would you like to overwrite attachments? (y/n) ')
                if option == 'n':
                    a = False
        if 'u' in options or 'e' in options:
            u = True
        if 't' in options or 'e' in options:
            t = True
        if 'f' in options or 'e' in options:
            f = True

        for number, message in enumerate(reversed(self.messageIndex)):
            text = '\rSaving: {0}% {1}/{2} messages'.format(int(100*(float(number)/float(self.total))), number, self.total)
            sys.stdout.write(text)
            sys.stdout.flush()
            try:
                if a:
                    for attachment in message['attachments']:
                        if attachment['type'] == 'image':
                            req.urlretrieve(attachment['url'], self.title+'/Attachments/'+str(attachmentNum)+'.png')
                            attachmentNum += 1
            
                text = message['text']
                if text == None:
                    text = "\n"
                
                if t:
                    self.outputFile.write(str(message['created_at'])+' ')
                
                if u:
                    self.outputFile.write(message['name'] + ': ')
                
                self.outputFile.write(text)
                
                if f:
                    self.outputFile.write(" ♥: " + str(len(message['favorited_by'])))

                self.outputFile.write('\n')
            except TypeError:
#                print(message)
                print('ErrorPrinting')
        print('\n')

    def pull(self):
        print('Backing-up "', self.groupInfo['name'], '":',sep='')
        self.title = '_'.join(self.groupInfo['name'].split())
        try:
            os.mkdir(self.title)
            self.outputFile = open(self.title + '/' + self.title + '.txt', 'w')
        except OSError:
            option = input('Would you like to overwrite this backup? (y/n) ')
            if option == 'y':
                self.outputFile = open(self.title + '/' + self.title + '.txt', 'w')
            else:
                exit()
        
        requestParameters = {'token': self.accessToken, 'limit': 100}
        self.total = requests.get('https://api.groupme.com/v3/groups/' + str(self.groupId) + '/messages', params = requestParameters).json()['response']['count']
        number = 0
        
        while True:
            try:
                responseMessages = requests.get('https://api.groupme.com/v3/groups/' + str(self.groupId) + '/messages', params = requestParameters).json()['response']['messages']
            except ValueError:
                break

            number += len(responseMessages)
            text = '\rProgress: {0}% {1}/{2} messages'.format(int(100*(float(number)/float(self.total))), number, self.total)
            sys.stdout.write(text)
            sys.stdout.flush()
            
            for message in responseMessages:
                self.messageIndex.append(message)
            requestParameters['before_id'] = responseMessages[-1]['id']
        print('\n')
        self.write()

def main():
    accessToken = str(input("Enter Access Token: "))

    requestParameters = {'token': accessToken, 'per_page': 15, 'page': 1}

    backup = Backup(accessToken)

    groups = requests.get('https://api.groupme.com/v3/groups', params = requestParameters).json()['response']

    while True:
        for num, group in enumerate(groups):
            print('[',num,'] ', group['name'],sep='')
        groupIndex = input('Which group would you like to backup? (# or \'next/prev\'): ')
        if groupIndex == 'next':
            requestParameters['page'] += 1
            groups = requests.get('https://api.groupme.com/v3/groups', params = requestParameters).json()['response']
        elif groupIndex == 'prev':
            requestParameters['page'] -= 1
            if not requestParameters['page']:
                requestParameters['page'] = 1
            groups = requests.get('https://api.groupme.com/v3/groups', params = requestParameters).json()['response']
        else:
            try:
                backup.groupId = groups[int(groupIndex)]['id']
                backup.groupInfo = groups[int(groupIndex)]
                break
            except TypeError:
                print('Enter a number or \'next/prev\'!')
            except ValueError:
                print('Enter a number or \'next/prev\'!')

    backup.pull()



if __name__ == '__main__':
    main()

