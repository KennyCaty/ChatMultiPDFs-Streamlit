import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from pypdf import PdfReader

from langchain.text_splitter import CharacterTextSplitter #文档分割器
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from HTMLtemplate import css, bot_template, user_template
# 如果要使用 Huggingface的 LLM
# from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf_docs):
    """返回一串字符串"""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: #循环读取每一页
            text += page.extract_text()  #提取文本
    return text

def get_text_chunks(raw_text):
    """分割成chunk列表"""
    text_spliter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200, #重叠部分，防止语言丢失
        length_function=len
    )
    chunks = text_spliter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    emmeddings = OpenAIEmbeddings()  # 需要付费的key 速度很快
    # emmeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')  # 速度较慢，免费
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=emmeddings)
    return vectorstore

def get_convsersation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5,"max_length":512})

    # 我们需要有意有记忆的ChatBot
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    print(response)
    # st.write(response)
    st.session_state.chat_history = response['chat_history'] #将历史保存在session_state里面

    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0: # human
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="ChatMultyPDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True) #允许写入HTML

    if 'conversation' not in st.session_state:
        st.session_state.conversation = None  #避免重复初始化
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header("ChatMultyPDFs :books:")

    st.write("Upload your PDFs firts!!!")
    user_question = st.text_input("Ask a question about your document, end press 'ENTER'")
    if user_question: #只有当用户提交时为True
        handle_userinput(user_question)

    # st.write(user_template.replace("{{MSG}}", "Hello GPT"), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", "Hello human"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_ducs = st.file_uploader("upload your pdf and click 'Process'", accept_multiple_files=True)
        '''返回一个文档列表'''
        if st.button("Process"):
            with st.spinner("Prosessing your PDFs"):
                # get pdf text
                raw_text = get_pdf_text(pdf_ducs)
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create a conversation chain
                st.session_state.conversation = get_convsersation_chain(vectorstore)

                st.write("DONE")


if __name__ == '__main__':
    main()