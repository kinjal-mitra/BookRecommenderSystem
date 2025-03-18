import streamlit as st
import pickle
import numpy as np

# Load pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Streamlit app
def main():
    st.title("Book Recommendation System")
    menu = ["Home", "Recommend"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Popular Books")
        cols = st.columns(3)
        for i in range(len(popular_df)):
            with cols[i % 3]:
                st.image(popular_df['Image-URL-M'].iloc[i], width=100)
                st.write(f"**{popular_df['Book-Title'].iloc[i]}** by {popular_df['Book-Author'].iloc[i]}")
                st.write(f"⭐ {popular_df['avg_rating'].iloc[i]} ({popular_df['num_ratings'].iloc[i]} votes)")
                st.write("---")
    
    elif choice == "Recommend":
        st.subheader("Find Books Similar to Your Favorite")
        user_input = st.text_input("Enter a book name:")
        if st.button("Recommend"):
            if user_input in pt.index:
                index = np.where(pt.index == user_input)[0][0]
                similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
                
                st.write("### Recommended Books:")
                cols = st.columns(3)
                for idx, i in enumerate(similar_items):
                    temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
                    title = temp_df['Book-Title'].values[0]
                    author = temp_df['Book-Author'].values[0]
                    image = temp_df['Image-URL-M'].values[0]
                    
                    with cols[idx % 3]:
                        st.image(image, width=100)
                        st.write(f"**{title}** by {author}")
                        st.write("---")
            else:
                st.error("Book not found in database. Please try another title.")

if __name__ == "__main__":
    main()
