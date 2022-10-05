import pandas as pd
import re
import emoji
import numpy as np
from collections import Counter

class Creat_Data_Frame:
     def __init__(self, text_data) -> None:
        self.text_data =text_data
     def dataframe(self):
            pattern_for_date="\d\d/\d\d/\d\d,.\d{1,2}:\d\d.\w\w"
            us_mess=re.split(pattern_for_date,self.text_data)[1:]
            dates=re.findall(pattern_for_date,self.text_data)
            data=pd.DataFrame(list(zip(dates,us_mess)),columns=['date',"user_name_and_messages"])
            users=[]
            massages=[]
            for message in data['user_name_and_messages']:
                mes_user=re.split("([\w\W]+?):\s",message)
                if len(mes_user) >1 :
                    users.append((mes_user[1][2:]).strip())
                    massages.append(mes_user[2][:-1])
                else:
                    users.append('Notification')
                    massages.append(mes_user[0][2:-1])
            data['users'] =users
            data['messages']=massages
            data.drop(columns=['user_name_and_messages'],inplace=True)
            data['date']=pd.to_datetime(data['date'])
            data['hour'] =data['date'].dt.hour
            data['month_name'] =data["date"].dt.month_name()
            data['day'] =data['date'].dt.day
            data['day_name']=data['date'].dt.day_name()
            
            return data
class Whatdata:
    def __init__(self,data, user=None):
        if user==None:
           self.data =data
        else:
            self.data=data[data['users']==user]
    def most_mess_by(self):
        data=self.data
        return data['users'].value_counts()
    def most_chat(self,str='D'):
             data=self.data
             if str== "M":
                return data.groupby("month_name").count()['messages']
             elif str =='D':
                return data.groupby("day_name").count()['messages']
             elif str =="H":
                return data.groupby("hour").count()['messages']
    def l_m_count(self):
        s=' '.join(self.data[self.data['users']!="Notification"]['messages'].tolist())
        links=re.findall(r'(https?://\S+)', s)
        medias=re.findall(r'<Media omitted>', s)
        emlist=[ em["emoji"][0] for em in emoji.emoji_list(s) ]
        return links,medias,emlist,s
    def list_clean_word(self):
        f = open('./stop_hinglish.txt','r')
        x,y,z,s=self.l_m_count()
        stopwords=f.read()
        orgtext=[]
        wolinks = re.sub(r'(https?://\S+)',' ',s)
        womedia=re.sub(r'<Media omitted>','',wolinks)
        woemoji=emoji.replace_emoji(womedia,'')
        for word in woemoji.split():
            if len(word)<=3:
                continue
            elif word in stopwords:
                continue
            else:
                orgtext.append(word.lower())
        f.close()
        return orgtext
    def mos_com_word_emoji(self):
        x,y,emoji,s=self.l_m_count()
        most_common_word=Counter(self.list_clean_word()).most_common() 
        most_common_emoji= Counter(emoji).most_common() 
        return most_common_word,most_common_emoji
    def heatmap_data(self,str="D"):
        if str =='D':
            heat_day_data=pd.pivot_table(self.data,index="day_name",columns='hour',values='messages',aggfunc ='count').fillna(0)
        else:
            heat_day_data=pd.pivot_table(self.data,index="month_name",columns='hour',values='messages',aggfunc ='count').fillna(0)
        
        return heat_day_data
