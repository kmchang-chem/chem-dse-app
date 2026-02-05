import streamlit as st
import pandas as pd
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="DSE Chemistry Quiz", layout="centered")

# --- 2. 絕對路徑處理 (解決找不到檔案的問題) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "questions.csv")

# --- 3. 載入資料 ---
@st.cache_data
def load_data():
    if not os.path.exists(csv_path):
        return None
    return pd.read_csv(csv_path)

df = load_data()

if df is None:
    st.error(f"❌ 找不到 questions.csv 檔案！請確認檔案放在：{current_dir}")
    st.stop()

# --- 4. 側邊欄：選擇題目 ---
st.sidebar.title("題目選擇")
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0

selected_q = st.sidebar.selectbox(
    "跳轉至題目",
    range(len(df)),
    format_func=lambda i: f"Question {df.iloc[i]['id']}",
    index=st.session_state.q_idx
)
st.session_state.q_idx = selected_q

# --- 5. 主介面：顯示題目 ---
q_row = df.iloc[st.session_state.q_idx]

st.title(f"Chemistry Quiz - Q{q_row['id']}")
st.subheader(f"Topic: {q_row['topic']}")

# 顯示題目文字
st.markdown(f"#### {q_row['question_text']}")

# 顯示圖片 (如果有提供圖片檔名且檔案存在)
if pd.notna(q_row['image_filename']) and q_row['image_filename'] != "":
    img_path = os.path.join(current_dir, q_row['image_filename'])
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info(f"（圖片 {q_row['image_filename']} 準備中）")

# --- 6. 答題邏輯 ---
options = [
    f"A. {q_row['option_a']}",
    f"B. {q_row['option_b']}",
    f"C. {q_row['option_c']}",
    f"D. {q_row['option_d']}"
]

# 使用 radio 按鈕選擇答案
choice = st.radio("選擇你的答案：", options, index=None)

if st.button("提交答案"):
    if choice:
        user_ans = choice[0]  # 取得 A, B, C 或 D
        correct_ans = str(q_row['correct_answer']).strip()
        
        if user_ans == correct_ans:
            st.success(f"✅ 正確！ 答案是 {correct_ans}")
        else:
            st.error(f"❌ 錯誤！ 正確答案是 {correct_ans}")
        
        # 顯示詳解
        st.markdown("---")
        st.markdown("### 💡 詳細解釋")
        st.info(q_row['explanation'])
    else:
        st.warning("請先選擇一個選項再提交。")

# --- 7. 下一題按鈕 ---
if st.session_state.q_idx < len(df) - 1:
    if st.button("下一題 ➡️"):
        st.session_state.q_idx += 1
        st.rerun()