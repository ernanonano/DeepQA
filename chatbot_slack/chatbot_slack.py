import logging
import sys

import sys
import os

import os.path
#chatbotPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
chatbotPath = os.path.abspath(os.getcwd())
print(chatbotPath)
sys.path.append(chatbotPath)
from chatbot import chatbot
from slackclient import SlackClient 
import time


logger = logging.getLogger(__name__)


class ChatbotManager():
    """ Manage a single instance of the chatbot shared over the website
    """
    def __init__(self, modelTag='ubuntu'):
        self.name = 'chatbot_slack_interface'
        self.verbose_name = 'Chatbot Slack Interface'

        self.bot = None
        self.modelTag = modelTag
    
    def initSlack(self):
        slack_token = os.environ["SLACK_API_TOKEN"] 
        self.sc = SlackClient(slack_token)
        self.users_dict = {}
        for u in self.sc.api_call("users.list")['members']:
            self.users_dict[u['id']] =  u['name']

    #@staticmethod
    def initBot(self):
        """ Instantiate the chatbot for later use
        Should be called only once
        """
        if not self.bot:
            logger.info('Initializing bot...')
            self.bot = chatbot.Chatbot()
            self.bot.main(['--modelTag', self.modelTag, '--test', 'daemon', '--rootDir', chatbotPath])
            #self.bot.main(['--modelTag', self.modelTag, '--test', 'daemon'])
        else:
            logger.info('Bot already initialized.')

    #@staticmethod
    def callBot(self, sentence):
        """ Use the previously instantiated bot to predict a response to the given sentence
        Args:
            sentence (str): the question to answer
        Return:
            str: the answer
        """
        if self.bot:
            return self.bot.daemonPredict(sentence)
        else:
            logger.error('Error: Bot not initialized!')
            
            
    def readAndProcessSlackMessagesLoop(self):
        if self.sc.rtm_connect():  # connect to a Slack RTM websocket 
            while True: 
                data=self.sc.rtm_read()  # read all data from the RTM websocket 
                if data and "text" in data[0] and 'bot_id' not in data[0]: 
                    logger.info(str(data) )
                    print(str(data))
                    channel=data[0]['channel'] 
                    text=data[0]['text']
                    user=data[0]['user']
                    print(user, self.users_dict)
                    if user in self.users_dict:
                        print("found user")
                        user = self.users_dict[user]
                    response = self.callBot(text)
                    response = response.replace('nombre_de_usuario','@'+str(user))
                    self.sc.api_call( 
                        "chat.postMessage", 
                        channel=channel, 
                        text=response 
                    ) 
                time.sleep(1) 
        else: 
          print( 'Connection Failed, invalid token?')


if __name__ == "__main__":
    #cm = ChatbotManager('ubuntu')
    cm = ChatbotManager('movistar_100k')
    cm.initBot()
    cm.initSlack()
    cm.readAndProcessSlackMessagesLoop()
