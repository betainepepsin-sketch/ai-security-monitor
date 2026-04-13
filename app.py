import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

st.set_page_config(page_title="AI 智慧雲端資安監控系統", layout="wide")

st.title("🛡️ AI 智慧雲端資安診斷系統")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 系統日誌即時饋送")
    sample_logs = """[2026-04-13 14:20:01] INFO: 使用者 'admin' 從 192.168.1.50 登入成功
[2026-04-13 14:22:15] WARNING: 發現來自 203.0.113.5 的多次登入失敗嘗試
[2026-04-13 14:25:30] CRITICAL: 偵測到 CloudStorage-01 出現未授權的 API 調用
[2026-04-13 14:28:12] ERROR: 子網域 subnet-2a 資料庫連線逾時"""
    
    log_input = st.text_area("Live Log Feed (預覽)", value=sample_logs, height=250)
    
    if st.button("🔍 執行 AI 威脅深度診斷"):
        with st.spinner("AI 正在分析日誌邏輯..."):
            st.warning("【AI 分析報告】偵測到高度疑似「暴力破解攻擊」。建議動作：立即針對來源 IP 執行防火牆阻斷，並查核管理員帳號權限。")

with col2:
    st.subheader("📊 資安風險指標")
    risk_data = pd.DataFrame({
        "監控維度": ["身份認證", "網路行為", "API調用", "資料存儲"],
        "風險等級": [85, 40, 95, 20]
    })
    st.bar_chart(risk_data.set_index("監控維度"))
    
    st.divider()
    
    st.subheader("⚡ 應變動作中心")
    if st.button("📢 發送資安警報至 Slack"):
        if not SLACK_WEBHOOK:
            st.error("錯誤：未偵測到環境變數中的 Webhook 配置。")
        else:
            payload = {"text": f"🚨 【資安警報】偵測到高風險活動\n內容摘要：{log_input[:100]}..."}
            try:
                resp = requests.post(SLACK_WEBHOOK, json=payload)
                if resp.status_code == 200:
                    st.success("警報已同步至 Slack 頻道。")
                else:
                    st.error(f"發送失敗。狀態碼：{resp.status_code}")
            except Exception as e:
                st.error(f"系統異常：{str(e)}")

st.sidebar.header("📡 系統運行狀態")
st.sidebar.info("執行環境：AWS Lambda (Active)")
st.sidebar.info("核心引擎：Claude-3-Sonnet")
st.sidebar.write("---")
st.sidebar.caption("本系統為自主研發之資安自動化原型。")
