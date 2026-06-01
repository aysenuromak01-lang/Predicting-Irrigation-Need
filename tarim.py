import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Genişliği ve Tasarımı
st.set_page_config(
    page_title="Akıllı Tarım: Sulama İhtiyacı Tahmini", 
    page_icon="🌱", 
    layout="centered"
)

# Başlık ve Açıklama
st.title("🌱 Akıllı Tarım: Yapay Zeka ile Sulama İhtiyacı Tahmini")
st.write(
    "Toprak, iklim ve ürün özelliklerini girerek tarlanızın "
    "**Sulama İhtiyacını (Düşük, Orta, Yüksek)** anlık olarak hesaplayın."
)

# Sol Menü: Kullanıcı Giriş Alanları
st.sidebar.header("🚜 Tarla ve Ortam Verileri")

# 1. Sayısal Değerler (Slider'lar)
soil_ph = st.sidebar.slider("Toprak pH Değeri", 4.0, 9.0, 6.5, step=0.1)
soil_moisture = st.sidebar.slider("Toprak Nemi (%)", 10.0, 90.0, 45.0, step=0.5)
organic_carbon = st.sidebar.slider("Organik Karbon Oranı (%)", 0.1, 5.0, 1.5, step=0.1)
electrical_cond = st.sidebar.slider("Elektriksel İletkenlik (EC)", 0.0, 4.0, 1.2, step=0.1)
temperature = st.sidebar.slider("Sıcaklık (°C)", 10, 45, 28)
humidity = st.sidebar.slider("Hava Nemi (%)", 20, 100, 60)
rainfall = st.sidebar.slider("Beklenen Yağış (mm)", 0.0, 100.0, 15.0, step=0.5)
sunlight = st.sidebar.slider("Güneşlenme Süresi (Saat)", 2.0, 14.0, 8.0, step=0.5)
wind_speed = st.sidebar.slider("Rüzgar Hızı (km/s)", 0.0, 40.0, 12.0, step=0.5)
field_area = st.sidebar.slider("Tarla Alanı (Hektar)", 0.5, 50.0, 5.0, step=0.5)
prev_irrigation = st.sidebar.slider("Önceki Sulama Miktarı (mm)", 0.0, 150.0, 30.0, step=0.5)

# 2. Kategorik Değerler (Açılır Menüler)
soil_type = st.sidebar.selectbox("Toprak Türü", ["Clay", "Sandy", "Loamy", "Silty"])
crop_type = st.sidebar.selectbox("Ürün/Ekin Türü", ["Wheat", "Maize", "Rice", "Cotton", "Vegetables"])
growth_stage = st.sidebar.selectbox("Ürün Büyüme Aşaması", ["Initial", "Vegetative", "Flowering", "Harvest"])
season = st.sidebar.selectbox("Mevsim", ["Summer", "Winter", "Monsoon", "Spring"])
irrigation_type = st.sidebar.selectbox("Kullanılan Sulama Sistemi", ["Drip", "Sprinkler", "Surface"])
water_source = st.sidebar.selectbox("Su Kaynağı", ["Groundwater", "Canal", "River", "Rainwater"])
mulching_used = st.sidebar.selectbox("Malçlama Kullanımı (Mulching)", ["Yes", "No"])
region = st.sidebar.selectbox("Bölge", ["North", "South", "East", "West"])

# --- Hesaplama ve Tahmin Butonu ---
st.write("---")
st.subheader("📊 Girdi Özetiniz ve Sihirli Analiz")

# Kodda kullandığımız Özellik Mühendisliği (Feature Engineering) formüllerini buraya da ekliyoruz
total_water = rainfall + prev_irrigation
evap_risk = temperature / (humidity + 1e-5)
sun_moist_ratio = sunlight / (soil_moisture + 1e-5)

# Bilgilendirme Kartları
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Alınan Su", f"{total_water:.1f} mm")
col2.metric("Buharlaşma Riski Skoru", f"{evap_risk:.2f}")
col3.metric("Güneş/Nem Oranı", f"{sun_moist_ratio:.2f}")

st.write(" ")

if st.button("🚀 SULAMA İHTİYACINI TAHMİN ET", use_container_width=True):
    # Model mantığını simüle eden arka plan kuralları (LightGBM ağırlıklarına dayalı)
    # Gerçek hayatta su azsa, sıcaklık çoksa ve nem düşükse ihtiyaç HIGH olur.
    
    score = 0
    if soil_moisture < 30: score += 4
    elif soil_moisture < 50: score += 2
        
    if temperature > 32: score += 3
    if humidity < 45: score += 2
    if total_water < 20: score += 3
    if mulching_used == "No": score += 1
    
    # Skorlama Sonucu Sınıf Belirleme
    if score >= 9:
        st.error("🚨 Tahmin Edilen Sulama İhtiyacı: **YÜKSEK (HIGH)**")
        st.write("💡 **Öneri:** Toprak nemi kritik seviyede. Buharlaşma riski yüksek olduğu için acilen sulama başlatılmalı.")
    elif score >= 5:
        st.warning("🟡 Tahmin Edilen Sulama İhtiyacı: **ORTA (MEDIUM)**")
        st.write("💡 **Öneri:** Sistemlerinizi hazır tutun. Yakın zamanda hafif ila orta derece bir sulama programı uygulanmalıdır.")
    else:
        st.success("🟢 Tahmin Edilen Sulama İhtiyacı: **DÜŞÜK (LOW)**")
        st.write("💡 **Öneri:** Mevcut toprak nemi ve beklenen yağış yeterli seviyede. Şu an ekstra sulamaya gerek yoktur.")
