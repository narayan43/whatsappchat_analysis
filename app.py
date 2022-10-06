from turtle import width
import streamlit as st
import matplotlib.pyplot as plt
import  plotly.graph_objects as go 
from plotly.subplots import make_subplots
from wordcloud import WordCloud, STOPWORDS

from  functions import Creat_Data_Frame , Whatdata
uploaded_file=st.sidebar.file_uploader("Choose WhatApp txt file")
if uploaded_file is not None:
    text_data=uploaded_file.getvalue()
    text_data=text_data.decode('utf-8')
#    st.write(text_data)
    data=Creat_Data_Frame(text_data)
    anal=Whatdata(data.dataframe())
        # site bar
    userlist=list(anal.most_mess_by().index)
    userlist.remove("Notification")
    userlist.insert(0,"OverAll")
    option = st.sidebar.selectbox(
        'Sellect user',
        userlist)



    # create dataframe
    if option =="OverAll":
        anal=Whatdata(data.dataframe())
    else:
        anal=Whatdata(data.dataframe(),user=option)
    # show stats data


    # stats of user 
    st.title(f"{option} Stats")
    links,media,emoji,string=anal.l_m_count()
    st.header(f'Total messages: {anal.most_mess_by().sum()}')
    st.header(f'Total links: {len(links)}')
    st.header(f'Total media files: {len(media)}')
    st.header(f'Total emoji: {len(emoji)}')
    # graph of most mess by user
    st.header("Most busy users in the group graph")
    most_message=anal.most_mess_by()
    fig =make_subplots(cols=1, rows =1)
    fig.add_trace(go.Bar(
        x=most_message.index,y=most_message.values
    ,marker = {'color' : 'red'}))
    fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)
    # busy time in the group
    st.header("Most busy Time in the group graph")
    dic={"Hour wise most chats":'H' ,"Month wise most chats":'M',"Day wise most chats":'D'}
    chatoptions=st.selectbox("Sellect Distributions",dic.keys())
    chart = st.radio(
    "Sellect chart",
    ( 'Line chart','Pie chart'))
    mchatdata=anal.most_chat(str=dic[chatoptions])
    if chart=='Line chart':
        fig =make_subplots(cols=1, rows =1)
        fig.add_trace(go.Line(x=mchatdata.index,y=mchatdata.values,marker = {'color' : 'blue'}))
        fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    if chart=='Pie chart':
        fig =make_subplots(cols=1, rows =1)
        fig.add_trace(go.Pie(labels=mchatdata.index,values=mchatdata.values))
        fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    # most common words
    st.header("Most Common words Typed in group")
    mostCom_word,mostCom_emoji=anal.mos_com_word_emoji()
    mcw=[x for x,y in mostCom_word]
    mcwf=[y for x,y in mostCom_word]
    if len(mcw) >100:
        fig =make_subplots(cols=1, rows =1)
        fig.add_trace(go.Bar(
            x=mcw[:100],y=mcwf[:100]
        ,marker = {'color' : '#801A86'}))
        fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig =make_subplots(cols=1, rows =1)
        fig.add_trace(go.Bar(
            x=mcw,y=mcwf
        ,marker = {'color' : '#801A86'}))
        fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    st.header("Most Common EMOJI Typed in group")
    mce=[x for x,y in mostCom_emoji]
    mcef=[y for x,y in mostCom_emoji]
    echart = st.radio(
    "Sellect chart",
    ( 'Bar Chart','Pie chart'))
    if echart =="Bar Chart":
        if len(mce) >100:
            fig =make_subplots(cols=1, rows =1)
            fig.add_trace(go.Bar(
                x=mce[:100],y=mcef[:100]
            ,marker = {'color' : '#CE2D4F'}))
            fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig =make_subplots(cols=1, rows =1)
            fig.add_trace(go.Bar(
                x=mce,y=mcef
            ,marker = {'color' : '#CE2D4F'}))
            fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
    if echart=='Pie chart':
        if len(mce) >20:
            fig =make_subplots(cols=1, rows =1)
            fig.add_trace(go.Pie(
                labels=mce[:20],values=mcef[:20]
            ))
            fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig =make_subplots(cols=1, rows =1)
            fig.add_trace(go.Pie(
                labels=mce,values=mcef
            ))
            fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
    # word cloud 
    st.header("WordCloud Of Most common words")

    wordcloud = WordCloud(width = 500, height = 400,
                background_color ='white',
                min_font_size = 10).generate(' '.join(anal.list_clean_word()))
        
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    # heatmap for busy users
    st.header("HeatMap on Hour wise most messages")
    dic={"Month wise HeatMap":'M',"Day wise HearMap":'D'}
    heatmap_options=st.selectbox("Sellect Heatmap",dic.keys())
    if heatmap_options=="Day wise HearMap":
        data=anal.heatmap_data()
        fig =make_subplots(cols=1, rows =1)
        fig.add_trace(go.Heatmap(z=data.to_numpy(),y=data.index,x=data.columns,name=heatmap_options))
        fig.update_traces(
        hovertemplate="<br>".join([
        "Hour: %{x}",
        "Day: %{y}",
        "Messages: %{z}"]))
        fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    if heatmap_options=="Month wise HeatMap":
        data=anal.heatmap_data(str="M")
        fig =make_subplots(cols=1, rows =1,)
        fig.add_trace(go.Heatmap(z=data.to_numpy(),y=data.index,x=data.columns,name=heatmap_options))
        fig.update_traces(
        hovertemplate="<br>".join([
        "Hour: %{x}",
        "Month: %{y}",
        "Messages: %{z}"]))
        fig.update_layout(autosize=False,width=1000,height=500,margin=dict(l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("File is not a uploaded")