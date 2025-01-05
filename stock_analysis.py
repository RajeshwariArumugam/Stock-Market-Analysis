import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data Function
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

# Calculate Daily Returns
@st.cache_data
def calculate_daily_returns(data):
    data['daily_return'] = data.groupby('ticker')['close'].pct_change()
    return data

# Calculate Cumulative Returns
@st.cache_data
def calculate_cumulative_returns(data):
    data['cumulative_return'] = (1 + data['daily_return']).groupby(data['ticker']).cumprod()
    return data

# Calculate Yearly Returns
@st.cache_data
def calculate_yearly_returns(data):
    """Calculate yearly returns for each stock."""
    # Ensure data is sorted by date for each ticker
    data = data.sort_values(by=['ticker', 'date'])

    # Calculate yearly return: (last_close - first_close) / first_close
    data['yearly_return'] = data.groupby('ticker')['close'].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0])

    # Drop any NaN values that might have been introduced due to missing data
    data = data.dropna(subset=['yearly_return'])

    return data

# Streamlit app
import streamlit as st
import requests
import json

# Function to load Lottie animations
def load_lottie_local(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)

# Streamlit App Configuration
st.set_page_config(page_title="StockScape Explorer", layout="wide")
st.title("📈 StockScape Explorer")
st.markdown("""
    <style>
        .css-1d391kg {  /* Sidebar container */
            display: none;
        }
        .css-18e3th9 { /* Main container */
            padding-top: 50px;
        }
        .top-right {
            position: absolute;
            top: 20px;
            right: 20px;
        }
        .top-right select {
            background-color: #f1f1f1;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)
# Sidebar Menu
st.sidebar.header("Navigate")

menu = ["Home", "Stock Analysis!"]
choice = st.sidebar.radio("Choose a page:", menu)

# Lottie local
lottie_animation = load_lottie_local(r"C:\Users\Raji\Downloads\Animation - 1736013810429.json")

if choice == "Home":
    # Home Page with Animation
    st.header("Welcome to StockScape Explorer! 📊")
    st.subheader("Discover, Analyze, and Track Stocks in Real-Time")
    # Two-column layout for text and animation
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(""" 
        ### Why You'll Love StockScape Explorer:
        - 📈 Analyze stock market trends.
        - 🔍 Track individual stock performance.
        - 💡 Make informed investment decisions with real-time data.
        
        Get started by navigating through the sidebar. Whether you're a seasoned investor or new to the stock market, StockScape Explorer is the perfect tool to track and analyze stocks! 🚀
        """)
    with col2:
        from streamlit_lottie import st_lottie
        st_lottie(lottie_animation, height=300, key="welcome_animation")

    st.markdown("---")
    st.info("📊 **Tip:** Use the 'Explore!' tab to dive into stock performance analysis and find trends.")

elif choice == "Stock Analysis!":
    st.title("Stock Data Analysis and Visualization")
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload Stock Data CSV", type="csv")
    if uploaded_file is not None:
        # Load data
        data = load_data(uploaded_file)
        data.columns = data.columns.str.lower()  # Normalize column names to lowercase

        # Display file preview
        st.write("Uploaded file preview:")
        st.dataframe(data.head())

        # Check required columns
        required_columns = {'ticker', 'close', 'date'}
        if not required_columns.issubset(data.columns):
            st.error(f"The uploaded file must contain the following columns: {required_columns}")
            st.stop()

        # Convert date column to datetime
        data['date'] = pd.to_datetime(data['date'])

        # Calculate yearly returns
        data = calculate_yearly_returns(data)

        # Analysis and Visualizations
        st.header("Data Analysis")

        ## 1. Top 10 Green and Loss Stocks
        st.subheader("Top 10 Green and Loss Stocks")
        # Calculate average yearly return for each ticker
        green_stocks = data.groupby('ticker')['yearly_return'].mean().nlargest(10)
        loss_stocks = data.groupby('ticker')['yearly_return'].mean().nsmallest(10)
    
        # Display Top 10 Green and Loss Stocks
        st.write("Top 10 Green Stocks:")
        st.dataframe(green_stocks)
        st.write("Top 10 Loss Stocks:")
        st.dataframe(loss_stocks)

        ## 2. Market Summary
        st.subheader("Market Summary")
        green_count = len(data[data['yearly_return'] > 0])
        red_count = len(data[data['yearly_return'] <= 0])
        avg_price = data['close'].mean()
        avg_volume = data['volume'].mean() if 'volume' in data.columns else None

        st.metric("Green Stocks", green_count)
        st.metric("Red Stocks", red_count)
        st.metric("Average Price", f"${avg_price:.2f}")
        if avg_volume is not None:
            st.metric("Average Volume", f"{avg_volume:,.0f}")

        ## 3. Volatility Analysis
        st.subheader("Volatility Analysis")
        data = calculate_daily_returns(data)
        volatility = data.groupby('ticker')['daily_return'].std().nlargest(10)
        st.bar_chart(volatility)

        ## 4. Cumulative Return Over Time
        st.subheader("Cumulative Return Over Time")
        data = calculate_cumulative_returns(data)
        top_performing_stocks = data.groupby('ticker')['cumulative_return'].max().nlargest(5).index
        for ticker in top_performing_stocks:
            stock_data = data[data['ticker'] == ticker]
            plt.plot(stock_data['date'], stock_data['cumulative_return'], label=ticker)
        plt.title("Top 5 Performing Stocks - Cumulative Returns")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.legend()
        st.pyplot(plt)

        # Sector-wise Performance
        st.subheader("Sector-wise Performance")
        sector_file = st.file_uploader("Upload Sector Mapping CSV", type="csv")
        if sector_file is not None:
            # Load sector data
            sector_data = pd.read_csv(sector_file)

            # Normalize column names to lowercase for consistency
            sector_data.columns = sector_data.columns.str.lower()

            # Display sector data preview
            st.write("Sector Mapping Preview:")
            st.dataframe(sector_data.head())

            # Check if sector data contains required columns
            required_sector_columns = {'company', 'sector', 'symbol'}
            if not required_sector_columns.issubset(sector_data.columns):
                st.error(f"Sector mapping file must contain the following columns: {required_sector_columns}")
                st.stop()

                # Rename columns for merging purposes
                sector_data = sector_data.rename(columns={'company': 'ticker', 'symbol': 'ticker'})

            # Merge sector data with stock data
                merged_data = data.merge(sector_data[['ticker', 'sector']], on='ticker', how='left')

            # Check if merge was successful
                st.write("Merged Data Preview:")
                st.dataframe(merged_data.head())

            # Calculate average yearly return per sector
                sector_performance = merged_data.groupby('sector')['yearly_return'].mean().dropna()

            # Display sector performance
                st.bar_chart(sector_performance)


    ## 6. Stock Price Correlation
        st.subheader("Stock Price Correlation")
        correlation_matrix = data.pivot_table(values='close', index='date', columns='ticker').corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm")
        plt.title("Stock Price Correlation Heatmap")
        st.pyplot(plt)

    else:   
        st.info("Please upload a CSV file to proceed.")
