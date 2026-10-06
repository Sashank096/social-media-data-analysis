import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Page settings
st.set_page_config(
    page_title="Social Media Data Analysis",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("📊 Dashboard Menu")

menu = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Sentiment Analysis",
        "Engagement Analysis",
        "Trending Keywords",
        "Analyzed Data"
    ]
)

st.title("📊 Social Media Data Analysis System")
st.write("Analyze social media posts using Python and NLP.")

# Upload Dataset
uploaded_file = st.file_uploader(
    "Upload Social Media CSV Dataset",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("social_media_data.csv")

# Clean Data
data = data.loc[:, ~data.columns.str.startswith("Unnamed")]
data = data.dropna()
data = data.drop_duplicates()

# Sentiment Function
def get_sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Create Sentiment Column
data["Sentiment"] = data["Text"].apply(get_sentiment)

# Total Engagement
data["Total Engagement"] = (
    data["Likes"] +
    data["Comments"] +
    data["Shares"]
)

# Convert Date
data["Date"] = pd.to_datetime(data["Date"])


# ==================================================
# DASHBOARD
# ==================================================

if menu == "Dashboard":

    st.subheader("📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Posts", len(data))
    col2.metric("Total Likes", int(data["Likes"].sum()))
    col3.metric("Total Comments", int(data["Comments"].sum()))
    col4.metric("Total Shares", int(data["Shares"].sum()))

    st.divider()

    # Quick Insights
    st.subheader("💡 Quick Insights")

    positive_posts = len(
        data[data["Sentiment"] == "Positive"]
    )

    negative_posts = len(
        data[data["Sentiment"] == "Negative"]
    )

    neutral_posts = len(
        data[data["Sentiment"] == "Neutral"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("😊 Positive Posts", positive_posts)
    col2.metric("😞 Negative Posts", negative_posts)
    col3.metric("😐 Neutral Posts", neutral_posts)
    # Sentiment Percentages
    st.subheader("📊 Sentiment Percentage")

    total_posts = len(data)

    positive_percentage = (positive_posts / total_posts) * 100
    negative_percentage = (negative_posts / total_posts) * 100
    neutral_percentage = (neutral_posts / total_posts) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric(
    "😊 Positive %",
        f"{positive_percentage:.1f}%"
    )

    col2.metric(
        "😞 Negative %",
        f"{negative_percentage:.1f}%"
    )

    col3.metric(
        "😐 Neutral %",
        f"{neutral_percentage:.1f}%"
    )

    st.divider()

    # Negative Feedback
    st.subheader("🚨 Negative Feedback")

    negative_data = data[
        data["Sentiment"] == "Negative"
    ]

    if len(negative_data) > 0:
        st.dataframe(
            negative_data[
                [
                    "Post_ID",
                    "Text",
                    "Likes",
                    "Comments",
                    "Shares",
                    "Sentiment"
                ]
            ]
        )
    else:
        st.success("🎉 No negative feedback found!")

    # Most Engaging Post
    st.subheader("🏆 Most Engaging Post")

    most_engaging = data.loc[
        data["Total Engagement"].idxmax()
    ]

    st.write(
        "**Post:**",
        most_engaging["Text"]
    )

    st.write(
        "**Total Engagement:**",
        int(most_engaging["Total Engagement"])
    )

    # Top Performing Posts
    st.subheader("📈 Top Performing Posts")

    top_posts = data.sort_values(
        by="Total Engagement",
        ascending=False
    ).head(5)

    st.dataframe(
        top_posts[
            [
                "Post_ID",
                "Text",
                "Likes",
                "Comments",
                "Shares",
                "Total Engagement"
            ]
        ]
    )





# ==================================================
# SENTIMENT ANALYSIS
# ==================================================

elif menu == "Sentiment Analysis":

    st.subheader("😊 Sentiment Analysis")

    sentiment_counts = data["Sentiment"].value_counts()

    # Bar Chart
    fig, ax = plt.subplots()

    sentiment_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Posts")
    ax.set_title("Sentiment Distribution")

    st.pyplot(fig)
    import matplotlib.pyplot as plt

    st.subheader("🥧 Sentiment Distribution")

    sentiment_counts = data["Sentiment"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
    sentiment_counts.values,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    startangle=90
    )

    ax.set_title("Sentiment Distribution")

    st.pyplot(fig)

    # Pie Chart
    st.subheader("🥧 Sentiment Pie Chart")

    fig_pie, ax_pie = plt.subplots()

    ax_pie.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax_pie.set_title(
        "Sentiment Distribution - Pie Chart"
    )

    st.pyplot(fig_pie)

    # Sentiment Filter
    st.subheader("🔍 Filter Posts by Sentiment")

    selected_sentiment = st.selectbox(
        "Select Sentiment",
        [
            "All",
            "Positive",
            "Negative",
            "Neutral"
        ]
    )

    if selected_sentiment == "All":
        filtered_data = data.copy()
    else:
        filtered_data = data[
            data["Sentiment"] == selected_sentiment
        ]

    st.write(
        "Number of Posts:",
        len(filtered_data)
    )

    st.dataframe(
        filtered_data[
            [
                "Post_ID",
                "Text",
                "Likes",
                "Comments",
                "Shares",
                "Sentiment"
            ]
        ]
    )


# ==================================================
# ENGAGEMENT ANALYSIS
# ==================================================

elif menu == "Engagement Analysis":

    st.subheader("📈 Engagement Analysis")

    # Engagement Summary
    avg_likes = data["Likes"].mean()
    avg_comments = data["Comments"].mean()
    avg_shares = data["Shares"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Likes",
        f"{avg_likes:.1f}"
    )

    col2.metric(
        "Average Comments",
        f"{avg_comments:.1f}"
    )

    col3.metric(
        "Average Shares",
        f"{avg_shares:.1f}"
    )

    # Engagement Chart
    engagement = {
        "Likes": data["Likes"].sum(),
        "Comments": data["Comments"].sum(),
        "Shares": data["Shares"].sum()
    }

    fig2, ax2 = plt.subplots()

    ax2.bar(
        engagement.keys(),
        engagement.values()
    )

    ax2.set_xlabel("Engagement Type")
    ax2.set_ylabel("Count")
    ax2.set_title("Social Media Engagement")

    st.pyplot(fig2)

    # Date-wise Analysis
    st.subheader("📅 Date-wise Engagement Analysis")

    date_engagement = data.groupby(
        "Date"
    )[["Likes", "Comments", "Shares"]].sum()

    st.line_chart(date_engagement)

    # Most Engaging Post
    st.subheader("🏆 Most Engaging Post")

    most_engaging = data.loc[
        data["Total Engagement"].idxmax()
    ]

    st.write(
        "**Post:**",
        most_engaging["Text"]
    )

    st.write(
        "**Likes:**",
        int(most_engaging["Likes"])
    )

    st.write(
        "**Comments:**",
        int(most_engaging["Comments"])
    )

    st.write(
        "**Shares:**",
        int(most_engaging["Shares"])
    )

    st.write(
        "**Total Engagement:**",
        int(most_engaging["Total Engagement"])
    )

    # Top Performing Posts
    st.subheader("📈 Top Performing Posts")

    top_posts = data.sort_values(
        by="Total Engagement",
        ascending=False
    ).head(5)

    st.dataframe(
        top_posts[
            [
                "Post_ID",
                "Text",
                "Likes",
                "Comments",
                "Shares",
                "Total Engagement"
            ]
        ]
    )


# ==================================================
# TRENDING KEYWORDS
# ==================================================

elif menu == "Trending Keywords":

    st.subheader("🔥 Trending Keywords")

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    from collections import Counter
    import re

    # Combine all post text
    text = " ".join(data["Text"].astype(str))

    # Remove special characters
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

    # Common words to ignore
    stop_words = {
        "the", "and", "this", "that", "with",
        "for", "are", "was", "you", "our",
        "has", "have", "very", "from"
    }

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    # Count keywords
    word_counts = Counter(filtered_words)

    st.subheader("📌 Most Used Keywords")

    top_words = word_counts.most_common(10)

    for word, count in top_words:
        st.write(f"**{word}** — {count} times")

    st.divider()

    # Word Cloud
    st.subheader("☁️ Word Cloud")

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(" ".join(filtered_words))

    fig, ax = plt.subplots()

    ax.imshow(
        wordcloud,
        interpolation="bilinear"
    )

    ax.axis("off")

    st.pyplot(fig)

# ==================================================
# ANALYZED DATA
# ==================================================

elif menu == "Analyzed Data":

    # Search
    st.subheader("🔎 Search Posts")

    search_text = st.text_input(
        "Enter Post ID or keyword from the post"
    )

    if search_text:

        search_results = data[
            data["Post_ID"].astype(str).str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            data["Text"].astype(str).str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        st.write(
            "Search Results:",
            len(search_results)
        )

        st.dataframe(
            search_results[
                [
                    "Post_ID",
                    "Text",
                    "Likes",
                    "Comments",
                    "Shares",
                    "Sentiment"
                ]
            ]
        )

    # Download CSV
    st.subheader("📥 Download Analyzed Data")

    csv_data = data.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="analyzed_social_media_data.csv",
        mime="text/csv"
    )

    # Complete Data
    st.subheader("📋 Analyzed Data")

    st.dataframe(data)
