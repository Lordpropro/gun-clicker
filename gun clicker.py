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

# --- Auto shooter: passive clicks ---
current_time = time.time()
elapsed = current_time - st.session_state.last_time
if elapsed >= 1:
    st.session_state.money += st.session_state.auto_damage
    st.session_state.last_time = current_time

# --- Layout ---
col1, col2 = st.columns([3,1])  # main area : shop

with col1:
    # Big clickable gun image
    st.image("gun.png", use_column_width=True)  # make sure gun.png is in your folder
    if st.button(" ", key="click"):  # invisible overlay button
        st.session_state.money += st.session_state.damage
        st.session_state.floating_messages.append(f"+{st.session_state.damage}")

    # Display money
    st.markdown(f"### 💰 Money: ${st.session_state.money}")

    # Show last 5 floating messages
    for msg in st.session_state.floating_messages[-5:]:
        st.info(msg)

with col2:
    st.subheader("🏪 Shop")
    
    # Upgrade gun (increase click damage)
    if st.button(f"Upgrade Gun (+1) - ${st.session_state.upgrade_cost}"):
        if st.session_state.money >= st.session_state.upgrade_cost:
            st.session_state.money -= st.session_state.upgrade_cost
            st.session_state.damage += 1
            st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)

    # Buy auto shooter (passive clicks)
    if st.button(f"Buy Auto Shooter (+1/sec) - ${st.session_state.auto_cost}"):
        if st.session_state.money >= st.session_state.auto_cost:
            st.session_state.money -= st.session_state.auto_cost
            st.session_state.auto_damage += 1
            st.session_state.auto_cost = int(st.session_state.auto_cost * 1.7)

    st.write("🔫 Damage per click:", st.session_state.damage)
    st.write("⚡ Auto damage per second:", st.session_state.auto_damage)