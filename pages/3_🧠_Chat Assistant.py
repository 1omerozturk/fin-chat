import streamlit as st
import os
import dotenv
from dotenv import load_dotenv
import openai
import json

# Sayfanın Başlığı
st.title(":speech_balloon: Fin_Chat Bot")

# Chat geçmişi oluşturma
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_messages" not in st.session_state:
    st.session_state.user_messages = []

# Geçmişi JSON dosyasında tutma
history_file_path = "chat_history.json"

# Geçmişi dosyadan yükleme
if os.path.exists(history_file_path):
    with open(history_file_path, "r") as file:
        st.session_state.messages = json.load(file)

# Mesaj geçmişini gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı mesajı alma ve gpt den geri dönüş alma
if prompt := st.chat_input(placeholder="Ask me questions."):

    # Kullanıcının Mesajı gösterme
    st.chat_message("user").markdown(prompt)

    # Kullanıcının mesajını geçmişe ekleme
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gpt den dönen mesajı alma
    load_dotenv()
    ak = os.getenv("API_KEY")
    openai.api_key = ak

    def chat(prompt):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt + " ,Bana bu sorunun cevabını (finansal asistan) olarak verir misin?",
                }
            ],
        )
        return completion.choices[0].message.content.strip()

    response = chat(prompt)

    # Gpt den dönen mesajı gösterme
    with st.chat_message("assistant"):
        st.markdown(f"**Siz:** {prompt}", unsafe_allow_html=True)
        st.markdown(f"**Assistant:** {response}", unsafe_allow_html=True)

    # Gptden dönen mesajı mesaj geçmişine ekleme:
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Geçmişi JSON dosyasına kaydetme
    with open(history_file_path, "w") as file:
        json.dump(st.session_state.messages, file)

# Solda geçmişi gösterme
with st.sidebar:
    st.title("Chat History - User")
    for idx, message in enumerate(st.session_state.messages, start=1):
        if message["role"] == "user":
            st.markdown(f"<strong>{idx}. User:</strong> {message['content']}", unsafe_allow_html=True)
