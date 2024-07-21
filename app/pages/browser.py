import streamlit as st
from config import config
st.set_page_config(page_title="Document Browser")

docs = [
    {
        "_id": 0,
        "title": "Title1",
        "source": "example.com",
        "text": """# Title1
        bla bla bla"""
    },
    {
        "_id": 1,
        "title": "Title2",
        "source": "example.com",
        "text": """# Title2
        bla bla something something
        [link somewhere](http://example.com)"""
    }
]

sources = [doc["source"] for doc in docs]

st.markdown("# Document Browser")
st.sidebar.header("Document Browser")

st.multiselect("Source", sources)

for doc in docs:
    with st.container():
        col1, col2, col3 = st.columns([2,2,1])
        col1.write(doc["title"])
        col2.write(doc["source"])
        if col3.button("View", key=str(doc["_id"])):
            print("view ", doc["_id"])