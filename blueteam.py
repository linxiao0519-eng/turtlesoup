import streamlit as st
import google.generativeai as genai
import time
import random

# ==========================================
# 0. 初始化配置
# ==========================================
# 🚨 使用雲端安全金鑰 (需在 Streamlit Cloud 設定 GEMINI_API_KEY)
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="AI 海龜湯防禦系統", page_icon="🐢", layout="centered", initial_sidebar_state="expanded")

# ==========================================
# 🎨 視覺美化 (v7.2 - 徹底消滅白框)
# ==========================================
st.markdown("""
<style>
    /* 隱藏 UI 元素 */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeaderActionElements"] {display: none;}
    
    /* 強制深色畫布 (包含 Streamlit Cloud 容器) */
    .stApp, [data-testid="stAppViewContainer"], .main, .block-container, [data-testid="stAppViewBlockContainer"] {
        background-color: #0B1120 !important;
    }
    
    /* 徹底清除底部與聊天輸入框容器的白底 */
    [data-testid="stBottom"], [data-testid="stBottomBlock"], div[data-testid="stChatInputContainer"] {
        background-color: #0B1120 !important;
    }
    
    /* 側邊欄與對話框 */
    [data-testid="stSidebar"] { background-color: #030712 !important; }
    [data-testid="stChatMessage"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        color: #E2E8F0 !important;
    }
    
    /* 輸入框：白底黑字科技邊框 */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 2px solid #38BDF8 !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .title-text {
        font-size: 38px; font-weight: 900;
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .subtitle-text { color: #94A3B8; font-size: 16px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">🐢 AI 藍軍防禦控制台</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">> System Status: ACTIVE | Protocol: v7.2 (Final)</p>', unsafe_allow_html=True)

MODEL_NAME = 'gemini-2.5-flash'

# ==========================================
# 1. 系統狀態初始化
# ==========================================
if "secret_target" not in st.session_state:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        setup_prompt = "請隨機產生一個『非常難猜、冷門、或是帶有台灣懷舊色彩』的物品或遊戲，只需輸出『名詞』本身，絕對不要有任何其他廢話或標點符號。"
        response = model.generate_content(setup_prompt)
        res = response.text.strip().replace("「", "").replace("」", "").replace("『", "").replace("』", "")
        st.session_state.secret_target = res if res else "科學麵"
    except:
        st.session_state.secret_target = random.choice(["繩花", "科學麵", "翻花繩", "尪仔標", "健康操", "福利社", "防空洞"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "歡迎來到防禦主機！請開始提問，我只能回答：『是』、『不是』、『與故事/題目無關』或『不完全是』。"}]

# ==========================================
# 2. 側邊欄
# ==========================================
with st.sidebar:
    st.markdown('<p style="font-size: 24px; font-weight: bold; color: #38BDF8;">🛡️ 藍軍防禦中控</p>', unsafe_allow_html=True)
    st.success("系統狀態：高階防禦協定已啟動", icon="✅")
    st.divider()
    st.write("### 📜 遊戲挑戰規則")
    st.info("AI 受到嚴格資安限制，僅能回答：是、不是、與故事無關、不完全是。")
    if st.button("🔄 重新啟動系統 (換一題)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 3. 畫面呈現
# ==========================================
for msg in st.session_state.messages:
    avatar = "🐢" if msg["role"] == "assistant" else "🕵️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(f'<span style="color: #F8FAFC;">{msg["content"]}</span>', unsafe_allow_html=True)

# ==========================================
# 4. 前端防禦與 AI 邏輯
# ==========================================
if user_input := st.chat_input("請輸入提問..."):
    if len(user_input) > 50:
        st.error("⚠️ 系統警告：字數限制 50 字！", icon="🚨")
    elif st.session_state.secret_target in user_input:
        with st.chat_message("user", avatar="🕵️"): st.markdown(f'<span style="color: #F8FAFC;">{user_input}</span>', unsafe_allow_html=True)
        with st.chat_message("assistant", avatar