import streamlit as st
import pandas as pd
from datetime import datetime
import time
import webbrowser
import base64

# ══════════════════════════════════════════════════════════════════════════
#  AILYN PRO MASTER V2.4 — 16K UHD (ULTRA INTRO + QTY FIXED)
#  ENGINE: 0.2s SMOOTH CLICK | HARDWARE ACCELERATED
#  INTRO: NEON GLOW SPLASH SCREEN
# ══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AILYN PRO 16K", 
    page_icon="🏗️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

class AilynPro16K:
    def __init__(self):
        self.NAME = "AILYN CONSTRUCTION"
        self.SENDER_ID = "HOUSE PROJECT"
        self.AILYN_EMAIL = "ailyn_peps0678@yahoo.com"
        self.GARRY_EMAIL = "garryboypepito2004@gmail.com"
        self.neon = "#00ff88"
        self.bg_img = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070"

        if 'ledger' not in st.session_state: st.session_state.ledger = []
        if 'budget_main' not in st.session_state: st.session_state.budget_main = 0.0
        if 'budget_surplus' not in st.session_state: st.session_state.budget_surplus = 0.0
        if 'view' not in st.session_state: st.session_state.view = "HOME"
        if 'mode' not in st.session_state: st.session_state.mode = ""
        if 'intro_done' not in st.session_state: st.session_state.intro_done = False

    def inject_16k_engine(self):
        st.markdown(f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@400;700;900&display=swap');
            
            * {{ -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }}
            
            .stApp {{ 
                background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("{self.bg_img}"); 
                background-size: cover; background-position: center; background-attachment: fixed; 
            }}

            /* UHD INTRO ANIMATION */
            @keyframes neonFade {{
                0% {{ opacity: 0; transform: scale(0.9); filter: blur(10px); }}
                50% {{ opacity: 1; filter: blur(0px); text-shadow: 0 0 30px {self.neon}; }}
                100% {{ opacity: 0; transform: scale(1.1); }}
            }}
            .intro-text {{
                font-family: 'Orbitron', sans-serif;
                color: white;
                font-size: 80px;
                letter-spacing: 25px;
                text-align: center;
                margin-top: 35vh;
                animation: neonFade 1.5s ease-in-out forwards;
            }}

            /* 16K GLASS CAPSULE */
            .main-capsule {{
                background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(50px);
                border-radius: 60px; padding: 45px; border: 1px solid rgba(255,255,255,0.08);
                display: flex; justify-content: space-around; align-items: center;
                margin: 20px auto; max-width: 1100px; transform: translateZ(0);
                box-shadow: 0 40px 100px rgba(0,0,0,0.8);
            }}
            .metric-label {{ color: {self.neon}; font-size: 0.7rem; letter-spacing: 6px; font-weight: 900; text-transform: uppercase; opacity: 0.8; }}
            .metric-value {{ color: white; font-size: 4rem; font-weight: 900; font-family: 'Inter'; letter-spacing: -2px; }}

            /* 0.2S SMOOTH BUTTONS */
            .stButton>button {{
                background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255,255,255,0.1) !important;
                border-radius: 22px !important; color: white !important; height: 95px !important;
                font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; transform: translateZ(0);
            }}
            .stButton>button:hover {{ 
                border: 1px solid {self.neon} !important; color: {self.neon} !important; 
                background: rgba(0, 255, 136, 0.08) !important; transform: translateY(-4px) scale(1.02); 
                box-shadow: 0 20px 40px rgba(0, 255, 136, 0.15) !important;
            }}
            .stButton>button:active {{ transform: scale(0.95); opacity: 0.8; }}
            
            header, footer {{ visibility: hidden !important; }}
            </style>
        """, unsafe_allow_html=True)

    def send_gmail_draft(self, target):
        total = st.session_state.budget_main + st.session_state.budget_surplus
        spent = sum(x['TOTAL'] for x in st.session_state.ledger)
        mat_list = "".join([f"- {e['QTY']}x {e['ITEM']}: P{e['TOTAL']:,.2f}%0A" for e in st.session_state.ledger])
        subject = f"{self.SENDER_ID}: Update - {datetime.now().strftime('%Y-%m-%d')}"
        body = f"Good Taylin,%0A%0AITEMS SUMMARY:%0A{mat_list}%0ABALANCE: P{total-spent:,.2f}%0A%0AUpdate heart heart ❤️"
        dest = {"GARRY": self.GARRY_EMAIL, "AILYN": self.AILYN_EMAIL, "BOTH": f"{self.GARRY_EMAIL},{self.AILYN_EMAIL}"}.get(target)
        webbrowser.open_new_tab(f"https://mail.google.com/mail/?view=cm&fs=1&to={dest}&su={subject}&body={body}")

    def generate_html_receipt(self):
        total = st.session_state.budget_main + st.session_state.budget_surplus
        spent = sum(x['TOTAL'] for x in st.session_state.ledger)
        rows = "".join([f"<tr><td>{e['DATE']}</td><td>{e['QTY']}</td><td>{e['ITEM']}</td><td align='right'>P{e['TOTAL']:,.2f}</td></tr>" for e in st.session_state.ledger])
        html = f"<html><body style='background:#000;color:#fff;font-family:sans-serif;padding:20px;'><h2>{self.NAME}</h2><table border='1' width='100%'><tr><th>DATE</th><th>QTY</th><th>ITEM</th><th>TOTAL</th></tr>{rows}</table><h3>Balance: P{total-spent:,.2f}</h3></body></html>"
        b64 = base64.b64encode(html.encode()).decode()
        return f'<a href="data:text/html;base64,{b64}" download="Receipt.html" style="text-decoration:none;"><button style="width:100%; height:95px; background:rgba(0,255,136,0.1); border:1px solid {self.neon}; color:{self.neon}; border-radius:22px; font-weight:900; cursor:pointer; transition:0.2s;">📥 DOWNLOAD RECEIPT</button></a>'

    def run(self):
        self.inject_16k_engine()
        total_avail = st.session_state.budget_main + st.session_state.budget_surplus
        spent = sum(x['TOTAL'] for x in st.session_state.ledger)

        # UPDATED ULTRA-HD INTRO
        if not st.session_state.intro_done:
            st.markdown(f'<div class="intro-text">{self.NAME}</div>', unsafe_allow_html=True)
            time.sleep(1.5)
            st.session_state.intro_done = True
            st.rerun()

        if st.session_state.view == "HOME":
            st.markdown(f'<h2 style="text-align:center; color:white; font-family:\'Orbitron\'; letter-spacing:15px; margin-top:30px; font-weight:900;">{self.SENDER_ID}</h2>', unsafe_allow_html=True)
            st.markdown(f"""<div class="main-capsule">
                <div style="text-align:center;"><div class="metric-label">Total Fund</div><div class="metric-value">₱ {total_avail:,.2f}</div></div>
                <div style="width:1px; height:80px; background:rgba(255,255,255,0.15);"></div>
                <div style="text-align:center;"><div class="metric-label">Current Balance</div><div class="metric-value" style="color:{self.neon}">₱ {total_avail-spent:,.2f}</div></div>
            </div>""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📦 Materials"): st.session_state.mode = "MATERIAL"; st.session_state.view = "ADD"; st.rerun()
                if st.button("🛠️ Others"): st.session_state.mode = "OTHERS"; st.session_state.view = "ADD"; st.rerun()
            with c2:
                if st.button("📧 Gmail Center"): st.session_state.view = "GMAIL_CENTER"; st.rerun()
                if st.button("⚠️ Reset All"): st.session_state.ledger = []; st.rerun()
            with c3:
                if st.button("🚚 Delivery"): st.session_state.mode = "DELIVERY"; st.session_state.view = "ADD"; st.rerun()
                if st.button("💰 Budget Setup"): st.session_state.view = "CONFIG"; st.rerun()

            if st.session_state.ledger:
                st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True, hide_index=True)

        elif st.session_state.view == "GMAIL_CENTER":
            st.markdown('<div class="main-capsule" style="flex-direction:column; gap:20px;">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 Sync to Ailyn"): self.send_gmail_draft("AILYN")
                if st.button("🛡️ Sync to Garry"): self.send_gmail_draft("GARRY")
            with col2:
                if st.button("📡 Broadcast Both"): self.send_gmail_draft("BOTH")
                st.markdown(self.generate_html_receipt(), unsafe_allow_html=True)
            if st.button("⬅️ BACK TO BOARD"): st.session_state.view = "HOME"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.view == "ADD":
            st.markdown(f'<h3 style="color:{self.neon}; text-align:center; font-family:Orbitron;">{st.session_state.mode} ENTRY</h3>', unsafe_allow_html=True)
            with st.form("fast_form", clear_on_submit=True):
                item = st.text_input("ITEM DESCRIPTION").upper()
                c1, c2 = st.columns(2)
                qty = c1.number_input("QUANTITY", min_value=1, value=1)
                price = c2.number_input("PRICE PER UNIT", min_value=0.0)
                if st.form_submit_button("SAVE RECORD") and item:
                    st.session_state.ledger.insert(0, {"DATE": datetime.now().strftime("%Y-%m-%d"), "QTY": qty, "ITEM": item, "TOTAL": qty * price})
                    st.rerun()
            if st.button("FINISH"): st.session_state.view = "HOME"; st.rerun()

        elif st.session_state.view == "CONFIG":
            st.markdown('<h2 style="text-align:center; color:white; font-family:Orbitron;">FUNDS SETUP</h2>', unsafe_allow_html=True)
            st.session_state.budget_main = st.number_input("Main Fund", value=st.session_state.budget_main)
            st.session_state.budget_surplus = st.number_input("Surplus", value=st.session_state.budget_surplus)
            if st.button("SAVE & RETURN"): st.session_state.view = "HOME"; st.rerun()

if __name__ == "__main__":
    AilynPro16K().run()