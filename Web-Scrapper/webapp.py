import streamlit as st
from bot import WebScraperBot
from selenium.webdriver.common.by import By
import time

# Page configuration
st.set_page_config(
    page_title="Web Scraper Bot",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .block-container {f
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }
    textarea, input, select, .stTextInput > div > div > input {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Web Scraper Bot with Sentiment Analysis")
st.markdown("Extract content from websites and analyze their sentiment in real-time")

# Sidebar Configuration
with st.sidebar:
    st.header("Settings")
    headless_mode = st.checkbox("Headless Mode", value=True, help="Run browser in headless mode (faster)")
    
    st.divider()
    st.subheader("Scraping Options")
    scrape_mode = st.radio(
        "Select scraping mode:",
        ["Entire Page", "Specific Elements"]
    )
    
    if scrape_mode == "Specific Elements":
        element_tag = st.selectbox(
            "Element to scrape:",
            ["p", "div", "span", "a", "h1", "h2", "h3", "article", "section", "button"]
        )
    else:
        element_tag = None

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Enter Website URL")
    url = st.text_input("Website URL:", placeholder="https://example.com", label_visibility="collapsed")
    prompt = st.text_area(
        "Prompt / Focus:",
        placeholder="e.g., Show pricing details and refund policy",
        height=80,
    )

if st.button("Scrape & Analyze", use_container_width=True):
    if not url:
        st.error("❌ Please enter a valid URL")
    else:
        try:
            with st.spinner("🔄 Initializing bot..."):
                bot = WebScraperBot(headless=headless_mode)
            
            with st.spinner("📥 Scraping website..."):
                if scrape_mode == "Specific Elements":
                    result = bot.scrape_and_analyze(url, element_tag, By.TAG_NAME, prompt=prompt)
                else:
                    result = bot.scrape_and_analyze(url, prompt=prompt)
                
                bot.close()
            
            if result and result.get("sentiment"):
                # Display Results
                st.success("Scraping completed successfully!")
                
                st.divider()
                
                # Create tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs(["Sentiment Analysis", "Prompt Matches", "Content Preview", "Details"])
                
                with tab1:
                    st.subheader("Sentiment Analysis Results")
                    sentiment = result["sentiment"]
                    
                    # Main sentiment display
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Sentiment",
                            sentiment["sentiment"],
                        )
                    
                    with col2:
                        # Polarity gauge (show neutral strength when classified as Neutral)
                        polarity = sentiment["polarity"]
                        neutral_strength = round(1 - abs(polarity), 3)
                        if sentiment["sentiment"] == "Neutral":
                            display_value = neutral_strength
                            delta_label = "Neutral confidence"
                        else:
                            display_value = polarity
                            delta_label = sentiment["sentiment"]
                        st.metric(
                            "Polarity Score",
                            f"{display_value}",
                            delta=delta_label
                        )
                    
                    with col3:
                        st.metric(
                            "Subjectivity",
                            f"{sentiment['subjectivity']}",
                            delta=f"{'Very Subjective' if sentiment['subjectivity'] > 0.7 else 'Objective' if sentiment['subjectivity'] < 0.3 else 'Mixed'}"
                        )
                    
                    # Visualization
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Polarity Distribution**")
                        polarity_data = {
                            "Sentiment": ["Positive", "Negative", "Neutral"],
                            "Score": [
                                max(0, sentiment["polarity"]),
                                max(0, -sentiment["polarity"]),
                                max(0, 1 - abs(sentiment["polarity"]))
                            ]
                        }
                        st.bar_chart(polarity_data, x="Sentiment", y="Score")
                    
                    with col2:
                        st.write("**Subjectivity Level**")
                        subj_data = {
                            "Type": ["Subjective", "Objective"],
                            "Score": [sentiment["subjectivity"], 1 - sentiment["subjectivity"]]
                        }
                        st.bar_chart(subj_data, x="Type", y="Score")
                
                with tab2:
                    st.subheader("Prompt-Aligned Content")
                    if result.get("prompt_matches"):
                        # Split snippets into individual sentences for better display
                        snippets = result["prompt_matches"].split(". ")
                        
                        st.markdown("### Matched Snippets")
                        for idx, snippet in enumerate(snippets, 1):
                            # Add period back if it was removed by split
                            if not snippet.endswith(".") and idx < len(snippets):
                                snippet = snippet + "."
                            
                            # Create a nice card-like display
                            st.markdown(
                                f"""
                                <div style="background-color: #1e293b; padding: 15px; border-left: 4px solid #38bdf8; margin: 10px 0; border-radius: 5px;">
                                    <p style="margin: 0; font-size: 14px; color: #e2e8f0;">{snippet}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        
                        st.markdown(f"**Total snippets found:** {len(snippets)}")
                    else:
                        st.info("No clear matches for your prompt were found in the scraped content. Try a different prompt.")
                
                with tab3:
                    st.subheader("Scraped Content Preview")
                    st.text_area(
                        "Content Preview:",
                        value=result["content_preview"],
                        height=250,
                        disabled=True
                    )
                
                with tab4:
                    st.subheader("Scraping Details")
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.write("**URL:**", url)
                        st.write("**Content Length:**", f"{result['content_length']} characters")
                    
                    with info_col2:
                        st.write("**Scraping Mode:**", scrape_mode)
                        if scrape_mode == "Specific Elements":
                            st.write("**Element Tag:**", element_tag)
                    
                    st.divider()
                    st.write("**Full Sentiment Data:**")
                    st.json(sentiment)
            else:
                st.error("❌ Failed to scrape the website. Please check the URL and try again.")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Tips:\n- Make sure the URL is accessible\n- Try disabling headless mode\n- Check your internet connection")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    🕷️ Web Scraper Bot with Sentiment Analysis | Powered by Selenium, TextBlob & Streamlit
    </div>
    """, unsafe_allow_html=True)