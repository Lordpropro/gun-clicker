
Copy

import streamlit as st
import time
import random

st.set_page_config(
    page_title="Gun Clicker",
    page_icon="🔫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── THEME & GLOBAL CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

/* Dark military theme */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a0a0f !important;
    color: #e0e0e0 !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at top, #1a1a2e 0%, #0a0a0f 60%) !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Typography ── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Orbitron', monospace !important;
    color: #ff4444 !important;
    text-shadow: 0 0 20px rgba(255,68,68,0.5);
}

/* ── Money Display ── */
.money-display {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    color: #ffd700;
    text-shadow: 0 0 30px rgba(255,215,0,0.6);
    text-align: center;
    padding: 12px 20px;
    background: linear-gradient(135deg, #1a1208, #2a1f0a);
    border: 2px solid #ffd700;
    border-radius: 8px;
    margin-bottom: 6px;
}

.per-second {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: #aaa;
    text-align: center;
    margin-bottom: 14px;
}

/* ── Main Gun Button ── */
div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div button {
    background: linear-gradient(145deg, #1c0505, #2d0808) !important;
    border: 3px solid #ff4444 !important;
    border-radius: 50% !important;
    width: 260px !important;
    height: 260px !important;
    box-shadow: 0 0 40px rgba(255,68,68,0.4), inset 0 0 20px rgba(255,68,68,0.1) !important;
    transition: all 0.08s ease !important;
    cursor: crosshair !important;
    color: white !important;
    margin: auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
}
div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div button:hover {
    transform: scale(1.07) !important;
    box-shadow: 0 0 60px rgba(255,68,68,0.7), inset 0 0 30px rgba(255,68,68,0.2) !important;
    border-color: #ff6666 !important;
    color: white !important;
}
div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div button:active {
    transform: scale(0.92) !important;
    box-shadow: 0 0 20px rgba(255,68,68,0.3) !important;
}
div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div button p {
    font-size: 8rem !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    color: white !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* ── Shop Cards ── */
.shop-card {
    background: linear-gradient(135deg, #12121c, #1a1a2e);
    border: 1px solid #333355;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.shop-card:hover { border-color: #5555aa; }
.shop-card-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    color: #aaaaff;
    font-weight: 700;
}
.shop-card-desc {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.82rem;
    color: #888;
    margin: 2px 0 6px 0;
}
.shop-card-cost {
    font-family: 'Orbitron', monospace;
    font-size: 0.95rem;
    color: #ffd700;
    font-weight: 700;
}
.shop-card-owned {
    font-size: 0.78rem;
    color: #666;
    float: right;
}

/* ── Upgrade buttons ── */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1a1a2e, #16162a) !important;
    color: #ccc !important;
    border: 1px solid #334 !important;
    border-radius: 6px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    transition: all 0.15s !important;
    width: 100% !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #22223e, #1e1e38) !important;
    border-color: #5566bb !important;
    color: #fff !important;
}

/* ── Milestone popup ── */
.milestone {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    color: #ffd700;
    background: linear-gradient(135deg, #1a1208, #2a2008);
    border: 2px solid #ffd700;
    border-radius: 8px;
    padding: 10px;
    margin: 8px 0;
    animation: glow 1.5s ease-in-out infinite alternate;
}
@keyframes glow {
    from { box-shadow: 0 0 10px rgba(255,215,0,0.3); }
    to   { box-shadow: 0 0 30px rgba(255,215,0,0.8); }
}

/* ── Stats panel ── */
.stat-row {
    font-family: 'Rajdhani', sans-serif;
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid #1a1a2a;
    font-size: 0.9rem;
}
.stat-label { color: #888; }
.stat-value { color: #ccc; font-weight: 600; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    color: #888 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #ff4444 !important;
    border-bottom: 2px solid #ff4444 !important;
}

/* Section headers */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    color: #ff4444;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1px solid #330000;
    padding-bottom: 4px;
    margin: 12px 0 8px 0;
}

/* Divider */
hr { border-color: #1a1a2e !important; }

/* Notification */
.notif {
    background: #0d1a0d;
    border: 1px solid #22aa22;
    border-radius: 6px;
    padding: 6px 12px;
    font-family: 'Rajdhani', sans-serif;
    color: #44ff44;
    font-size: 0.9rem;
    margin: 4px 0;
}
.notif-warn {
    background: #1a0d0d;
    border: 1px solid #aa2222;
    color: #ff6666;
}

/* Floating numbers area */
.floats-area {
    min-height: 60px;
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 1.2rem;
    color: #ff4444;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ─── GAME DATA ────────────────────────────────────────────────────────────────

BUILDINGS = [
    {"id": "lookout",   "name": "Lookout",        "icon": "👁️",  "base_cost": 15,   "base_dps": 0.1,  "desc": "A scout watches the perimeter."},
    {"id": "pistol",    "name": "Pistol Rack",     "icon": "🔫",  "base_cost": 100,  "base_dps": 0.5,  "desc": "Automated pistols fire steadily."},
    {"id": "rifle",     "name": "Rifle Range",     "icon": "🎯",  "base_cost": 500,  "base_dps": 3,    "desc": "Precision rifles picking off targets."},
    {"id": "turret",    "name": "Auto-Turret",     "icon": "🤖",  "base_cost": 2000, "base_dps": 10,   "desc": "Heavy automated turret system."},
    {"id": "drone",     "name": "Drone Squadron",  "icon": "🚁",  "base_cost": 8000, "base_dps": 40,   "desc": "Aerial drones patrol the skies."},
    {"id": "tank",      "name": "Tank Division",   "icon": "🪖",  "base_cost": 30000,"base_dps": 150,  "desc": "Heavy armour rolls into battle."},
    {"id": "satellite", "name": "War Satellite",   "icon": "🛰️",  "base_cost": 120000,"base_dps":500,  "desc": "Orbital strike capability online."},
]

UPGRADES = [
    # (id, name, icon, cost, description, effect_label)
    {"id": "better_grip",   "name": "Better Grip",       "icon": "🖐️", "cost": 100,    "desc": "+1 click damage",              "type": "click", "value": 1},
    {"id": "hollow_point",  "name": "Hollow Points",     "icon": "💊", "cost": 500,    "desc": "+3 click damage",              "type": "click", "value": 3},
    {"id": "speed_trigger", "name": "Speed Trigger",     "icon": "⚡", "cost": 1000,   "desc": "+5 click damage",              "type": "click", "value": 5},
    {"id": "burst_fire",    "name": "Burst Fire",        "icon": "💥", "cost": 5000,   "desc": "+15 click damage",             "type": "click", "value": 15},
    {"id": "auto_oiler",    "name": "Auto Oiler",        "icon": "🛢️", "cost": 200,    "desc": "Lookouts x2 DPS",              "type": "building_mult", "building": "lookout", "mult": 2},
    {"id": "mag_ext",       "name": "Extended Mags",     "icon": "📦", "cost": 1000,   "desc": "Pistol Racks x2 DPS",          "type": "building_mult", "building": "pistol",  "mult": 2},
    {"id": "scope",         "name": "Sniper Scope",      "icon": "🔭", "cost": 5000,   "desc": "Rifle Ranges x2 DPS",          "type": "building_mult", "building": "rifle",   "mult": 2},
    {"id": "ai_targeting",  "name": "AI Targeting",      "icon": "🧠", "cost": 20000,  "desc": "Auto-Turrets x2 DPS",          "type": "building_mult", "building": "turret",  "mult": 2},
    {"id": "stealth_drone", "name": "Stealth Coating",   "icon": "👻", "cost": 80000,  "desc": "Drone Squadrons x2 DPS",       "type": "building_mult", "building": "drone",   "mult": 2},
    {"id": "reactive_armor","name": "Reactive Armour",   "icon": "🛡️", "cost": 300000, "desc": "Tank Divisions x2 DPS",        "type": "building_mult", "building": "tank",    "mult": 2},
]

MILESTONES = [
    (100,      "🔫 First Blood",      "You dealt your first 100 damage!"),
    (1000,     "💪 Rookie Shooter",   "1,000 damage dealt!"),
    (10000,    "🎖️ Veteran Operator", "10,000 damage dealt!"),
    (100000,   "🏆 Elite Marksman",   "100,000 damage — legend status!"),
    (1000000,  "💀 One-Man Army",     "1,000,000! Unstoppable."),
    (10000000, "☠️ War Machine",      "10,000,000. Nothing survives."),
]


# ─── SESSION STATE INIT ───────────────────────────────────────────────────────

def init():
    defaults = {
        "money": 0,
        "total_earned": 0,
        "click_damage": 1,
        "last_time": time.time(),
        "buildings": {b["id"]: 0 for b in BUILDINGS},
        "upgrades_bought": set(),
        "notifications": [],
        "milestones_seen": set(),
        "total_clicks": 0,
        "last_click_msgs": [],
        "combo": 0,
        "last_click_time": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
s = st.session_state


# ─── COMPUTED STATS ───────────────────────────────────────────────────────────

def building_dps(b_id):
    b = next(x for x in BUILDINGS if x["id"] == b_id)
    dps = b["base_dps"]
    # Apply any bought multiplier upgrades for this building
    for upg in UPGRADES:
        if upg["type"] == "building_mult" and upg["building"] == b_id:
            if upg["id"] in s.upgrades_bought:
                dps *= upg["mult"]
    return dps * s.buildings[b_id]

def total_dps():
    return sum(building_dps(b["id"]) for b in BUILDINGS)

def building_cost(b_id):
    b = next(x for x in BUILDINGS if x["id"] == b_id)
    owned = s.buildings[b_id]
    return int(b["base_cost"] * (1.15 ** owned))

def fmt(n):
    if n >= 1_000_000_000: return f"{n/1_000_000_000:.2f}B"
    if n >= 1_000_000:     return f"{n/1_000_000:.2f}M"
    if n >= 1_000:         return f"{n/1_000:.1f}K"
    return str(int(n))


# ─── AUTO-INCOME TICK ─────────────────────────────────────────────────────────

now = time.time()
elapsed = now - s.last_time
if elapsed >= 1:
    ticks = int(elapsed)
    income = total_dps() * ticks
    s.money += income
    s.total_earned += income
    s.last_time += ticks


# ─── MILESTONE CHECKS ─────────────────────────────────────────────────────────

for threshold, title, desc in MILESTONES:
    if s.total_earned >= threshold and threshold not in s.milestones_seen:
        s.milestones_seen.add(threshold)
        s.notifications.insert(0, ("milestone", f"🏅 {title}: {desc}"))
# trim notifications
s.notifications = s.notifications[:5]


# ─── LAYOUT ──────────────────────────────────────────────────────────────────

st.markdown("<h1 style='text-align:center; font-size:2.5rem; margin-bottom:0;'>🔫 GUN CLICKER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555; font-family:Rajdhani,sans-serif; margin-top:0;'>Click. Upgrade. Dominate.</p>", unsafe_allow_html=True)

left, center, right = st.columns([1.2, 1.6, 1.2])


# ─── LEFT: STATS & BUILDINGS ─────────────────────────────────────────────────

with left:
    st.markdown("<div class='section-header'>📊 Arsenal Status</div>", unsafe_allow_html=True)
    
    dps = total_dps()
    st.markdown(f"""
    <div style='font-family:Rajdhani,sans-serif;'>
    <div class='stat-row'><span class='stat-label'>💰 Total Earned</span><span class='stat-value'>${fmt(int(s.total_earned))}</span></div>
    <div class='stat-row'><span class='stat-label'>⚡ Per Second</span><span class='stat-value'>{dps:.1f}/s</span></div>
    <div class='stat-row'><span class='stat-label'>🖱️ Per Click</span><span class='stat-value'>{s.click_damage}</span></div>
    <div class='stat-row'><span class='stat-label'>🖱️ Total Clicks</span><span class='stat-value'>{fmt(s.total_clicks)}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header' style='margin-top:16px;'>🏗️ Your Buildings</div>", unsafe_allow_html=True)
    for b in BUILDINGS:
        owned = s.buildings[b["id"]]
        if owned > 0:
            bdps = building_dps(b["id"])
            st.markdown(f"""
            <div class='shop-card'>
                <span class='shop-card-title'>{b['icon']} {b['name']}</span>
                <span class='shop-card-owned'>×{owned}</span><br>
                <span class='shop-card-desc'>{bdps:.1f} total DPS</span>
            </div>
            """, unsafe_allow_html=True)

    # Notifications
    if s.notifications:
        st.markdown("<div class='section-header' style='margin-top:14px;'>📢 Intel</div>", unsafe_allow_html=True)
        for kind, msg in s.notifications[-3:]:
            css = "milestone" if kind == "milestone" else "notif"
            st.markdown(f"<div class='{css}'>{msg}</div>", unsafe_allow_html=True)


# ─── CENTER: MAIN CLICK BUTTON ───────────────────────────────────────────────

with center:
    # Money display
    st.markdown(f"<div class='money-display'>💰 ${fmt(int(s.money))}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='per-second'>⚡ {total_dps():.1f} per second &nbsp;|&nbsp; 🖱️ {s.click_damage} per click</div>", unsafe_allow_html=True)

    # Combo display
    combo_now = time.time()
    if combo_now - s.last_click_time < 2 and s.combo >= 5:
        st.markdown(f"<div style='text-align:center; font-family:Orbitron,monospace; color:#ff8800; font-size:1rem; font-weight:700;'>🔥 COMBO x{s.combo}!</div>", unsafe_allow_html=True)

    # Gun click button — emoji overlaid via CSS ::after for guaranteed size
    st.markdown('''
    <div id="gun-click-marker"></div>
    <style>
    div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div {
        display: flex;
        justify-content: center;
        position: relative;
    }
    div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div::after {
        content: "🔫";
        font-size: 9rem;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        z-index: 10;
        line-height: 1;
    }
    div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div button p,
    div[data-testid="stMarkdownContainer"]:has(#gun-click-marker) + div button span {
        opacity: 0 !important;
        font-size: 0 !important;
    }
    </style>
    ''', unsafe_allow_html=True)

    if st.button("🔫", key="gun_btn", use_container_width=False):
        now2 = time.time()
        if now2 - s.last_click_time < 1.0:
            s.combo += 1
        else:
            s.combo = 1
        s.last_click_time = now2
        
        combo_bonus = max(1, s.combo // 5)  # bonus every 5 combo
        total_click = s.click_damage * combo_bonus
        s.money += total_click
        s.total_earned += total_click
        s.total_clicks += 1
        
        msgs = [f"+{total_click}"]
        if s.combo >= 10:
            msgs.append(f"🔥 x{combo_bonus} COMBO!")
        s.last_click_msgs = msgs[-4:]

    # Floating click messages
    if s.last_click_msgs:
        st.markdown("<div class='floats-area'>" + "&nbsp;&nbsp;".join(s.last_click_msgs) + "</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='floats-area'></div>", unsafe_allow_html=True)

    # Milestone banners
    for threshold, title, desc in MILESTONES:
        if s.total_earned >= threshold and threshold in s.milestones_seen:
            # Show the most recent milestone only
            highest = max([t for t, _, _ in MILESTONES if t in s.milestones_seen], default=0)
            if threshold == highest:
                st.markdown(f"<div class='milestone'>🏅 {title}</div>", unsafe_allow_html=True)
            break


# ─── RIGHT: SHOP ─────────────────────────────────────────────────────────────

with right:
    tab1, tab2 = st.tabs(["🏗️ BUILDINGS", "⬆️ UPGRADES"])

    with tab1:
        st.markdown("<div class='section-header'>Buy Buildings</div>", unsafe_allow_html=True)
        for b in BUILDINGS:
            cost = building_cost(b["id"])
            owned = s.buildings[b["id"]]
            can_afford = s.money >= cost
            btn_label = f"{b['icon']} {b['name']} ×{owned}  — 💰${fmt(cost)}"
            
            st.markdown(f"""
            <div class='shop-card'>
                <div class='shop-card-title'>{b['icon']} {b['name']} <span class='shop-card-owned'>×{owned}</span></div>
                <div class='shop-card-desc'>{b['desc']}</div>
                <div class='shop-card-cost'>💰 ${fmt(cost)}</div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_text = f"Buy — ${fmt(cost)}" if can_afford else f"🔒 ${fmt(cost)}"
            if st.button(btn_text, key=f"buy_{b['id']}", disabled=not can_afford):
                s.money -= cost
                s.buildings[b["id"]] += 1
                s.notifications.insert(0, ("info", f"✅ Bought {b['name']}! ({s.buildings[b['id']]} owned)"))

    with tab2:
        st.markdown("<div class='section-header'>Buy Upgrades</div>", unsafe_allow_html=True)
        available = [u for u in UPGRADES if u["id"] not in s.upgrades_bought]
        if not available:
            st.markdown("<p style='color:#555; font-family:Rajdhani;'>All upgrades purchased! 💪</p>", unsafe_allow_html=True)
        for upg in available:
            can_afford = s.money >= upg["cost"]
            st.markdown(f"""
            <div class='shop-card'>
                <div class='shop-card-title'>{upg['icon']} {upg['name']}</div>
                <div class='shop-card-desc'>{upg['desc']}</div>
                <div class='shop-card-cost'>💰 ${fmt(upg['cost'])}</div>
            </div>
            """, unsafe_allow_html=True)
            btn_text = f"Buy — ${fmt(upg['cost'])}" if can_afford else f"🔒 ${fmt(upg['cost'])}"
            if st.button(btn_text, key=f"upg_{upg['id']}", disabled=not can_afford):
                s.money -= upg["cost"]
                s.upgrades_bought.add(upg["id"])
                if upg["type"] == "click":
                    s.click_damage += upg["value"]
                s.notifications.insert(0, ("info", f"✅ Upgrade unlocked: {upg['name']}!"))


# ─── AUTO-REFRESH (for passive income) ───────────────────────────────────────
# Only auto-rerun if there's passive income active
if total_dps() > 0:
    time.sleep(1)
    st.rerun()