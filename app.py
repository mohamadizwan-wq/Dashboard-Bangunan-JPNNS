"""Public Streamlit host for the JPNS interactive building dashboard."""
import base64
import json
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from build_dashboard import extract

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Dashboard Aset Bangunan JPNS", page_icon=str(ROOT / "logo.jpg"), layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
/* The dashboard owns scrolling; its frame fills the browser viewport. */
[data-testid="stAppViewContainer"], .stApp {background:#f3f6f2;}
[data-testid="stHeader"] {display:none;}
.block-container {padding:0!important;max-width:none!important;}
iframe[title="st.iframe"] {
    position:fixed;inset:0;width:100%!important;height:100dvh!important;
    border:0;display:block;
}
</style>""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_dashboard(source_bytes, template, logo_bytes):
    from io import BytesIO
    records, incomplete = extract(BytesIO(source_bytes))
    payload = dict(records=records, incomplete=incomplete, modified="", logo="data:image/jpeg;base64," + base64.b64encode(logo_bytes).decode())
    # A deployed file's modification time is not the date of its data collection.
    template = template.replace("$('updated').textContent='Tarikh fail: '+DATA.modified;", "$('updated').textContent='Versi Data: ' + DATA.version;")
    template = template.replace("<br>Waktu Malaysia", "")
    template = template.replace("Sumber: data.xlsx", "Sumber: Seksyen Kejuruteraan")
    template = template.replace("['Tidak digunakan',unused", "['Tidak Digunakan',unused")
    template = template.replace('<span id="updated"></span>', '<span id="updated"></span><br>Developer: Seksyen Kejuruteraan')
    for title in ("Portfolio aset bangunan", "Taburan mengikut kategori", "Keadaan & penggunaan", "Daerah pentadbiran", "Daftar aset bangunan", "Ringkasan portfolio", "Semakan data sumber", "Jumlah aset", "Keadaan baik", "Rosak / selenggara", "Carian aset", "Daerah sivil", "Kategori aset", "Keadaan aset"):
        template = template.replace(title, title.title())
    template = template.replace("Keadaan & Penggunaan", "Keadaan")
    template = template.replace("Keadaan Baik tidak semestinya sedang digunakan.", "Ringkasan keadaan aset berdasarkan rekod semasa.")
    template = re.sub(r",\['Rujukan Excel',`[^`]*`\]", "", template)
    template = template.replace("max-width:1800px", "max-width:none")
    template = template.replace("Paparan berdasarkan salinan data semasa dashboard dijana. Jalankan Kemas_Kini_Dashboard.ps1 selepas mengubah Excel.", "Data terbuka untuk paparan awam. Maklumat berdasarkan fail Excel yang terakhir diterbitkan oleh pentadbir.")
    payload['version'] = '1.0'
    return template.replace('__PAYLOAD__', json.dumps(payload, ensure_ascii=True).replace('</', '<\\/'))

try:
    html = load_dashboard((ROOT/'data.xlsx').read_bytes(), (ROOT/'dashboard_template.html').read_text(encoding='utf-8'), (ROOT/'logo.jpg').read_bytes())
except (OSError, ValueError, KeyError) as exc:
    st.error('Fail sumber tidak dapat dibaca. Pentadbir perlu menyemak data.xlsx dan fail aplikasi dalam repository.')
    st.stop()

components.html(html, height=1900, scrolling=True)
