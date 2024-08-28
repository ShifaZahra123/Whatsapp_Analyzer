from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_start(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users']==selected_user]

    num_massages = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_del_messages = df[df['messages'] == 'This message was deleted '].shape[0]

    num_medias = df[df['messages'] == '<Media omitted> '].shape[0]

    extractor = URLExtract()
    url = []
    for message in df['messages']:
        url.extend(extractor.find_urls(message))

    return df, num_massages, len(words),num_del_messages, num_medias, len(url)


def most_busy_users(df):
    x = df['users'].value_counts().head()
    new_df = round(df['users'].value_counts().head()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x, new_df

def generate_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]

    wc = WordCloud(height=500, width=500, min_font_size=10, background_color='white')
    wc_df = wc.generate(df['messages'].str.cat(sep=" "))
    return wc_df


def most_common_words(selected_user, df):

    f = open("Stop_words.txt",'r')      #provide some stop word containing file
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['users']==selected_user]

    temp = df[df['messages'] != 'group_notification ']
    temp = temp[temp['messages'] != '<Media Omitted> ']

    words=[]
    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_word_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_word_df


def common_emojis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline



def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline


def week_activity(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    return df.pivot_table(index = "day_name", columns="period", values="messages", aggfunc="count").fillna(0)