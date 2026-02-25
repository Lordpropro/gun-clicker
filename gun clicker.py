import streamlit as st
import time
import base64
import os

st.set_page_config(page_title="Gun Clicker", page_icon="🔫", layout="wide")

# --- Helper to load your image into CSS ---
@st.cache_data
def load_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Load your gun.png file
gun_b64 = load_image_base64("gun.png")

# --- CSS Trick to inject the image directly into the button ---
if gun_b64:
    st.markdown(f"""
    <style>
    /* Target the specific button hiding underneath our custom marker */
    div[data-testid="stMarkdownContainer"]:has(#gun-target) + div[data-testid="stButton"] button {{
        background-image: url("data:image/png;base64,{gun_b64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        background-color: transparent;
        border: none;
        box-shadow: none;
        height: 250px; /* Adjust this to change gun size */
        color: transparent; /* Hides the default button text */
    }}
    
    /* Add a cool clicker-game "bounce" animation! */
    div[data-testid="stMarkdownContainer"]:has(#gun-target) + div[data-testid="stButton"] button:hover {{
        transform: scale(1.05);
        background-color: transparent;
    }}
    div[data-testid="stMarkdownContainer"]:has(#gun-target) + div[data-testid="stButton"] button:active {{
        transform: scale(0.95);
        background-color: transparent;
    }}
    
    /* Ensure default text is definitely hidden */
    div[data-testid="stMarkdownContainer"]:has(#gun-target) + div[data-testid="stButton"] button p {{
        display: none; 
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ 'gun.png' not found. Make sure the image is in the exact same folder as this script!")

st.title("🔫 Gun Clicker")

# --- Initialize game state ---
if "money" not in st.session_state:
    st.session_state.money = 0
if "damage" not in st.session_state:
    st.session_state.damage = 1
if "auto_damage" not in st.session_state:
    st.session_state.auto_damage = 0
if "upgrade_cost" not in st.session_state:
    st.session_state.upgrade_cost = 10
if "auto_cost" not in st.session_state:
    st.session_state.auto_cost = 50
if "last_time" not in st.session_state:
    st.session_state.last_time = time.time()
if "floating_messages" not in st.session_state:
    st.session_state.floating_messages = []

# --- Auto shooter logic ---
current_time = time.time()
elapsed = current_time - st.session_state.last_time
if elapsed >= 1:
    ticks = int(elapsed) # Figure out how many full seconds passed
    st.session_state.money += st.session_state.auto_damage * ticks
    st.session_state.last_time += ticks # Preserves fractions of a second so math stays accurate

# --- Layout ---
col1, col2 = st.columns([2,1])

with col1:
    # 1. We drop an invisible marker so our CSS knows exactly which button to target
    st.markdown('<div id="gun-target"></div>', unsafe_allow_html=True)
    
    # 2. The standard button (CSS transforms this into your actual gun.png)
    if st.button("CLICK", key="gun_click", use_container_width=True):
        st.session_state.money += st.session_state.damage
        st.session_state.floating_messages.append(f"+{st.session_state.damage}")
        
        # Keep app fast by only saving the last 3 messages so the list doesn't grow infinitely
        if len(st.session_state.floating_messages) > 3:
            st.session_state.floating_messages = st.session_state.floating_messages[-3:]

    # Display money
    st.markdown(f"**💰 Money: ${st.session_state.money}**")

    # Show last 3 floating messages
    for msg in st.session_state.floating_messages:
        st.info(msg, icon="💥")

with col2:
    st.subheader("🏪 Shop")
    
    if st.button(f"Upgrade Gun (+1) - ${st.session_state.upgrade_cost}"):
        if st.session_state.money >= st.session_state.upgrade_cost:
            st.session_state.money -= st.session_state.upgrade_cost
            st.session_state.damage += 1
            st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)
    
    if st.button(f"Buy Auto Shooter (+1/sec) - ${st.session_state.auto_cost}"):
        if st.session_state.money >= st.session_state.auto_cost:
            st.session_state.money -= st.session_state.auto_cost
            st.session_state.auto_damage += 1
            st.session_state.auto_cost = int(st.session_state.auto_cost * 1.7)

    st.write("🔫 Damage per click:", st.session_state.damage)
    st.write("⚡ Auto damage per second:", st.session_state.auto_damage)