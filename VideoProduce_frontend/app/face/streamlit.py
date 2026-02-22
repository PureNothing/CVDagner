import streamlit as st
import requests
from app.core import config

st.title("🎥 Выберете камеру и загрузите видео")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("1️⃣ Камера 1", use_container_width=True):
        st.session_state.camera = 1

with col2:
    if st.button("2️⃣ Камера 2", use_container_width=True):
        st.session_state.camera = 2

with col3:
    if st.button("3️⃣ Камера 3", use_container_width=True):
        st.session_state.camera = 3

with col4:
    if st.button("4️⃣ Камера 4", use_container_width=True):
        st.session_state.camera = 4

with col5:
    if st.button("5️⃣ Камера 5", use_container_width=True):
        st.session_state.camera = 5

if "camera" in st.session_state:
    st.info(f"🎯 Выбрана камера {st.session_state.camera}")

    files = st.file_uploader("📥 Загрузите видео", accept_multiple_files=True, type=["mp4", "avi", "mov"])

    if st.button("📤 Отправить") and files:
        with st.spinner(f"⏳ Отправляю {len(files)} видео.."):

            file_to_send = []
            for file in files:
                file_to_send.append(("file", file))
            
            url = f"{config.FAST_API_URL}/{st.session_state.camera}"
            response = requests.post(url=url, files=file_to_send)

            if response.status_code == 200:
                st.success(f"✅  Видео загружено")
            else:
                st.error(f"❌ Ошибка загрузки")
