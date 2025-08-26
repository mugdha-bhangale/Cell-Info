import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🔋 Battery Cell Monitor",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    .cell-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .lfp-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }

    .nmc-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .metric-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }

    .stProgress .st-bo {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'cell_types' not in st.session_state:
    st.session_state.cell_types = []
if 'step' not in st.session_state:
    st.session_state.step = 1

# Header with emojis and colors
st.markdown('<h1 class="main-header">🔋 Battery Cell Monitor Dashboard 🔋</h1>', unsafe_allow_html=True)
st.markdown("### 🌈 Colorful & Interactive Battery Management System ⚡✨")

# Sidebar for controls
with st.sidebar:
    st.header("🎮 Control Panel")

    # Reset button
    if st.button("🔄 Reset All", type="primary"):
        st.session_state.cells_data = {}
        st.session_state.cell_types = []
        st.session_state.step = 1
        st.rerun()

    # Step indicator
    st.markdown("### 📍 Current Step")
    if st.session_state.step == 1:
        st.info("Step 1: Add Battery Cells 🔋")
    else:
        st.success("Step 2: Monitor & Control ⚡")

    # Quick stats
    if st.session_state.cells_data:
        st.markdown("### 📊 Quick Stats")
        total_cells = len(st.session_state.cells_data)
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])

        st.metric("Total Cells", total_cells, delta=None)
        st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
        st.metric("Total Capacity", f"{total_capacity:.2f} Ah")

# Step 1: Cell Type Input
if st.session_state.step == 1:
    st.markdown("## 🔋 Step 1: Add Your Battery Cells")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### Choose Cell Types")
        st.markdown("Select **LFP** (Lithium Iron Phosphate) or **NMC** (Nickel Manganese Cobalt)")

        # Cell type selection
        cell_type_options = ["Select cell type...", "LFP", "NMC"]
        selected_type = st.selectbox(
            f"🔋 Cell #{len(st.session_state.cell_types) + 1} Type:",
            cell_type_options,
            key=f"cell_type_{len(st.session_state.cell_types)}"
        )

        if st.button("➕ Add Cell",
                     disabled=(selected_type == "Select cell type..." or len(st.session_state.cell_types) >= 8)):
            cell_type = selected_type.lower()
            st.session_state.cell_types.append(cell_type)

            # Generate cell data
            cell_key = f"cell_{len(st.session_state.cell_types)}_{cell_type}"
            voltage = 3.2 if cell_type == "lfp" else 3.6
            min_voltage = 2.8 if cell_type == "lfp" else 3.2
            max_voltage = 3.6 if cell_type == "lfp" else 4.0
            temp = round(random.uniform(25, 40), 1)

            st.session_state.cells_data[cell_key] = {
                "voltage": voltage,
                "current": 0.0,
                "temp": temp,
                "capacity": 0.0,
                "min_voltage": min_voltage,
                "max_voltage": max_voltage,
                "type": cell_type
            }
            st.rerun()

    # Display added cells
    if st.session_state.cell_types:
        st.markdown("### 🎯 Added Cells Preview")

        cols = st.columns(min(4, len(st.session_state.cell_types)))
        for idx, cell_type in enumerate(st.session_state.cell_types):
            with cols[idx % 4]:
                card_class = "lfp-card" if cell_type == "lfp" else "nmc-card"
                emoji = "🟢" if cell_type == "lfp" else "🟣"
                st.markdown(f"""
                <div class="cell-card {card_class}">
                    <h3>{emoji} Cell #{idx + 1}</h3>
                    <p><strong>Type:</strong> {cell_type.upper()}</p>
                    <p><strong>Status:</strong> Ready ✅</p>
                </div>
                """, unsafe_allow_html=True)

        # Progress bar
        progress = len(st.session_state.cell_types) / 8
        st.progress(progress)
        st.markdown(f"**Progress:** {len(st.session_state.cell_types)}/8 cells added")

        # Continue button
        if st.button("🚀 Continue to Monitoring Dashboard", type="primary"):
            st.session_state.step = 2
            st.rerun()

