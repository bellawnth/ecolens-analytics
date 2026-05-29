# EcoLens: Food Carbon Footprint Dashboard
AI-driven sustainable consumption dashboard for food carbon footprint analysis and environmental impact visualization

🔗 **Link Dashboard:**
[https://ecolens-analytics.streamlit.app](https://ecolens-analytics.streamlit.app)

---

# 📌 Deskripsi Proyek

Merupakan dashboard analitik interaktif berbasis data yang dikembangkan untuk menganalisis jejak karbon (*carbon footprint*) dari berbagai jenis makanan guna meningkatkan *awareness* terhadap *sustainable consumption*. Proyek ini berangkat dari permasalahan masih terbatasnya akses informasi terkait dampak lingkungan dari konsumsi sehari-hari. Dashboard ini tidak hanya menampilkan besaran emisi CO₂e tiap makanan tetapi juga mengeksplorasi distribusi emisi antar kategori pangan, pola kontribusi karbon serta rekomendasi alternatif makanan yang lebih ramah lingkungan melalui visualisasi data interaktif. Dengan pendekatan *data-drive*n dan *exploratory data analysis (EDA)* dan *explanatory data analysis*, dashboard ini dirancang untuk membantu pengguna memahami hubungan antara pola konsumsi dan dampak lingkungan secara lebih intuitif, informatif dan praktis.

---

# 📚 Library yang Digunakan

* `streamlit` → membangun dashboard interaktif
* `pandas` → manipulasi dan analisis data
* `numpy` → komputasi numerik
* `plotly` → visualisasi data interaktif

---

# ⚙️ Setup Environment

## Menggunakan Anaconda

```bash
conda create --name ecolens python=3.9
conda activate ecolens
pip install -r requirements.txt
```

## Menggunakan Terminal / Shell

```bash
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

---

# ▶️ Cara Menjalankan Dashboard

```bash
streamlit run EcoLens_Dash.py
```

Kemudian buka browser dan akses:

```bash
http://localhost:8501
```

---

# ☁️ Link Dashboard Streamlit Cloud

Streamlit:
[https://your-streamlit-dashboard-link.streamlit.app](https://ecolens-analytics.streamlit.app)
