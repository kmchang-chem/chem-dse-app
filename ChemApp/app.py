import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="HKDSE Chem", layout="centered")

@st.cache_data
def load_data():
    # 強制使用 utf-8 讀取，並忽略錯誤行
    return pd.read_csv("questions.csv", encoding="utf-8", on_bad_lines='skip')

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 初始化 Session State
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'score' not in st.session_state:
    st.session_state.score = {'correct': 0, 'total': 0}
if 'answered' not in st.session_state:
    st.session_state.answered = False

# 側邊欄
st.sidebar.title("🧪 Chemistry Setup")
topics = df['topic'].unique()
selected_topic = st.sidebar.selectbox("Select Topic:", topics)

if 'last_topic' not in st.session_state:
    st.session_state.last_topic = None

# 如果按了按鈕，或者「目前選的主題」跟「上一次」不一樣
if st.sidebar.button("New Random Question") or (selected_topic != st.session_state.last_topic):
    st.session_state.last_topic = selected_topic  # 更新紀錄
    topic_df = df[df['topic'] == selected_topic]
    if not topic_df.empty:
        st.session_state.current_q = topic_df.sample(1).iloc[0]
        st.session_state.answered = False

# 主畫面
st.title("HKDSE Chemistry Practice")

col1, col2 = st.columns(2)
col1.metric("Score", f"{st.session_state.score['correct']} / {st.session_state.score['total']}")

if st.session_state.current_q is not None:
    q = st.session_state.current_q
    st.markdown(f"### {q['question_text']}")
    
    # 圖片處理
    if pd.notna(q['image_filename']):
        img_path = os.path.join("images", str(q['image_filename']).strip())
        if os.path.exists(img_path):
            st.image(img_path)
    
    with st.form("quiz_form"):
        options = {"A": q['option_a'], "B": q['option_b'], "C": q['option_c'], "D": q['option_d']}
        choice = st.radio("Choose:", list(options.keys()), format_func=lambda x: f"{x}. {options[x]}")
        
        if st.form_submit_button("Submit"):
            correct = str(q['correct_answer']).strip().upper()
            if choice == correct:
                st.success("✅ Correct!")
                if not st.session_state.answered:
                    st.session_state.score['correct'] += 1
                    st.session_state.score['total'] += 1
                    st.session_state.answered = True
            else:
                st.error(f"❌ Wrong! Answer is {correct}")
                if not st.session_state.answered:
                    st.session_state.score['total'] += 1
                    st.session_state.answered = True
            st.info(f"Explanation: {q['explanation']}")
else:
    st.info("👈 Click 'New Random Question' to start!")
