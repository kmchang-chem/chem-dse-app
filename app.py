import streamlit as st
import pandas as pd
import os

# --- 1. 頁面基本設定 (這行一定要在最上面) ---
st.set_page_config(page_title="DSE Chemistry Quiz by ChemChang", layout="centered")

# ==========================================
# 👇 請將 CSS 樣式貼在這裡 (在 set_page_config 之後)
# ==========================================
st.markdown(
    """
    <style>
    /* 1. 整體背景顏色 (淺灰藍，保護眼睛) */
    .stApp {
        background-color: #F0F2F6;
    }

    /* 2. 標題 (H1) 樣式 */
    h1 {
        color: #2E86C1; /* 化學藍 */
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;
    }

    /* 3. 副標題 (H3) 樣式 - 對應 Topic */
    h3 {
        color: #2874A6;
        border-bottom: 2px solid #2874A6;
        padding-bottom: 10px;
    }

    /* 4. 題目文字 (Markdown) 加大 */
    .stMarkdown p {
        font-size: 20px !important;
        color: #17202A;
    }

    /* 5. 按鈕美化 (圓角 + 陰影) */
    .stButton>button {
        background-color: #ffffff;
        color: #2E86C1;
        border: 2px solid #2E86C1;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #2E86C1;
        color: white;
        border-color: #2E86C1;
    }

    /* 6. 側邊欄背景 */
    [data-testid="stSidebar"] {
        background-color: #D6EAF8;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ==========================================

# --- 2. 絕對路徑處理 (後面維持原本的程式碼) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "questions.csv")

--- 3. 載入資料 ---
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