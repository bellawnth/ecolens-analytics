import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"

st.set_page_config(
    page_title="EcoLens · Food Footprint",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root {
   --bg:         #f2f8f4;
  --white:      #ffffff;
  --ink:        #0d2116;
  --g1:         #0a4f2e;
  --g2:         #1a7a47;
  --g3:         #2da562;
  --g4:         #3ecc7a;
  --g5:         #72dfa0;
  --g6:         #aff0c8;
  --g7:         #d6f7e6;
  --lime:       #8bc34a;
  --teal:       #00897b;
  --forest:     #1b5e20;
  --olive:      #558b2f;
  --emerald:    #00c853;
  --sage:       #a5d6a7;
  --muted:      #5a7a65;
  --border:     #c8e6d4;
  --coral:      #e53935;
  --amber:      #f9a825;
}
html, body, .stApp, p, label, .stMarkdown {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: #0d2116;
}
.stApp { background: var(--bg) !important; }

.js-plotly-plot svg text,
.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .gtitle,
.js-plotly-plot .legendtext,
.js-plotly-plot .annotation-text,
.js-plotly-plot .bar text,
.js-plotly-plot .textpoint text {
  fill: #0d2116 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── fix plotly hover tooltip ── */
.hoverlayer .hovertext rect { fill: #ffffff !important; stroke: #c8e6d4 !important; }
.hoverlayer .hovertext text { fill: #0d2116 !important; }
.hoverlayer .hovertext path { stroke: #c8e6d4 !important; }

/* ── Hero ── */
.hero {
  background: linear-gradient(135deg, #0a4f2e 0%, #1a7a47 50%, #2da562 100%);
  border-radius: 22px;
  padding: 2.6rem 3rem 2.2rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  right: -80px; top: -80px;
  width: 340px; height: 340px;
  border-radius: 50%;
  background: radial-gradient(circle, #3ecc7a33 0%, transparent 65%);
}
.hero::after {
  content: '';
  position: absolute;
  left: 35%; bottom: -90px;
  width: 280px; height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, #aff0c822 0%, transparent 65%);
}
.hero-badge {
  display: inline-block;
  background: rgba(62,204,122,.25);
  border: 1px solid rgba(62,204,122,.45);
  color: #aff0c8;
  font-size: .68rem; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase;
  padding: .22rem .75rem;
  border-radius: 20px;
  margin-bottom: .9rem;
  font-family: 'Space Grotesk', monospace !important;
}
.hero h1 {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 700;
  color: #fff !important; margin: 0; letter-spacing: -1.5px; line-height: 1;
}
.hero h1 em { color: #72dfa0 !important; font-style: normal; }
.hero p { color: #aff0c8 !important; font-size: .9rem; margin: .55rem 0 0; font-weight: 300; }

/* ── KPI — fixed equal height ── */
.kpi-row { display:flex; gap:1rem; margin-bottom:1.5rem; align-items:stretch; }
.kpi {
  background:var(--white); min-width:0; border-radius:16px;
  padding:1.25rem 1.4rem; flex:1;
  border:1.5px solid var(--border);
  box-shadow:0 2px 16px rgba(10,79,46,.08);
  display:flex; flex-direction:column; justify-content:space-between;
  min-height:110px;
}
.kpi-label {
  font-size:.68rem; color:var(--muted) !important;
  text-transform:uppercase; letter-spacing:.1em; font-weight:700;
  font-family:'Space Grotesk', sans-serif !important;
}
.kpi-val {
  font-family:'Space Grotesk', sans-serif !important;
  font-size:1.8rem;
  font-weight:700;
  color:var(--g1) !important;
  line-height:1.15;
  margin:.2rem 0 .1rem;
  word-break:break-word;
  overflow-wrap:break-word;
}
.kpi-sub { font-size:.75rem; color:#94b8a3 !important; }
.kpi-val.red   { color:var(--coral) !important; }
.kpi-val.amber { color:var(--amber) !important; }
.kpi-val.teal  { color:var(--teal)  !important; }
.kpi-val.lime  { color:#558b2f      !important; }
/* small font for long text KPI */
.kpi-val.sm    { font-size:1.1rem !important; line-height:1.3; }

/* ── Section title ── */
.sec {
  font-family:'Space Grotesk', sans-serif !important;
  font-size:1.02rem; font-weight:700; color:var(--g1) !important;
  border-left:4px solid var(--g3);
  padding:.28rem 0 .28rem .7rem; margin:2rem 0 1rem;
}

/* ── Insight cards ── */
.insight {
  background:var(--white); border-radius:14px;
  padding:1rem 1.25rem; border-left:4px solid var(--g2);
  margin-bottom:.75rem; box-shadow:0 2px 10px rgba(10,79,46,.06);
}
.insight.red   { border-color:var(--coral); }
.insight.amber { border-color:var(--amber); }
.insight.teal  { border-color:var(--teal);  }
.insight-title { font-family:'Space Grotesk',sans-serif !important; font-weight:700; font-size:.92rem; margin-bottom:.35rem; }
.insight-body  { font-size:.82rem; color:#2e5040 !important; line-height:1.65; }

/* ── Swap cards ── */
.swap-card {
  background:var(--white); border:1.5px solid var(--border);
  border-radius:14px; padding:.9rem 1.15rem; margin-bottom:.6rem;
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  box-shadow:0 1px 8px rgba(10,79,46,.05);
}
.swap-cat  { font-size:.67rem; color:var(--muted) !important; text-transform:uppercase; letter-spacing:.07em; font-family:'Space Grotesk',sans-serif !important; margin-bottom:.3rem; }
.swap-from { color:var(--coral) !important; font-weight:700; font-size:.88rem; }
.swap-to   { color:var(--g2) !important;   font-weight:700; font-size:.88rem; }
.swap-save { background:var(--g7); color:var(--g1) !important; border-radius:8px; padding:.22rem .6rem; font-size:.72rem; font-weight:700; white-space:nowrap; border:1px solid var(--g6); font-family:'Space Grotesk',monospace !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background:#0a3320 !important; }
section[data-testid="stSidebar"] { color:#a8d8b8 !important; font-family:'Plus Jakarta Sans',sans-serif !important; }
section[data-testid="stSidebar"] h2 { color:#fff !important; font-family:'Space Grotesk',sans-serif !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label { color:#72dfa0 !important; font-weight:700 !important; font-size:.78rem !important; letter-spacing:.08em !important; text-transform:uppercase !important; }
section[data-testid="stSidebar"] hr { border-color:#1a4d30 !important; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── Colors ────────────────────────────────────────────────────────────────────
INK     = "#0d2116"
G1,G2,G3,G4,G5,G6 = "#0a4f2e","#1a7a47","#2da562","#3ecc7a","#72dfa0","#aff0c8"
LIME    = "#8bc34a"
TEAL    = "#00897b"
OLIVE   = "#558b2f"
CORAL   = "#e53935"
AMBER   = "#f9a825"
GRID    = "#e8f4ed"

PL_FONT = dict(family="Plus Jakarta Sans, sans-serif", color=INK, size=12)
COMMON  = dict(font=PL_FONT, paper_bgcolor="white", plot_bgcolor="white")

# Semantic color per food category
CAT_COLOR = {

    # 🔥 High impact / animal-based
    "Meat & Poultry":      "#D62828",   # premium red
    "Fish & Seafood":      "#1D4ED8",   # deep ocean blue
    "Fast Food":           "#F77F00",   # vibrant orange
    "Dairy Products":      "#9D4EDD",   # vivid purple
    "Eggs":                "#FFB703",   # egg yolk gold

    # 🍰 Sweet / dessert
    "Sweets & Desserts":   "#E91E63",   # hot pink
    "Sweeteners":          "#FF9F1C",   # honey orange

    # 🌾 grains / bakery / oils
    "Fats & Oils":         "#A3A380",   # olive tone
    "Grains & Cereals":    "#8D6E63",   # grain brown
    "Bakery Products":     "#B08968",   # bread beige

    # 🌱 Plant-based
    "Plant-Based Protein": "#2DC653",   # eco green
    "Legumes":             "#55A630",   # bean green
    "Vegetables":          "#38B000",   # fresh green
    "Fruits":              "#FF4D6D",   # fruit watermelon
    "Root Crops":          "#BC6C25",   # earthy orange-brown
    "Nuts & Seeds":        "#7F5539",   # walnut brown

    # 🥤 liquids
    "Beverages":           "#00B4D8",   # aqua blue
    "Soups":               "#2A9D8F",   # teal

    # 🍲 mixed
    "Mixed Dishes":        "#6D597A",   # muted plum
    "Condiments & Sauces": "#8338EC",   # sauce violet
}

HOVER_STYLE = dict(
    bgcolor="white",
    bordercolor="#c8e6d4",
    font=dict(color=INK, size=12, family="Plus Jakarta Sans, sans-serif"),
)

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('final_dataset_footprint_emission.csv')
    df["emisi"] = pd.to_numeric(df["emisi"], errors="coerce")
    return df.dropna(subset=["emisi"])

df = load_data()

SUBSTITUTIONS = [
    {"from":"Beef (Beef Herd)", "to":"Lentils",        "saving":98.5, "cat":"Meat → Legumes"},
    {"from":"Steak",            "to":"Tofu",            "saving":53.2, "cat":"Meat → Plant-Based"},
    {"from":"Lamb & Mutton",    "to":"Chicken",         "saving":35.0, "cat":"Meat & Poultry"},
    {"from":"Chocolate",        "to":"Fresh Fruit",     "saving":46.2, "cat":"Sweets → Fruits"},
    {"from":"Prawn",            "to":"Mussels / Clams", "saving":14.0, "cat":"Fish & Seafood"},
    {"from":"Cheese",           "to":"Hummus",          "saving":11.0, "cat":"Dairy → Legumes"},
    {"from":"Butter",           "to":"Olive Oil",       "saving":2.2,  "cat":"Fats & Oils"},
    {"from":"Whole Milk",       "to":"Oat Milk",        "saving":2.5,  "cat":"Dairy → Grain"},
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌱 EcoLens")
    st.markdown("---")
    all_cats = ["All Categories"] + sorted(df["kategori"].unique().tolist())
    sel_cat = st.selectbox("📂 Filter Category", all_cats)
    top_n = st.slider("🏆 Top / Bottom N", 3, 15, 5)
    show_outliers = st.checkbox("Show extreme outliers (>30 kg)", value=True)
    st.markdown("---")
    st.markdown("**ℹ️ About EcoLens**")
    st.caption("EcoLens estimates CO₂ footprint from food. 290 items · 20 categories · CO₂e/kg food.")
    st.markdown("---")
    st.caption(f"📊 {len(df)} items · {df['kategori'].nunique()} categories")

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = df.copy() if sel_cat == "All Categories" else df[df["kategori"] == sel_cat].copy()
plot_df  = df.copy() if show_outliers else df[df["emisi"] <= 30].copy()
if not show_outliers:
    filtered = filtered[filtered["emisi"] <= 30]

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🌍 Carbon Intelligence Platform</div>
  <h1>🌱 Eco<em>Lens</em></h1>
  <p>Food Carbon Footprint Dashboard · 290 items · 20 categories · CO₂e per kg food</p>
</div>
""", unsafe_allow_html=True)

# ── KPIs — rendered as one flex row so heights match ─────────────────────────
cat_stats = df.groupby("kategori")["emisi"].mean()
max_cat, min_cat = cat_stats.idxmax(), cat_stats.idxmin()

kpi_defs = [
    ("Total Items",       str(len(df)),                  f"{df['kategori'].nunique()} categories", ""),
    ("Avg CO₂",          f"{df['emisi'].mean():.2f}",   "CO₂e / kg food",                     "amber"),
    ("Median CO₂",       f"{df['emisi'].median():.2f}", "CO₂e / kg food",                     "teal"),
    ("Highest Category", max_cat,                        f"{cat_stats[max_cat]:.1f} kg avg",      "red sm"),
    ("Lowest Category",  min_cat,                        f"{cat_stats[min_cat]:.3f} kg avg",      "lime sm"),
]

cards_html = '<div class="kpi-row">'
for lbl, val, sub, cls in kpi_defs:
    cards_html += f"""
    <div class="kpi">
      <div class="kpi-label">{lbl}</div>
      <div class="kpi-val {cls}">{val}</div>
      <div class="kpi-sub">{sub}</div>
    </div>"""
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# ── Row 1: Bar + Donut ────────────────────────────────────────────────────────
st.markdown('<div class="sec">📊 Average CO₂ Emission by Category</div>', unsafe_allow_html=True)
r1a, r1b = st.columns([3, 2])

with r1a:
    cat_avg = df.groupby("kategori")["emisi"].mean().sort_values().reset_index()
    # Color each bar by its semantic category color
    bar_colors = [CAT_COLOR.get(c, G3) for c in cat_avg["kategori"]]

    fig_bar = go.Figure(go.Bar(
        x=cat_avg["emisi"],
        y=cat_avg["kategori"],
        orientation="h",
        marker_color=bar_colors,
        text=[f"{v:.2f}" for v in cat_avg["emisi"]],
        textposition="outside",
        textfont=dict(color=INK, size=11, family="Plus Jakarta Sans"),
        hovertemplate="<b>%{y}</b><br>Avg CO₂: <b>%{x:.3f}</b> CO₂e/kg<extra></extra>",
    ))
    fig_bar.update_layout(**COMMON,
        hoverlabel=HOVER_STYLE,
        height=580,
        margin=dict(l=10, r=80, t=10, b=10),
        xaxis_title="CO₂e per kg food",
        yaxis_title="",
        xaxis=dict(gridcolor=GRID, tickfont=dict(color=INK, size=11)),
        yaxis=dict(tickfont=dict(color=INK, size=11)),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with r1b:
    cat_sum = df.groupby("kategori")["emisi"].sum().sort_values(ascending=False).reset_index()
    top8 = cat_sum.head(8).copy()
    other_val = cat_sum.iloc[8:]["emisi"].sum()
    if other_val > 0:
        top8 = pd.concat([top8, pd.DataFrame([{"kategori":"Others","emisi":other_val}])], ignore_index=True)

    donut_colors = [CAT_COLOR.get(c, G3) for c in top8["kategori"]]
    donut_colors = [c if c != G3 else "#aaa" for c in donut_colors]  # Others → grey

    fig_donut = go.Figure(go.Pie(
        labels=top8["kategori"], values=top8["emisi"],
        hole=0.52,
        marker_colors=donut_colors,
        textinfo="percent",
        textfont=dict(color="white", size=11, family="Plus Jakarta Sans"),
        hovertemplate="<b>%{label}</b><br>Total: %{value:.1f}<br>%{percent}<extra></extra>",
    ))
    fig_donut.update_layout(
        paper_bgcolor="white", height=290,
        hoverlabel=HOVER_STYLE,
        margin=dict(l=5, r=5, t=35, b=5),
        legend=dict(font=dict(size=10, family="Plus Jakarta Sans", color=INK)),
        title=dict(text="Share of Total Emissions",
                   font=dict(size=13, family="Space Grotesk", color=INK), x=0.5),
        annotations=[dict(text=f"<b>{len(df)}</b><br>items", x=0.5, y=0.5,
                          showarrow=False,
                          font=dict(size=13, family="Space Grotesk", color=INK))],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown(f"""
    <div class="insight red">
      <div class="insight-title" style="color:{CORAL}">🥩 Meat & Poultry Dominates</div>
      <div class="insight-body">
      Meat and poultry have the highest carbon footprint, averaging 
      <b>24.2 CO₂e/kg</b> nearly <b>30× higher</b> than fruits. 
      Beef records the highest emission in the dataset at 
      <b>99.5 CO₂e/kg</b>.
      </div>
    </div>

    <div class="insight">
      <div class="insight-title" style="color:{G1}">🥦 Plant-Based Foods Are More Sustainable</div>
      <div class="insight-body">
      Fruits and vegetables average below 
      <b>0.8 CO₂e/kg</b>, making them significantly more sustainable. 
      Replacing one meat-based meal per week with legumes may reduce emissions by approximately 
      <b>100 CO₂e per month</b>.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Row 2: Top & Bottom N ─────────────────────────────────────────────────────
st.markdown(
    f'<div class="sec">🏆 Top & Bottom {top_n} Emitters — {sel_cat}</div>',
    unsafe_allow_html=True
)

r2a, r2b = st.columns(2)

top_items    = filtered.nlargest(top_n, "emisi").reset_index(drop=True)
bottom_items = filtered.nsmallest(top_n, "emisi").reset_index(drop=True)

# ── Gradient Colors ───────────────────────────────────────────────────────────

# High emitters → dark red to soft orange
TOP_GRADIENT = [
    "#B71C1C",  # dark red
    "#D84343",  # red
    "#EF7777",  # soft coral
    "#F4A261",  # orange
    "#FFD166",  # warm yellow
]

# Low emitters → soft green to dark green
BOTTOM_GRADIENT = [
    "#D8F3DC",  # very light green
    "#B7E4C7",  # pastel green
    "#95D5B2",  # mint green
    "#52B788",  # medium green
    "#2D6A4F",  # dark green
]

# Automatically adjust if top_n changes
top_colors = TOP_GRADIENT[:len(top_items)]
bot_colors = BOTTOM_GRADIENT[:len(bottom_items)]

# ── Highest Emitters ──────────────────────────────────────────────────────────
with r2a:

    st.markdown(f"**🔴 Highest {top_n} CO₂ Emitters**")

    fig_top = go.Figure(go.Bar(

        x=top_items["emisi"],
        y=top_items["nama"],

        orientation="h",

        marker_color=top_colors,

        text=[f"{v:.2f}" for v in top_items["emisi"]],
        textposition="outside",

        textfont=dict(
            color=INK,
            size=11,
            family="Plus Jakarta Sans"
        ),

        hovertemplate=
        "<b>%{y}</b><br>"
        "CO₂: <b>%{x:.3f}</b> kg CO₂e/kg"
        "<extra></extra>",
    ))

    fig_top.update_layout(

        **COMMON,

        hoverlabel=HOVER_STYLE,

        height=max(320, top_n * 52),

        margin=dict(
            l=10,
            r=80,
            t=10,
            b=10
        ),

        xaxis_title="kg CO₂e/kg",

        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                color=INK,
                size=11
            )
        ),

        xaxis=dict(
            gridcolor=GRID,
            tickfont=dict(
                color=INK,
                size=11
            )
        ),
    )

    st.plotly_chart(
        fig_top,
        use_container_width=True
    )


# ── Lowest Emitters ───────────────────────────────────────────────────────────
with r2b:

    st.markdown(f"**🟢 Lowest {top_n} CO₂ Emitters**")

    fig_bot = go.Figure(go.Bar(

        x=bottom_items["emisi"],
        y=bottom_items["nama"],

        orientation="h",

        marker_color=bot_colors,

        text=[f"{v:.4f}" for v in bottom_items["emisi"]],
        textposition="outside",

        textfont=dict(
            color=INK,
            size=11,
            family="Plus Jakarta Sans"
        ),

        hovertemplate=
        "<b>%{y}</b><br>"
        "CO₂: <b>%{x:.4f}</b> kg CO₂e/kg"
        "<extra></extra>",
    ))

    fig_bot.update_layout(

        **COMMON,

        hoverlabel=HOVER_STYLE,

        height=max(320, top_n * 52),

        margin=dict(
            l=10,
            r=80,
            t=10,
            b=10
        ),

        xaxis_title="kg CO₂e/kg",

        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                color=INK,
                size=11
            )
        ),

        xaxis=dict(
            gridcolor=GRID,
            tickfont=dict(
                color=INK,
                size=11
            )
        ),
    )

    st.plotly_chart(
        fig_bot,
        use_container_width=True
    )

# ── Row 3: Box Plot ───────────────────────────────────────────────────────────
st.markdown('<div class="sec">📦 Emission Spread per Category</div>', unsafe_allow_html=True)
box_cats = sorted(plot_df["kategori"].unique())
box_colors = [CAT_COLOR.get(c, G3) for c in box_cats]

fig_box = go.Figure()
for cat, col in zip(box_cats, box_colors):
    sub = plot_df[plot_df["kategori"] == cat]
    fig_box.add_trace(go.Box(
        x=sub["emisi"], name=cat,
        marker_color=col, line_color=col,
        boxpoints="outliers",
        hovertemplate="<b>%{text}</b><br>CO₂: %{x:.3f}<extra></extra>",
        text=sub["nama"].tolist(),
    ))
fig_box.update_layout(**COMMON,
    hoverlabel=HOVER_STYLE,
    height=560 if sel_cat == "All Categories" else 280,
    showlegend=False,
    margin=dict(l=10, r=20, t=10, b=10),
    xaxis=dict(gridcolor=GRID, tickfont=dict(color=INK, size=11),
               title="CO₂ Emission (CO₂e/kg)"),
    yaxis=dict(tickfont=dict(color=INK, size=11)),
)
st.plotly_chart(fig_box, use_container_width=True)

# ── Row 4: Scatter ────────────────────────────────────────────────────────────
st.markdown('<div class="sec">🔵 Individual Items vs Category Average</div>', unsafe_allow_html=True)
scatter_df = plot_df.copy()
scatter_df["cat_avg"] = scatter_df["kategori"].map(scatter_df.groupby("kategori")["emisi"].mean())
scatter_df["color"]   = scatter_df["kategori"].map(CAT_COLOR).fillna(G3)

fig_sc = go.Figure()
for cat in scatter_df["kategori"].unique():
    sub = scatter_df[scatter_df["kategori"] == cat]
    fig_sc.add_trace(go.Scatter(
        x=sub["cat_avg"], y=sub["emisi"],
        mode="markers", name=cat,
        marker=dict(
            color=CAT_COLOR.get(cat, G3),
            size=sub["emisi"].apply(lambda v: max(6, min(30, v * 1.5))),
            opacity=0.82,
            line=dict(width=0.5, color="white"),
        ),
        text=sub["nama"],
        hovertemplate="<b>%{text}</b><br>Item: <b>%{y:.2f}</b> kg CO₂e/kg<br>Cat avg: <b>%{x:.2f}</b><extra></extra>",
    ))

max_val = scatter_df["cat_avg"].max() * 1.1
fig_sc.add_trace(go.Scatter(
    x=[0, max_val], y=[0, max_val], mode="lines",
    line=dict(dash="dot", color="#bbb", width=1.5), showlegend=False,
))
fig_sc.update_layout(**COMMON,
    hoverlabel=HOVER_STYLE,
    height=440,
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(font=dict(size=10, family="Plus Jakarta Sans", color=INK),
                orientation="h", y=-0.35, x=0),
    xaxis=dict(gridcolor=GRID, tickfont=dict(color=INK, size=11),
               title="Average Category Emission"),
    yaxis=dict(gridcolor=GRID, tickfont=dict(color=INK, size=11),
               title="Food Item Emission"),
)
st.plotly_chart(fig_sc, use_container_width=True)

# ── Row 5: Data Table ─────────────────────────────────────────────────────────

st.markdown(
    '<div class="sec">📋 Full Food Emission Database</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns([3, 1])

with c1:
    search = st.text_input(
        "🔍 Search food item",
        placeholder="e.g. chicken, tofu, beef…"
    )

with c2:
    sort_order = st.selectbox(
        "Sort",
        ["Highest first", "Lowest first", "Alphabetical"]
    )

# ── Filter ─────────────────────────────────────────────

show_df = filtered.copy()

if search:
    show_df = show_df[
        show_df["nama"]
        .str.lower()
        .str.contains(search.lower(), na=False)
    ]

if sort_order == "Highest first":
    show_df = show_df.sort_values("emisi", ascending=False)

elif sort_order == "Lowest first":
    show_df = show_df.sort_values("emisi", ascending=True)

else:
    show_df = show_df.sort_values("nama")

show_df = show_df.reset_index(drop=True)
show_df.index += 1

# ── Create Color Indicator ─────────────────────────────

def emission_level(x):

    if x >= 15:
        return "🔴 Very High"

    elif x >= 8:
        return "🟠 High"

    elif x >= 3:
        return "🟡 Moderate"

    elif x >= 1:
        return "🟢 Low"

    else:
        return "🌿 Very Low"

# ── Display Data ───────────────────────────────────────

max_rows = st.slider(
    "Rows to display",
    min_value=1,
    max_value=max(1, len(show_df)),
    value=min(25, len(show_df))
)

disp = show_df[
    ["nama", "kategori", "emisi"]
].head(max_rows).copy()

disp.columns = [
    "Food Item",
    "Category",
    "CO₂e/kg"
]

disp["Impact Level"] = disp["CO₂e/kg"].apply(emission_level)

disp["CO₂e/kg"] = (
    disp["CO₂e/kg"]
    .astype(float)
    .map(lambda x: f"{x:.2f}")
)

# ── Render Table ───────────────────────────────────────
st.markdown("""
<style>

/* dataframe container */
[data-testid="stDataFrame"] {
    background-color: white !important;
}

/* header */
[data-testid="stDataFrame"] thead th {
    background-color: #f1f5f9 !important;
    color: black !important;
}

/* cells */
[data-testid="stDataFrame"] tbody td {
    background-color: white !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
st.dataframe(
    disp,
    use_container_width=True,
    height=520
)

st.caption(f"Showing {len(disp)} items")

# ── Row 6: Smart Swaps ────────────────────────────────────────────────────────
st.markdown('<div class="sec">♻️ Smarter Swaps — Reduce Your Footprint</div>', unsafe_allow_html=True)
st.caption("Simple food substitutions that can dramatically cut your meal's carbon footprint.")
scols = st.columns(2)
for i, s in enumerate(SUBSTITUTIONS):
    with scols[i % 2]:
        st.markdown(f"""
        <div class="swap-card">
          <div>
            <div class="swap-cat">{s['cat']}</div>
            <span class="swap-from">🍽 {s['from']}</span>
            <span style="color:#bbb;margin:0 .5rem">→</span>
            <span class="swap-to">✅ {s['to']}</span>
          </div>
          <span class="swap-save">−{s['saving']:.1f} kg</span>
        </div>""", unsafe_allow_html=True)

# ── Row 7: Insights ───────────────────────────────────────────────────────────
st.markdown('<div class="sec">💡 Why Emissions Vary So Much</div>', unsafe_allow_html=True)
insights_data = [
    ("🥩 Meat & Poultry", "red", CORAL,
     "Cattle and sheep produce large amounts of <b>methane</b>, a powerful greenhouse gas. Beef is one of the highest-emission foods, reaching up to <b>99.5 CO₂e per kg</b>."),

    ("🐟 Fish & Seafood", "amber", AMBER,
     "Some seafood methods like <b>bottom trawling</b> use large amounts of fuel and increase emissions. Shrimp farming can also cause <b>mangrove deforestation</b>, while sardines and shellfish usually have lower footprints."),

    ("🧀 Dairy Products", "teal", TEAL,
     "Dairy emissions mainly come from <b>methane from cows</b> and feed production. Plant-based milk such as oat or soy milk can reduce emissions by around <b>60–80%</b> compared to cow’s milk."),

    ("🥦 Fruits & Vegetables", "", G1,
     "Fruits and vegetables generally require less land, water, and energy than animal products. Most fruits produce less than <b>0.47 CO₂e per kg</b>, making them among the most sustainable food choices."),
]
ic1, ic2 = st.columns(2)
for i, (title, cls, color, body) in enumerate(insights_data):
    with (ic1 if i % 2 == 0 else ic2):
        st.markdown(f"""
        <div class="insight {cls}">
          <div class="insight-title" style="color:{color}">{title}</div>
          <div class="insight-body">{body}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<style>

/* hide menu */
#MainMenu {
    visibility: hidden;
}

/* hide footer */
footer {
    visibility: hidden;
}

/* remove top-right deploy/share widgets */
[data-testid="stDecoration"] {
    display: none !important;
}

/* safari weird text bug */
body::before,
body::after {
    display: none !important;
    content: none !important;
}

</style>
""", unsafe_allow_html=True)
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:.76rem;color:#7a9e8a;font-family:'Space Grotesk',sans-serif">
  🌱 EcoLens · Food Carbon Footprint Intelligence · 290 items · 20 categories
</div>""", unsafe_allow_html=True)
