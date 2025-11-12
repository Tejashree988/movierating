import streamlit as st
import pandas as pd

# --- Streamlit page config ---
st.set_page_config(page_title="Movie Ratings Data Analysis", layout="wide")

st.title("🎬 Movie Ratings Data Analysis")
st.write("Analyze and visualize movie ratings data interactively using Python and Streamlit.")

# --- Sidebar: Upload or use local file ---
st.sidebar.header("📂 Upload or Select Dataset")
uploaded = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
use_local = False
if uploaded is None:
    if st.sidebar.button("Use local movies.csv"):
        use_local = True

@st.cache_data
def load_data(uploaded_file, use_local_flag):
    """Load CSV data from upload or local file"""
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
            return None
    if use_local_flag:
        try:
            return pd.read_csv("movies.csv")
        except FileNotFoundError:
            st.error("movies.csv not found in app folder. Upload a CSV instead.")
            return None
    return None

df = load_data(uploaded, use_local)

# --- Check dataset loaded ---
if df is None:
    st.info("Upload a CSV with columns like: MovieID, Title, Genre, UserID, Rating, Year.\nOr click 'Use local movies.csv' in the sidebar.")
    st.stop()

# --- Show dataset preview ---
st.subheader("📊 Dataset Preview")
st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
st.dataframe(df.head(10))

# --- Normalize column names ---
cols_lower = {c.lower(): c for c in df.columns}
required = ["title", "genre", "rating"]
missing = [r for r in required if r not in cols_lower]
if missing:
    st.error(f"Missing required columns (case-insensitive): {missing}")
    st.stop()

title_col = cols_lower["title"]
genre_col = cols_lower["genre"]
rating_col = cols_lower["rating"]

# Convert rating to numeric
df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
df = df.dropna(subset=[rating_col])

# --- Sidebar filters ---
st.sidebar.header("⚙️ Settings")
min_ratings = st.sidebar.slider("Minimum ratings to include a movie in Top List", 1, 5, 2)

# --- Data Analysis ---
avg_ratings = df.groupby(title_col)[rating_col].mean().sort_values(ascending=False)
counts = df.groupby(title_col).size().sort_values(ascending=False)
genre_avg = df.groupby(genre_col)[rating_col].mean().sort_values(ascending=False)
genre_count = df[genre_col].value_counts()

movie_stats = pd.DataFrame({
    "Average Rating": avg_ratings,
    "Total Ratings": counts
}).sort_values(["Average Rating", "Total Ratings"], ascending=[False, False])

# --- Display Results ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Movies by Average Rating")
    top_movies = movie_stats[movie_stats["Total Ratings"] >= min_ratings].head(10)
    st.dataframe(top_movies)

with col2:
    st.subheader("🎭 Genre Analysis")
    st.write("**Average Rating by Genre**")
    st.bar_chart(genre_avg)
    st.write("**Number of Ratings by Genre**")
    st.bar_chart(genre_count)

# --- Drill-down Analysis ---
st.subheader("🔍 Movie Rating Distribution")
selected_movie = st.selectbox("Choose a movie to view rating distribution", movie_stats.index.tolist())
if selected_movie:
    movie_data = df[df[title_col] == selected_movie]
    st.write(f"Ratings for **{selected_movie}**")
    st.bar_chart(movie_data[rating_col].value_counts().sort_index())

# --- Download Buttons (Fixed) ---
st.subheader("📥 Download Results")
csv_movies = movie_stats.to_csv().encode('utf-8')
st.download_button("Download Movie Stats (CSV)", data=csv_movies, file_name="movie_stats.csv", mime="text/csv")

csv_genre = genre_avg.to_csv().encode('utf-8')
st.download_button("Download Genre Averages (CSV)", data=csv_genre, file_name="genre_avg.csv", mime="text/csv")

# --- Footer ---
st.markdown("---")
st.caption("Developed by Tejashree | Built with ❤️ using Streamlit & Pandas")

