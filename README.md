# Dashboard Aset Bangunan JPNS

Dashboard interaktif data terbuka dengan carian, penapis, carta, butiran aset dan eksport CSV.

## Terbitkan di Streamlit Community Cloud

1. Cipta repository GitHub berstatus Public, contohnya `dashboard-bangunan-jpns`.
2. Muat naik SEMUA enam fail dalam folder ini ke peringkat utama repository:
   `app.py`, `build_dashboard.py`, `dashboard_template.html`, `data.xlsx`, `logo.jpg` dan `requirements.txt`.
   README.md ini juga boleh dimuat naik.
3. Log masuk https://share.streamlit.io menggunakan akaun yang disambungkan kepada GitHub.
4. Pilih Create app, kemudian pilihan deploy daripada GitHub.
5. Pilih repository, branch `main` dan main file path `app.py`.
6. Klik Deploy. Pastikan akses aplikasi ditetapkan kepada public.

## Kemas kini

Gantikan `data.xlsx` dalam repository GitHub dan commit perubahan. Streamlit akan menggunakan versi yang diterbitkan semula. Mengedit Excel dalam PC sahaja tidak mengemas kini laman.

Pautan Google Drive memerlukan kebenaran perkongsian gambar asal yang membenarkan pelawat melihatnya.
Rekod tanpa nama tidak dihitung. Koordinat berulang pada lokasi berlainan ditandakan untuk semakan.

## Jalankan secara tempatan

`pip install -r requirements.txt`

`streamlit run app.py`

Paparan dashboard dibenamkan dalam Streamlit untuk mengekalkan reka bentuk HTML asal.
