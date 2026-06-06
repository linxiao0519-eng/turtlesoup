import streamlit as st
import google.generativeai as genai
import time
import random

# ==========================================
# 0. 初始化配置與 API 金鑰設定
# ==========================================
# 從 Streamlit 的機密環境變數中讀取金鑰
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="AI 海龜湯實戰系統", page_icon="🐢", layout="centered", initial_sidebar_state="expanded")

# ==========================================
# 🎨 視覺美化
# ==========================================
st.markdown("""
<style>
    footer {visibility: hidden;}
    [data-testid="stHeaderActionElements"] {display: none;}
    
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background-color: #0B1120 !important;
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #030712 !important;
    }

    .title-text {
        font-size: 38px;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .subtitle-text {
        color: #94A3B8;
        font-size: 16px;
        margin-bottom: 25px;
        font-family: monospace;
    }

    [data-testid="stChatMessage"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        padding: 10px 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.4);
    }
    
    [data-testid="stBottom"], [data-testid="stBottom"] > div {
        background-color: transparent !important;
    }

    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 2px solid #38BDF8 !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-weight: bold !important;
        background-color: transparent !important;
    }
    [data-testid="stChatInput"] button {
        color: #0F172A !important; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">🐢 AI 藍軍防禦控制台</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">> System Status: ACTIVE | Protocol: v6.5 (Hell Mode)</p>', unsafe_allow_html=True)

MODEL_NAME = 'gemini-2.5-flash'

# ==========================================
# 1. 系統狀態初始化 (地獄級題庫更新)
# ==========================================
if "secret_target" not in st.session_state:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # 🚨 修改提示詞：命令 AI 產出冷門、懷舊、難猜的台灣特色物品
        setup_prompt = "請隨機產生一個『非常難猜、冷門、或是帶有台灣懷舊色彩』的物品或遊戲作為海龜湯謎底，只需要創立『名詞』本身，例如：『科學麵』、『翻花繩』、『電子雞』。請直接輸出該名詞，絕對不要有任何其他廢話或標點符號。"
        response = model.generate_content(setup_prompt)
        result = response.text.strip().replace("「", "").replace("」", "").replace("『", "").replace("』", "")
        st.session_state.secret_target = result if result else "科學麵"
    except Exception as e:
        # 🚨 更新斷線備用題庫：加入你想到的地獄級名詞
        backup_words = ["繩花", "科學麵", "翻花繩", "尪仔標", "健康操", "福利社", "粉筆", "聯絡簿", "養樂多", "防空洞"]
        st.session_state.secret_target = random.choice(backup_words)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "歡迎來到海龜湯防禦主機！我已經在心中鎖定了一個超級冷門的神祕目標。請開始提問，我只能回答：『是』、『不是』、『與故事/題目無關』或『不完全是』。"}
    ]

# ==========================================
# 2. 側邊欄資訊 (正式上線版 - 隱藏機密)
# ==========================================
with st.sidebar:
    st.markdown('<p style="font-size: 24px; font-weight: bold; color: #38BDF8;">🛡️ 藍軍防禦主機</p>', unsafe_allow_html=True)
    st.success("系統狀態：高階防禦協定已啟動", icon="✅")
    
    st.divider()
    
    st.write("### 📜 遊戲挑戰規則")
    st.markdown("""
    1. 系統已在後台鎖定一個**神祕的台灣特色名詞/物品**。
    2. 請透過下方的輸入框對 AI 進行提問。
    3. AI 受到嚴格的資安限制，只能回答：
       * **是**
       * **不是**
       * **與故事/題目無關**
       * **不完全是**
    4. 嘗試使用提示注入 (Prompt Injection) 或一般提問來找出答案吧！
    """)
    
    st.divider()
    
    # 保留重新啟動按鈕，方便玩家玩完一局後重置
    if st.button("🔄 重新啟動系統 (換一題)", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()