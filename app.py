import streamlit as st
import plotly.express as px

# Fungsi estimasi waktu pengiriman
def hitung_estimasi_pengiriman(jarak_km):
    if jarak_km <= 50:
        return "1 Hari"
    elif jarak_km <= 200:
        return "2-3 Hari"
    else:
        return "4+ Hari"

# Fungsi deskripsi status
def status_pengiriman(kode):
    status_dict = {
        0: "Dalam Proses",
        1: "Dikirim",
        2: "Dalam Perjalanan",
        3: "Tiba di Kota Tujuan",
        4: "Diterima oleh Pelanggan"
    }
    return status_dict.get(kode, "Status Tidak Diketahui")

# Streamlit UI
st.title("📦 Aplikasi Pelacakan Pengiriman Paket")

# Input data paket dari user
with st.form("form_paket"):
    id_paket = st.text_input("ID Paket")
    jarak = st.number_input("Jarak Pengiriman (km)", min_value=0.0)
    status_kode = st.selectbox("Status Paket", options=[0, 1, 2, 3, 4], format_func=status_pengiriman)
    submit = st.form_submit_button("Tambah Paket")

# Menyimpan paket di session_state
if "paket_list" not in st.session_state:
    st.session_state.paket_list = []

if submit:
    st.session_state.paket_list.append({
        "id": id_paket,
        "jarak": jarak,
        "status": status_kode
    })
    st.success(f"Paket {id_paket} berhasil ditambahkan!")

# Menampilkan laporan data paket
if st.session_state.paket_list:
    st.subheader("📊 Laporan Pengiriman")

    for paket in st.session_state.paket_list:
        st.markdown(f"""
        **ID Paket**: {paket['id']}  
        **Status**: {status_pengiriman(paket['status'])}  
        **Estimasi Waktu**: {hitung_estimasi_pengiriman(paket['jarak'])}  
        ---""")

    # --- GRAFIK JUMLAH PAKET PER STATUS ---
    st.subheader("📈 Grafik Jumlah Paket per Status")

    # Hitung jumlah per status
    from collections import Counter
    counter = Counter([status_pengiriman(p['status']) for p in st.session_state.paket_list])
    df_grafik = {
        "Status": list(counter.keys()),
        "Jumlah Paket": list(counter.values())
    }

    fig = px.bar(df_grafik, x="Status", y="Jumlah Paket", color="Status",
                 title="Distribusi Status Paket", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Belum ada data paket yang dimasukkan.")
