import streamlit as st
import time

st.set_page_config(page_title="Gun Clicker", page_icon="🔫", layout="centered")

st.title("🔫 Gun Clicker")

# --- Game Data ---
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

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()


# --- Auto Income System ---
current_time = time.time()
time_passed = current_time - st.session_state.last_update

if time_passed >= 1:
    st.session_state.money += st.session_state.auto_damage
    st.session_state.last_update = current_time


# --- Big Money Display ---
st.markdown(f"# 💰 ${st.session_state.money}")


# --- Main Click Area ---
st.markdown("## 🔫 CLICK TO SHOOT")

if st.button("🔥 FIRE 🔥", use_container_width=True):
    st.session_state.money += st.session_state.damage
    st.rerun()


st.divider()

# --- Shop Section ---
st.subheader("🏪 Gun Shop")

col1, col2 = st.columns(2)

with col1:
    if st.button(f"Upgrade Gun (+1 damage) - ${st.session_state.upgrade_cost}"):
        if st.session_state.money >= st.session_state.upgrade_cost:
            st.session_state.money -= st.session_state.upgrade_cost
            st.session_state.damage += 1
            st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)
            st.rerun()

with col2:
    if st.button(f"Buy Auto Shooter (+1/sec) - ${st.session_state.auto_cost}"):
        if st.session_state.money >= st.session_state.auto_cost:
            st.session_state.money -= st.session_state.auto_cost
            st.session_state.auto_damage += 1
            st.session_state.auto_cost = int(st.session_state.auto_cost * 1.7)
            st.rerun()


st.divider()

st.write("🔫 Damage per click:", st.session_state.damage)
st.write("⚡ Auto damage per second:", st.session_state.auto_damage)