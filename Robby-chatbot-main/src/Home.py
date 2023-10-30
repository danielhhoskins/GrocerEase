import streamlit as st


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="GrocerEase | Chat-Bot 🤖")


#Contact
with st.sidebar.expander("Options"):

    st.write("**GitHub:**",
"[yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)")

    st.write("**Medium:** "
"[@yvann-hub](https://medium.com/@yvann-hub)")

    st.write("**Twitter:** [@yvann_hub](https://twitter.com/yvann_hub)")
    st.write("**Mail** : barbot.yvann@gmail.com")
    st.write("**Created by Yvann**")


#Title
st.markdown(
    """
    <h2 style='text-align: center;'>GrocerEase🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>Online Grocery Ordering Using LLMs🧠</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Robby's Pages
st.subheader("🚀 Prompt GrocerEase:")
#
st.write("""
- “ I’m feeling like having spaggetthi with meat sauce. Make it enough for 3 people.”\n
- “ I forgot to mention that I'm gluten free.”\n
- “ Please recommend snacks for a 4 hour long hike”
""")
# st.write("""
# - **Robby-Chat**: General Chat on data (PDF, TXT,CSV) with a [vectorstore](https://github.com/facebookresearch/faiss) (index useful parts(max 4) for respond to the user) | works with [ConversationalRetrievalChain](https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html)
# - **Robby-Sheet** (beta): Chat on tabular data (CSV) | for precise information | process the whole file | works with [CSV_Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/csv.html) + [PandasAI](https://github.com/gventuri/pandas-ai) for data manipulation and graph creation
# - **Robby-Youtube**: Summarize YouTube videos with [summarize-chain](https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html)
# """)
st.markdown("---")


#Contributing
st.markdown("### 🎯 Benefits")
st.markdown("""

- Time savings is one of the most important drivers of online grocery ordering
- No existing grocery solutions are primarily chatbot-based
""", unsafe_allow_html=True)
# st.markdown("""
# **Robby is under regular development. Feel free to contribute and help me make it even more data-aware!**
# """, unsafe_allow_html=True)





