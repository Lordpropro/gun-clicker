import streamlit as st

st.set_page_config(page_title="Gun Clicker", page_icon="🔫")

st.title("🔫 Gun Clicker")

# --- Game Data ---
if "money" not in st.session_state:
    st.session_state.money = 0

if "damage" not in st.session_state:
    st.session_state.damage = 1

if "upgrade_cost" not in st.session_state:
    st.session_state.upgrade_cost = 10

if "level" not in st.session_state:
    st.session_state.level = 1


# --- Layout Columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Stats")
    st.write("💰 Money:", st.session_state.money)
    st.write("🔫 Damage:", st.session_state.damage)
    st.write("⭐ Level:", st.session_state.level)

with col2:
    st.subheader("Actions")
    
    if st.button("FIRE 🔥"):
        st.session_state.money += st.session_state.damage
        
        # Level up at 100 money
        if st.session_state.money >= 100:
            st.session_state.level = 2

    if st.button(f"Upgrade Gun (${st.session_state.upgrade_cost})"):
        if st.session_state.money >= st.session_state.upgrade_cost:
            st.session_state.money -= st.session_state.upgrade_cost
            st.session_state.damage += 1
            st.session_state.upgrade_cost += 10