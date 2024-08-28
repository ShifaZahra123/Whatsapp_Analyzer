import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# configuring the page
st.set_page_config(
    page_title="Chat-Mine",
    layout="wide",
    initial_sidebar_state="expanded",
)


# find and read styles file
styles_file_path = Path(__file__).parent/'styles.css'
with open(styles_file_path, 'r') as f:
    st.write(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# App elements starts from here

st.sidebar.write('<div class="title">Chat-Mine</div>', unsafe_allow_html=True)
st.write('<div class="title">Welcome to Chat-Mine!</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    # To recive uploaded data
    bytes_data = uploaded_file.getvalue()

    try:
        data = bytes_data.decode('utf-8')

        # preprocessing data, making data frame
        df = preprocessor.preprocess(data)

        # Fetch unique user names and arrange them to show in the select box
        user_list = df['users'].unique().tolist()

# Convert everything to lowercase for a case-insensitive check
        user_list_lower = [user.lower() for user in user_list]

# Check if "group_notification" exists in the list before trying to remove it
        if "group_notification" in user_list_lower:
            user_list.pop(user_list_lower.index("group_notification"))

        user_list.sort()
        user_list.insert(0, "Overall")

        # sidebar element, chose user name
        selected_user = st.sidebar.selectbox("Choose User", user_list)


        # After clicking "Show Analysis" button
        if st.sidebar.button("Show Analysis"):
            df, num_massages, num_words, num_del_messages, num_medias, num_url = helper.fetch_start(selected_user, df)

            st.header("Statistics")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                # st.header("Total Messages")
                # st.title(num_massages)
                st.metric("Total Messages", num_massages)

            with col2:
                # st.header("Total Words")
                # st.title(num_words)
                st.metric("Total Words", num_words)

            with col3:
                # st.header("Deleted Messages")
                # st.title(num_del_messages)
                st.metric("Deleted Messages", num_del_messages)

            with col4:
                # st.header("Media Shared")
                # st.title(num_medias)
                st.metric("Media Shared", num_medias)

            with col5:
                # st.header("URL Shared")
                # st.title(num_url)
                st.metric("URL Shared", num_url)

            st.header("Timelines")
            col1, col2 = st.columns(2)
            with col1:
                # monthly timeline
                st.subheader("Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['messages'])
                plt.xticks(rotation="vertical")
                st.pyplot(fig)


            with col2:
                # daily timeline
                st.subheader("Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['messages'])
                plt.xticks(rotation="vertical")
                st.pyplot(fig)



            # week activity map
            st.header("Activity Map")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Most Busy Days")
                busy_day = helper.week_activity(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.subheader("Most Busy Months")
                busy_month = helper.month_activity(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            # activity heatmap
            st.header("Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

            # showing Busy users in a group, valid only for group/overall
            if selected_user == 'Overall' :
                st.header("Most Busy Users")
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)
                with col1:
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2 :
                    st.dataframe(new_df)

            # word analysis
            st.header("Word Analysis")
            # col1, col2 = st.columns(2)
            # with col1:
            #     # wordcloud
            #     st.subheader("Wordcloud")
            #     wc_df = helper.generate_wordcloud(selected_user, df)
            #     fig, ax = plt.subplots()
            #     ax.imshow(wc_df)
            #     st.pyplot(fig)
            # with col2:
            #     # most common words
            #     st.subheader("Most Common Words")
            #     most_common_word_df = helper.most_common_words(selected_user, df)
            #     fig, ax = plt.subplots()
            #     ax.barh(most_common_word_df[0], most_common_word_df[1])
            #     plt.xticks(rotation='vertical')
            #     st.pyplot(fig)

            # wordcloud analysis
            st.subheader("Wordcloud")
            wc_df = helper.generate_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(wc_df)
            st.pyplot(fig)

            st.subheader("Most Common Words")
            most_common_word_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_word_df[0], most_common_word_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


            #emoji analysis
            st.title("Emoji Analysis")
            emoji_df = helper.common_emojis(selected_user,df)
            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%.2f")
                st.pyplot(fig)

            with col2:
                emoji_df = emoji_df.rename(columns={0:'emoji', 1:'counts'})
                st.dataframe(emoji_df)
            st.title("Thank You ! ")

        else:
            st.markdown('''You forgot to hit the "Show analysis" button ✌️ or Data Processing...😀''')

    except Exception as e:
            st.markdown(f"An error occurred: {e}")



else:
    st.subheader("Steps : ")
    st.markdown("1. Goto sidebar & Upload .txt file (whatsapp chat exported file)")
    st.markdown('''2. Choose user and hit the "show analysis" button''')




