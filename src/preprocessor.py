import re
import pandas as pd


def preprocess(data) :
    
    pattern = "\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s\S\S"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # modifing 12 hours time to 24 hours time 
    for i in range(len(dates)) :
        if dates[i][-2:] == 'pm' and dates[i][dates[i].find(' ')+1:dates[i].find(':')] != '12':
            perfect_time = str(int(dates[i][dates[i].find(' ')+1:dates[i].find(':')]) + 12)
            dates[i] = dates[i][:10] + perfect_time + dates[i][dates[i].find(':'):]
        elif dates[i][-2:] == 'am' and dates[i][dates[i].find(' ')+1:dates[i].find(':')] == '12' :
            perfect_time = '00'
            dates[i] = dates[i][:10] + perfect_time + dates[i][dates[i].find(':'):]


    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    df['user_message'] = df['user_message'].str.replace('\n', ' ')

    # convert the message_date as date time format
    df['message_date'] = pd.to_datetime(df['message_date'],format='%d/%m/%y, %H:%M %p')

    # seperate user and massage
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else :
            users.append('Group_notifications')
            messages.append(entry[0])
            
    df['users'] = users
    df['messages'] = messages
    df.drop(columns = ['user_message'], inplace = True)


    # extracting date, time, etc.
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minutes'] = df['message_date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(00))
        elif hour == 0:
            period.append( str(00) + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df
