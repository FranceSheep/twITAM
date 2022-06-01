import tweepy
import datetime
import pandas as pd  
import os
from ultis import *
import matplotlib.pyplot as plt

#sustantivos = '(ITAM OR @ITAM_mx)'
#adjetivos_pos = '(estoy feliz OR alegre OR aliviado OR aliviada)'
#adjetivos_neg = '(triste OR enojado OR enojada OR ansioso OR ansiosa OR hasta la madre)'
#query = f'{sustantivos}'

class TwITAM:
    def __init__(self, data_path):
        self.data_path = data_path
        self.auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAPXBaQEAAAAAdkCJ2DPJdlXod0Y4dSG9CtJUqCE%3Dt2ezG3CNPpHGj7Lb692Vgq8gkAq4Sfkof3ZzcOHSr38ppE45rq")
        self.tweet_gate = tweepy.API(self.auth)
        self.query = '(ITAM OR @ITAM_mx OR #ITAM)'
        self.accounts_ITAM = ['ITAM_mx','DAE_ITAM','EconomiaITAM','RRII_ITAM','CPoliticaITAM','ITAM_Biblioteca','ITAMMusica','DataAlgoSocITAM','EstadisticaITAM','Derecho_ITAM','IntercambioITAM','CDA_ITAM','IngenieriaITAM','ITAMuniversity','AspirantesITAM','DiplomadosITAM','PosgradosITAM','ExITAM','EnergiaITAM']
        self.tweets_data = []
        self.id_data = []
        self.dates = []
        
        self.num_positives = []
        self.num_negatives = []
        self.final_conns = []

    def get_tweets(self,days):
        today = datetime.date.today()
        time_lapse = datetime.timedelta(days)
        tweets = self.tweet_gate.search_tweets(self.query,lang='es',count=100,until=today-time_lapse)
        for twit in tweets:
            if not twit.retweeted and 'RT @' not in twit.text and twit.user.screen_name not in self.accounts_ITAM:
                idTweet = twit.id
                status = self.tweet_gate.get_status(idTweet, tweet_mode="extended")
                #print(status.full_text )
                self.tweets_data.append(status.full_text)
                self.id_data.append(idTweet)
                self.dates.append(pd.to_datetime(twit.created_at))
                #print(twit.user.screen_name)
                #print('\n')
                
    def get_connotation(self):
        for tweet in self.tweets_data:
            conn = connotation(tweet)
            self.num_positives.append(conn[0])
            self.num_negatives.append(conn[1])
            self.final_conns.append(conn[2])
            
    def get_dataFrame(self):
        pre_dict = {'id':self.id_data, 'tweet': self.tweets_data,'date':self.dates, 'positives': self.num_positives, 'negatives': self.num_negatives, 'tweet_connotation':self.final_conns}
        self.df = pd.DataFrame(pre_dict)
        #print(self.df['negatives'])
        #print(self.df['date'])
        #print(self.df['negatives'].sum())
        #print(self.df['positives'].sum())

        #print(self.df.groupby('tweet_connotation').count()['id'])
        print(self.df)
        
home_dir = '.'                
tw = TwITAM(os.path.join(home_dir, 'tweets'))
for i in range(8):
    tw.get_tweets(i)
tw.get_connotation()
tw.get_dataFrame()