# Step 2: Current Input and Monitoring
elif st.session_state.step == 2:
    st.markdown("## ⚡ Step 2: Battery Monitoring Dashboard")

    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Back to Cell Setup"):
            st.session_state.step = 1
            st.rerun()

    # Current input section
    st.markdown("### 🔧 Set Current Values")

    # Create columns for cell controls
    cell_keys = list(st.session_state.cells_data.keys())
    cols = st.columns(min(3, len(cell_keys)))

    for idx, cell_key in enumerate(cell_keys):
        cell = st.session_state.cells_data[cell_key]
        with cols[idx % 3]:
            emoji = "🟢" if cell['type'] == "lfp" else "🟣"
            st.markdown(f"#### {emoji} {cell_key.replace('_', ' ').title()}")

            # Current input
            new_current = st.number_input(
                "Current (A):",
                min_value=0.0,
                max_value=100.0,
                value=cell['current'],
                step=0.1,
                key=f"current_{cell_key}"
            )

            if new_current != cell['current']:
                st.session_state.cells_data[cell_key]['current'] = new_current
                st.session_state.cells_data[cell_key]['capacity'] = round(cell['voltage'] * new_current, 2)

    # Real-time monitoring cards
    st.markdown("### 📊 Real-Time Cell Monitoring")

    for cell_key, cell in st.session_state.cells_data.items():
        col1, col2, col3, col4 = st.columns(4)

        card_color = "#38ef7d" if cell['type'] == "lfp" else "#764ba2"

        with col1:
            st.metric(
                label=f"🔋 {cell_key.replace('_', ' ').title()}",
                value=f"{cell['voltage']}V",
                delta=None
            )

        with col2:
            st.metric(
                label="⚡ Current",
                value=f"{cell['current']}A",
                delta=None
            )

        with col3:
            st.metric(
                label="🌡️ Temperature",
                value=f"{cell['temp']}°C",
                delta=None
            )

        with col4:
            st.metric(
                label="✨ Capacity",
                value=f"{cell['capacity']} Ah",
                delta=None
            )

        # Battery level indicator
        battery_level = min(100, (cell['capacity'] / 10) * 100) if cell['capacity'] > 0 else 0
        st.progress(battery_level / 100)

        st.markdown("---")

    # Visualizations
    st.markdown("### 📈 Data Visualizations")

    if st.session_state.cells_data:
        # Create dataframe for plotting
        df_data = []
        for cell_key, cell in st.session_state.cells_data.items():
            df_data.append({
                'Cell': cell_key.replace('_', ' ').title(),
                'Voltage (V)': cell['voltage'],
                'Current (A)': cell['current'],
                'Temperature (°C)': cell['temp'],
                'Capacity (Ah)': cell['capacity'],
                'Type': cell['type'].upper()
            })

        df = pd.DataFrame(df_data)

        # Create visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Voltage vs Current scatter plot
            fig1 = px.scatter(
                df,
                x='Voltage (V)',
                y='Current (A)',
                color='Type',
                size='Capacity (Ah)',
                hover_data=['Temperature (°C)'],
                title="🔋 Voltage vs Current Analysis",
                color_discrete_map={'LFP': '#38ef7d', 'NMC': '#764ba2'}
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Temperature distribution
            fig2 = px.bar(
                df,
                x='Cell',
                y='Temperature (°C)',
                color='Type',
                title="🌡️ Temperature Distribution",
                color_discrete_map={'LFP': '#38ef7d', 'NMC': '#764ba2'}
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Capacity overview
        fig3 = go.Figure(data=[
            go.Bar(
                name='Current Capacity',
                x=df['Cell'],
                y=df['Capacity (Ah)'],
                marker_color=['#38ef7d' if t == 'LFP' else '#764ba2' for t in df['Type']]
            )
        ])

        fig3.update_layout(
            title="✨ Cell Capacity Overview",
            xaxis_title="Battery Cells",
            yaxis_title="Capacity (Ah)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        st.plotly_chart(fig3, use_container_width=True)

        # Data table
        st.markdown("### 📋 Detailed Cell Data")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# Footer with fun emojis
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <h3>🎉 Battery Monitoring Complete! 🎉</h3>
    <p>⚡ Powered by Streamlit 🚀 Built with ❤️ 🔋</p>
    <p>🌟 ✨ 💫 ⭐ 🎯 💎 🔥 🌈 🎨 🎪</p>
</div>
""", unsafe_allow_html=True)