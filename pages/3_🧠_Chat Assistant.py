import streamlit as st
import os
import dotenv
from dotenv import load_dotenv
import openai


# Sayfanın Başlığı
st.title(":speech_balloon: Fin_Chat Bot")

# Chat geçmişi oluşturma ve kuyruk yapısı
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini göstermek 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı mesajı alma ve gpt den geri dönüş alma
if prompt := st.chat_input(placeholder="Ask me questions."):
    # Kullanıcının Mesajı gösterme
    st.chat_message("user").markdown(prompt)
    # Kullanıcının mesajını geçmişe ekleme
    st.session_state.messages.append({"role": "user", "content": prompt})
    load_dotenv()
    ak=os.getenv("API_KEY")
    openai.api_key=ak
    def chat(prompt):
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
         "role": "user",
         "content": prompt + "Bana bu sorunun cevabını (finansal asistan) olarak verir misin?",
         }
            ]
        )
        return completion.choices[0].message.content.strip()
    response = chat(prompt)
    # Gpt den dönen mesajı gösterme
    with st.chat_message("assistant"):
        st.markdown(response)
    # Gptden dönen mesajı mesaj geçmişine ekleme:
    st.session_state.messages.append({"role": "assistant", "content": response})
    

