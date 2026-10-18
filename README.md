# ⚡ Streamlit Visualization Showcase

An interactive, multi-engine data visualization dashboard built with [Streamlit](https://streamlit.io/) demonstrating charts, interactive controls, and reactive data flows.

## 📊 Features & Showcases

1. **⚡ Native Streamlit Charts**: High-speed line, area, bar, and multidimensional scatter charts.
2. **🌌 Plotly 3D & Financial**: Interactive 3D scatter plots, hierarchical sunburst charts, and financial candlestick charts with range sliders.
3. **🔗 Altair Linked Brushing**: Cross-filtering where selecting points in one chart highlights and filters data in another.
4. **🗺️ PyDeck 3D Geospatial**: WebGL-powered 3D hexagon elevation density maps.
5. **🎨 Seaborn & Matplotlib**: Statistical correlation heatmaps and kernel density estimation (KDE) distributions.
6. **⏱️ Real-Time Live Streaming**: Dynamic mutation and row-appending with `chart.add_rows()` and `st.empty()`.
7. **📋 Rich Data Table**: Sparkline trend history (`LineChartColumn`), progress bars (`ProgressColumn`), and currency formatting.

---

## 🚀 Quickstart

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/sz6190909/demo_Streamlit_dashboard.git
cd demo_Streamlit_dashboard
python -m venv .venv
```

Activate the virtual environment:
- **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run main.py
```
