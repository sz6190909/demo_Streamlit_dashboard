"""
Streamlit Visualization & Analytics Powerhouse Showcase
======================================================
This application demonstrates the extensive data visualization and interactive capabilities of Streamlit.
Features showcased:
1. Native Streamlit charts (line, area, bar, scatter)
2. Interactive Plotly charts (Financial Candlestick, 3D Scatter, Sunburst)
3. Altair cross-filtering & linked interval brushing
4. PyDeck 3D Geospatial elevation layers
5. Seaborn & Matplotlib statistical matrices and distributions
6. Interactive DataFrame with sparklines & progress columns
7. Live streaming / real-time data simulation with st.empty() and add_rows()
"""

import time
from datetime import datetime, timedelta
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import seaborn as sns
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Streamlit Visualization Showcase",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished cards and aesthetic touches
st.markdown(
    """
    <style>
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 8px 16px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. Synthetic Data Generators (Cached for high performance)
# -----------------------------------------------------------------------------
@st.cache_data
def generate_timeseries_data(days: int = 90, noise_factor: float = 1.0):
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # Random walk with momentum
    trend = np.linspace(50, 150, days)
    sales = trend + np.cumsum(np.random.randn(days) * 3 * noise_factor)
    marketing_spend = (trend * 0.4) + np.random.randn(days) * 5 * noise_factor
    users = np.clip((sales * 15) + np.random.randn(days) * 50, a_min=100, a_max=None)
    
    return pd.DataFrame({
        "Date": dates,
        "Revenue ($k)": np.round(sales, 2),
        "Marketing Spend ($k)": np.round(np.clip(marketing_spend, 5, None), 2),
        "Active Users": np.round(users).astype(int),
        "Region": np.random.choice(["North America", "Europe", "Asia-Pacific", "Latin America"], size=days),
    })

@st.cache_data
def generate_category_data():
    categories = ["SaaS Enterprise", "Cloud Storage", "AI API", "Security", "DevOps Tools"]
    regions = ["Americas", "EMEA", "APAC"]
    
    rows = []
    np.random.seed(99)
    for cat in categories:
        for reg in regions:
            revenue = np.random.randint(50_000, 500_000)
            profit = int(revenue * np.random.uniform(0.18, 0.45))
            satisfaction = np.round(np.random.uniform(7.8, 9.8), 1)
            rows.append({
                "Category": cat,
                "Region": reg,
                "Revenue": revenue,
                "Profit": profit,
                "CSAT Score": satisfaction,
                "Headcount": np.random.randint(10, 80),
            })
    return pd.DataFrame(rows)

@st.cache_data
def generate_geospatial_data(n_points: int = 600):
    np.random.seed(77)
    # Centered around San Francisco Bay Area tech corridor
    latitudes = 37.7749 + np.random.randn(n_points) * 0.08
    longitudes = -122.4194 + np.random.randn(n_points) * 0.08
    severities = np.random.randint(10, 100, size=n_points)
    
    return pd.DataFrame({
        "lat": latitudes,
        "lon": longitudes,
        "activity_weight": severities,
    })

# -----------------------------------------------------------------------------
# 3. Sidebar Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://streamlit.io/images/brand/streamlit-mark-color.svg",
        width=48,
    )
    st.title("Streamlit Studio")
    st.caption("Exploring the visualization power & reactivity of Streamlit.")
    
    st.markdown("---")
    st.subheader("⚙️ Global Parameters")
    
    time_window = st.slider("Time Window (Days)", min_value=30, max_value=180, value=90, step=15)
    noise_level = st.slider("Volatility Factor", min_value=0.2, max_value=3.0, value=1.0, step=0.2)
    selected_regions = st.multiselect(
        "Filter Regions",
        options=["North America", "Europe", "Asia-Pacific", "Latin America"],
        default=["North America", "Europe", "Asia-Pacific", "Latin America"],
    )
    
    st.markdown("---")
    st.markdown(
        """
        **Included Chart Engines:**
        - 📊 Native Streamlit Charts
        - 📈 Plotly Express & Graph Objects
        - 🔬 Altair Cross-Filtering
        - 🗺️ PyDeck 3D Hexagon Geospatial
        - 🎨 Seaborn / Matplotlib Heatmaps
        - ⚡ Live Reactive Streaming
        """
    )
    
    st.info("💡 Adjust any sidebar control to witness instantaneous UI reactivity across all tabs!")

# Fetch filtered data
raw_ts_data = generate_timeseries_data(days=time_window, noise_factor=noise_level)
ts_data = raw_ts_data[raw_ts_data["Region"].isin(selected_regions)]
if ts_data.empty:
    st.warning("No data matches the selected region filter. Showing all regions.")
    ts_data = raw_ts_data

cat_data = generate_category_data()
geo_data = generate_geospatial_data(n_points=500)

# -----------------------------------------------------------------------------
# 4. Header & Executive KPI Metrics
# -----------------------------------------------------------------------------
st.title("⚡ Streamlit Power Showcase: Plots & Graphs")
st.markdown(
    "Experience why Streamlit is one of the world's most loved frameworks for data science, "
    "interactive dashboards, and machine learning visualization."
)

col1, col2, col3, col4 = st.columns(4)

total_revenue = ts_data["Revenue ($k)"].sum()
prev_revenue = total_revenue * 0.91
avg_users = int(ts_data["Active Users"].mean())
csat_avg = cat_data["CSAT Score"].mean()
total_profit = cat_data["Profit"].sum()

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.0f}k",
        delta=f"+{((total_revenue - prev_revenue) / prev_revenue)*100:.1f}% vs last cycle",
    )
with col2:
    st.metric(
        label="Avg Active Users",
        value=f"{avg_users:,}",
        delta="+8.4%",
    )
with col3:
    st.metric(
        label="Customer CSAT",
        value=f"{csat_avg:.1f} / 10",
        delta="★ Top Tier",
    )
with col4:
    st.metric(
        label="Net Operating Profit",
        value=f"${total_profit / 1000:,.1f}k",
        delta="+14.2% YoY",
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Interactive Charting Showcases (Tabbed Layout)
# -----------------------------------------------------------------------------
tab_native, tab_plotly, tab_altair, tab_geo, tab_sns, tab_streaming, tab_table = st.tabs([
    "⚡ Native Streamlit",
    "🌌 Plotly (3D & Interactive)",
    "🔗 Altair Linked Brushing",
    "🗺️ PyDeck 3D Geospatial",
    "🎨 Seaborn & Matplotlib",
    "⏱️ Live Real-Time Stream",
    "📋 Rich Data Table",
])

# -----------------------------------------------------------------------------
# TAB 1: Native Streamlit Charts
# -----------------------------------------------------------------------------
with tab_native:
    st.subheader("1. Native High-Performance Charts")
    st.write(
        "Streamlit includes lightning-fast built-in chart types that require zero boilerplate "
        "and automatically adapt to light/dark themes."
    )
    
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        st.markdown("#### `st.line_chart` & `st.area_chart`")
        line_df = ts_data.groupby("Date")[["Revenue ($k)", "Marketing Spend ($k)"]].mean()
        st.line_chart(line_df, use_container_width=True)
        st.area_chart(line_df["Marketing Spend ($k)"], use_container_width=True)
        
    with subcol2:
        st.markdown("#### `st.scatter_chart` & `st.bar_chart`")
        st.scatter_chart(
            ts_data,
            x="Marketing Spend ($k)",
            y="Revenue ($k)",
            color="Region",
            size="Active Users",
            use_container_width=True,
        )
        bar_df = cat_data.groupby("Category")[["Revenue", "Profit"]].sum()
        st.bar_chart(bar_df, use_container_width=True)

    with st.expander("🔍 How this was built in Streamlit"):
        st.code(
            """# One-liner native charts:
st.line_chart(df.groupby("Date")[["Revenue", "Spend"]].mean())
st.scatter_chart(df, x="Spend", y="Revenue", color="Region", size="Users")
st.bar_chart(df.groupby("Category")[["Revenue", "Profit"]].sum())
""",
            language="python",
        )

# -----------------------------------------------------------------------------
# TAB 2: Plotly Express & Graph Objects (3D, Financial & Hierarchical)
# -----------------------------------------------------------------------------
with tab_plotly:
    st.subheader("2. Plotly Interactive Visualizations")
    st.write("Plotly provides smooth hover cards, interactive zooming, box selection, and rich 3D graphs.")
    
    pcol1, pcol2 = st.columns(2)
    
    with pcol1:
        st.markdown("#### Interactive 3D Scatter (Revenue vs Spend vs Users)")
        fig_3d = px.scatter_3d(
            ts_data,
            x="Marketing Spend ($k)",
            y="Revenue ($k)",
            z="Active Users",
            color="Region",
            size="Revenue ($k)",
            hover_name="Date",
            opacity=0.85,
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
        fig_3d.update_layout(
            margin=dict(l=0, r=0, b=0, t=20),
            scene=dict(
                xaxis_title="Spend ($k)",
                yaxis_title="Revenue ($k)",
                zaxis_title="Active Users",
            ),
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with pcol2:
        st.markdown("#### Hierarchical Breakdown (Sunburst: Category → Region)")
        fig_sunburst = px.sunburst(
            cat_data,
            path=["Category", "Region"],
            values="Revenue",
            color="Profit",
            color_continuous_scale="RdYlGn",
            hover_data=["CSAT Score"],
        )
        fig_sunburst.update_layout(margin=dict(l=0, r=0, b=0, t=20))
        st.plotly_chart(fig_sunburst, use_container_width=True)

    st.markdown("#### Financial Candlestick / Volatility Trend with Range Slider")
    # Generate synthetic candlestick bars
    candle_dates = pd.date_range(end=datetime.today(), periods=45)
    base_price = 140.0
    opens = []
    highs = []
    lows = []
    closes = []
    curr = base_price
    for _ in range(45):
        change = np.random.randn() * 3
        o = curr
        c = curr + change
        h = max(o, c) + abs(np.random.randn() * 1.5)
        l = min(o, c) - abs(np.random.randn() * 1.5)
        opens.append(o)
        closes.append(c)
        highs.append(h)
        lows.append(l)
        curr = c
        
    fig_candle = go.Figure(
        data=[
            go.Candlestick(
                x=candle_dates,
                open=opens,
                high=highs,
                low=lows,
                close=closes,
                increasing_line_color="#00CC96",
                decreasing_line_color="#EF553B",
            )
        ]
    )
    fig_candle.update_layout(
        xaxis_rangeslider_visible=True,
        margin=dict(l=0, r=0, b=0, t=20),
        height=380,
    )
    st.plotly_chart(fig_candle, use_container_width=True)

    with st.expander("🔍 View Plotly Code Recipe"):
        st.code(
            """import plotly.express as px
import plotly.graph_objects as go

# 3D Scatter:
fig_3d = px.scatter_3d(df, x="Spend", y="Revenue", z="Users", color="Region")
st.plotly_chart(fig_3d, use_container_width=True)

# Sunburst:
fig_sunburst = px.sunburst(cat_df, path=["Category", "Region"], values="Revenue", color="Profit")
st.plotly_chart(fig_sunburst, use_container_width=True)

# Candlestick:
fig_candle = go.Figure(data=[go.Candlestick(x=dates, open=opens, high=highs, low=lows, close=closes)])
st.plotly_chart(fig_candle, use_container_width=True)
""",
            language="python",
        )

# -----------------------------------------------------------------------------
# TAB 3: Altair Linked Brushing & Cross-Filtering
# -----------------------------------------------------------------------------
with tab_altair:
    st.subheader("3. Altair Linked Interval Brushing & Cross-Filtering")
    st.info("👉 **Try it:** Click and drag a selection rectangle across the scatter plot on the left. Watch how the right bar chart dynamically filters!")
    
    # Create an Altair interval selection brush
    brush = alt.selection_interval(name="brush")
    
    scatter_chart = (
        alt.Chart(cat_data)
        .mark_circle(size=120)
        .encode(
            x=alt.X("Revenue:Q", title="Revenue ($)"),
            y=alt.Y("Profit:Q", title="Profit ($)"),
            color=alt.condition(brush, "Category:N", alt.value("lightgray")),
            tooltip=["Category", "Region", "Revenue", "Profit", "CSAT Score"],
        )
        .add_params(brush)
        .properties(title="Drag to Highlight Points (Scatter)", height=380)
    )
    
    bar_chart = (
        alt.Chart(cat_data)
        .mark_bar()
        .encode(
            x=alt.X("sum(Revenue):Q", title="Total Selected Revenue ($)"),
            y=alt.Y("Category:N", sort="-x", title="Product Category"),
            color=alt.Color("Category:N", legend=None),
            tooltip=["Category", "sum(Revenue):Q"],
        )
        .transform_filter(brush)
        .properties(title="Dynamically Filtered Totals", height=380)
    )
    
    linked_charts = alt.hconcat(scatter_chart, bar_chart).resolve_scale(color="independent")
    st.altair_chart(linked_charts, use_container_width=True)
    
    with st.expander("🔍 View Altair Brushing Recipe"):
        st.code(
            """import altair as alt

brush = alt.selection_interval(name="brush")

scatter = (
    alt.Chart(df).mark_circle(size=100)
    .encode(
        x="Revenue:Q",
        y="Profit:Q",
        color=alt.condition(brush, "Category:N", alt.value("lightgray"))
    )
    .add_params(brush)
)

bars = (
    alt.Chart(df).mark_bar()
    .encode(x="sum(Revenue):Q", y="Category:N")
    .transform_filter(brush)
)

st.altair_chart(scatter | bars, use_container_width=True)
""",
            language="python",
        )

# -----------------------------------------------------------------------------
# TAB 4: PyDeck 3D Geospatial Visualization
# -----------------------------------------------------------------------------
with tab_geo:
    st.subheader("4. PyDeck 3D Geospatial Density & Elevation Layers")
    st.write(
        "Render complex 3D maps using WebGL-powered PyDeck. "
        "Hold `Ctrl` (or right-click) and drag the map below to rotate the 3D pitch and camera angle!"
    )
    
    gcol1, gcol2 = st.columns([1, 3])
    with gcol1:
        hex_radius = st.slider("Hexagon Grid Radius (meters)", min_value=100, max_value=800, value=300, step=50)
        elevation_scale = st.slider("3D Elevation Multiplier", min_value=1, max_value=25, value=10, step=1)
        show_points = st.checkbox("Overlay Scatter Points Layer", value=True)
    
    layers = [
        pdk.Layer(
            "HexagonLayer",
            data=geo_data,
            get_position="[lon, lat]",
            radius=hex_radius,
            elevation_scale=elevation_scale,
            elevation_range=[0, 1500],
            extruded=True,
            coverage=0.9,
            pickable=True,
            auto_highlight=True,
        ),
    ]
    
    if show_points:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=geo_data,
                get_position="[lon, lat]",
                get_color="[255, 75, 75, 160]",
                get_radius=120,
                pickable=True,
            )
        )
    
    with gcol2:
        deck = pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            initial_view_state=pdk.ViewState(
                latitude=37.7749,
                longitude=-122.4194,
                zoom=11.2,
                pitch=50,
                bearing=-20,
            ),
            layers=layers,
            tooltip={"text": "Activity Density\nElevation: {elevationValue}"},
        )
        st.pydeck_chart(deck, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: Seaborn & Matplotlib (Statistical Deep-Dive)
# -----------------------------------------------------------------------------
with tab_sns:
    st.subheader("5. Statistical Analysis with Seaborn & Matplotlib")
    st.write("Streamlit effortlessly displays standard Python visualization libraries via `st.pyplot()`.")
    
    scol1, scol2 = st.columns(2)
    
    with scol1:
        st.markdown("#### Correlation Matrix Heatmap")
        corr_matrix = ts_data[["Revenue ($k)", "Marketing Spend ($k)", "Active Users"]].corr()
        
        fig_heat, ax_heat = plt.subplots(figsize=(6, 4))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="crest",
            linewidths=1,
            cbar=True,
            ax=ax_heat,
            square=True,
        )
        ax_heat.set_title("Metric Correlations", fontsize=12, pad=10)
        st.pyplot(fig_heat, use_container_width=True)
        plt.close(fig_heat)

    with scol2:
        st.markdown("#### Distribution / KDE Plot (Revenue by Region)")
        fig_kde, ax_kde = plt.subplots(figsize=(6, 4))
        sns.kdeplot(
            data=ts_data,
            x="Revenue ($k)",
            hue="Region",
            common_norm=False,
            fill=True,
            alpha=0.3,
            palette="Set2",
            ax=ax_kde,
        )
        ax_kde.set_title("Kernel Density Estimation", fontsize=12, pad=10)
        ax_kde.set_ylabel("Density")
        st.pyplot(fig_kde, use_container_width=True)
        plt.close(fig_kde)

# -----------------------------------------------------------------------------
# TAB 6: Live Real-Time Stream Simulation
# -----------------------------------------------------------------------------
with tab_streaming:
    st.subheader("6. Real-Time Streaming & Dynamic Mutation")
    st.write(
        "Streamlit can update and append data in real-time using `chart.add_rows()` and `st.empty()`. "
        "Click the button below to simulate high-frequency incoming sensor / market ticks."
    )
    
    run_stream = st.button("🚀 Start Live Stream Simulation", key="btn_stream")
    stream_placeholder = st.empty()
    status_placeholder = st.empty()
    progress_bar = st.empty()
    
    if run_stream:
        # Initialize streaming chart with initial baseline data
        stream_df = pd.DataFrame(
            np.random.randn(20, 2) + [100, 100],
            columns=["Sensor Alpha (Hz)", "Sensor Beta (Hz)"],
        )
        chart = stream_placeholder.line_chart(stream_df)
        
        for step in range(1, 26):
            time.sleep(0.12)
            # Generate new data point
            new_row = pd.DataFrame(
                np.random.randn(1, 2) * 1.5 + [stream_df.iloc[-1, 0] + np.random.randn() * 0.5,
                                               stream_df.iloc[-1, 1] + np.random.randn() * 0.5],
                columns=["Sensor Alpha (Hz)", "Sensor Beta (Hz)"],
            )
            chart.add_rows(new_row)
            
            # Update status
            progress_bar.progress(step / 25)
            status_placeholder.markdown(
                f"**Incoming Stream Active:** Processed packet `{step}/25` | "
                f"Alpha: `{new_row.iloc[0, 0]:.2f}` | Beta: `{new_row.iloc[0, 1]:.2f}`"
            )
            
        status_placeholder.success("✅ Real-time simulation stream concluded successfully!")
        progress_bar.empty()
    else:
        st.caption("Press 'Start Live Stream Simulation' above to witness dynamic frame updates without full page reloads.")

# -----------------------------------------------------------------------------
# TAB 7: Rich Interactive Data Table
# -----------------------------------------------------------------------------
with tab_table:
    st.subheader("7. Interactive DataFrame with Embedded Sparklines & Progress Bars")
    st.write(
        "Streamlit's `st.dataframe` supports rich column configurations, including embedded mini trend lines, "
        "currency formatters, and visual progress gauges."
    )
    
    # Generate aggregated summary with trend history for sparklines
    summary_list = []
    np.random.seed(123)
    for cat in cat_data["Category"].unique():
        sub = cat_data[cat_data["Category"] == cat]
        rev = sub["Revenue"].sum()
        prof = sub["Profit"].sum()
        margin = int((prof / rev) * 100)
        # Create a mini 14-day history array for the sparkline
        trend_sparkline = (np.cumsum(np.random.randn(14)) + 50).tolist()
        
        summary_list.append({
            "Product Category": cat,
            "Total Revenue": rev,
            "Operating Profit": prof,
            "Profit Margin": margin,
            "Quarterly CSAT": sub["CSAT Score"].mean(),
            "30-Day Momentum": trend_sparkline,
        })
    
    rich_table_df = pd.DataFrame(summary_list)
    
    st.dataframe(
        rich_table_df,
        column_config={
            "Product Category": st.column_config.TextColumn("Category", width="medium"),
            "Total Revenue": st.column_config.NumberColumn("Total Revenue", format="$%d"),
            "Operating Profit": st.column_config.NumberColumn("Profit", format="$%d"),
            "Profit Margin": st.column_config.ProgressColumn(
                "Margin %",
                help="Operating profit margin ratio",
                format="%d%%",
                min_value=0,
                max_value=60,
            ),
            "Quarterly CSAT": st.column_config.NumberColumn(
                "Avg CSAT",
                format="%.1f / 10",
            ),
            "30-Day Momentum": st.column_config.LineChartColumn(
                "Trend Sparkline",
                help="Historical trend line rendered inside cell",
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("Crafted with Streamlit • Run with: `streamlit run main.py`")
