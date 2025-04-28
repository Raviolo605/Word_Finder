import streamlit as st
import re
import unicodedata

def normalize_text(text):
    """Normalize text by removing accents and non-alphanumeric characters, then converting to lowercase."""
    text_wo_acc = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_wo_acc)
    return clean_text.lower()

def match_group(chunk, group, mode="AND"):
    """Match a group of words in the chunk using AND or OR logic."""
    if not group:
        return True  # If the group is empty, treat as always True
    normalized_chunk = normalize_text(chunk)
    if mode == "AND":
        return all(any(normalize_text(word) in normalized_chunk for word in alternatives) for alternatives in group)
    elif mode == "OR":
        return any(any(normalize_text(word) in normalized_chunk for word in alternatives) for alternatives in group)
    else:
        raise ValueError("Mode must be 'AND' or 'OR'")

def file_watcher(filename, groups, lines_to_join=1, mode="AND"):
    """Watch a file and return chunks matching the specified word groups."""
    try:
        with open(filename, "r", encoding="utf-8") as f1:
            lines = f1.readlines()
            results = []
            for i in range(len(lines)):
                chunk = ''.join(lines[i:i+lines_to_join])
                if match_group(chunk, groups, mode):
                    results.append(chunk)
            return results
    except FileNotFoundError:
        return ["File not found!"]

# --- Streamlit App ---

st.title("Advanced File Watcher")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

st.markdown("### Enter words (use commas `,` to separate synonyms)")
word1 = st.text_input("Group 1 (mandatory)", "")
word2 = st.text_input("Group 2 (optional)", "")
word3 = st.text_input("Group 3 (optional)", "")

lines_to_join = st.slider("Number of lines to join for search", min_value=1, max_value=4, value=1)

search_mode = st.selectbox("Search mode", ["AND", "OR"], help="AND requires all groups to match, OR requires at least one group to match")

if uploaded_file is not None:
    filename = uploaded_file.name
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if word1:
        groups = []
        for w in [word1, word2, word3]:
            if w.strip():
                groups.append([alt.strip() for alt in w.split(",") if alt.strip()])
        
        results = file_watcher(filename, groups, lines_to_join, mode=search_mode)

        if results:
            st.write("### Results found:")
            for result in results:
                st.write(result)
        else:
            st.write("No results found.")
