import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="CAN Bus Signal Monitor", layout="wide")
st.title("🚗 CAN Bus Signal Monitor")
st.caption("AUTOSAR-inspired ECU signal monitoring and fault detection")

@st.cache_data
def load_data():
    return pd.read_csv("signal_log.csv", parse_dates=["time"])

df = load_data()

# ── Top metrics ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Signals Logged", f"{len(df):,}")
col2.metric("Fault Events", f"{len(df[df['fault'] != 'OK']):,}")
col3.metric("Fault Rate", f"{len(df[df['fault'] != 'OK']) / len(df) * 100:.1f}%")
col4.metric("ECUs Monitored", df['ecu'].nunique())

st.divider()

# ── Signal selector ───────────────────────────────────────────
signal = st.selectbox("Select Signal", df['signal'].unique())
df_signal = df[df['signal'] == signal].copy()
df_signal = df_signal.reset_index(drop=True)

# ── Signal plot ───────────────────────────────────────────────
st.subheader(f"Signal: {signal}")

df_ok    = df_signal[df_signal['fault'] == 'OK']
df_fault = df_signal[df_signal['fault'] != 'OK']

import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_ok.index, y=df_ok['value'],
    mode='lines', name='OK',
    line=dict(color='#00CC96', width=1)
))
fig.add_trace(go.Scatter(
    x=df_fault.index, y=df_fault['value'],
    mode='markers', name='FAULT',
    marker=dict(color='red', size=4, symbol='x')
))
fig.update_layout(
    xaxis_title="Sample Index",
    yaxis_title="Signal Value",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h"),
    height=350
)
st.plotly_chart(fig, use_container_width=True)

# ── Fault breakdown ───────────────────────────────────────────
st.divider()
st.subheader("Fault Breakdown by Signal")
fault_df = df[df['fault'] != 'OK'].groupby(['signal','fault']).size().reset_index(name='count')
st.dataframe(fault_df, use_container_width=True)

# ── Raw log ───────────────────────────────────────────────────
st.divider()
with st.expander("View Raw Log"):
    st.dataframe(df.tail(200), use_container_width=True)