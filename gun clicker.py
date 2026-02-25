import streamlit as st
import time

st.set_page_config(page_title="Gun Clicker", page_icon="🔫", layout="wide")
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

# --- Auto shooter ---
current_time = time.time()
elapsed = current_time - st.session_state.last_time
if elapsed >= 1:
    st.session_state.money += st.session_state.auto_damage
    st.session_state.last_time = current_time

# --- Layout ---
col1, col2 = st.columns([2,1])

with col1:
    # Display smaller gun image
    st.image("gun.png", width=200)  # width = 200 pixels, adjust to make it smaller
    
    # Big button under image (same width as image)
    if st.button("CLICK THE GUN 🔫", key="gun_click", use_container_width=True):
        st.session_state.money += st.session_state.damage
        st.session_state.floating_messages.append(f"+{st.session_state.damage}")

    # Display money
    st.markdown(f"**💰 Money: ${st.session_state.money}**")

    # Show last 3 floating messages
    for msg in st.session_state.floating_messages[-3:]:
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