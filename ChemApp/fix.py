import pandas as pd
import os

# 1. 這是最標準、格式完美的 CSV 內容
csv_content = """id,topic,question_text,image_filename,option_a,option_b,option_c,option_d,correct_answer,explanation
1,Separation Methods,Which of the following mixtures can be separated by filtration?,,"a mixture of oil and water","a mixture of ethanol and water","a mixture of silver chloride and water","a mixture of sodium chloride and water",C,"Filtration is used to separate an insoluble solid from a liquid. AgCl is insoluble."
2,Environmental Chem,Which of the following gases can cause acid rain?,,"CH4(g)","CO(g)","N2(g)","SO2(g)",D,"Sulphur dioxide (SO2) dissolves in rain water to form acid rain."
3,General Chem,Solid W dissolves in water to form an alkaline solution. What is W?,,"calcium oxide","calcium chloride","copper(II) oxide","copper(II) chloride",A,"Calcium oxide (CaO) reacts with water to form calcium hydroxide, which is alkaline."
4,Stoichiometry,Which fertiliser has the highest percentage by mass of nitrogen?,,"(NH2)2CO","NH4NO3","NaNO3","(NH4)2SO4",A,"Urea (NH2)2CO has the highest % of Nitrogen by mass."
5,Redox,"Consider the experimental set-up with KMnO4 and CuSO4. What is observed?",2023_q5_setup.png,"Purple patch to P","Purple patch to Q","Purple to P, Blue to Q","Purple to Q, Blue to P",C,"MnO4- (purple) is negative, migrates to Anode (P). Cu2+ (blue) is positive, migrates to Cathode (Q)."
"""

# 2. 這是修正後的 App 程式碼 (確保讀取設定正確)
app_code = """import streamlit as st
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

if st.sidebar.button("New Random Question"):
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
"""

# 3. 執行寫入動作 (強制覆蓋舊檔案)
print("正在修復檔案...")
try:
    with open("questions.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    print("✅ questions.csv 重建成功！(格式: UTF-8)")

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(app_code)
    print("✅ app.py 重建成功！(已修正讀取邏輯)")
    
    print("\n🎉 修復完成！請執行: streamlit run app.py")
except Exception as e:
    print(f"❌ 寫入失敗: {e}")