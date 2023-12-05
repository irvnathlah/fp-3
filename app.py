import streamlit as st
from sqlalchemy import text

list_teknisi = ['', 'Jaenuri', 'Subaeri', 'Markipat', 'Johnson', 'Awaluddin']
list_kendala = ['', 'Laki-laki', 'Perempuan']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://irvnathlah:KHZeoGLtD51X@ep-broad-breeze-56976802.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS bengkeloke (id serial, nama_teknisi varchar, nama_pelanggan varchar, jenis_kelamin char(25), \
                                                       kendala text, nomor_telepon varchar, alamat text, tanggal_servis date);')
    session.execute(query)

st.header('pDATA BASE BENGKEL OKE')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM bengkeloke ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO bengkeloke (nama_teknisi, nama_pelanggan, jenis_kelamin, kendala, nomor_telepon, alamat, waktu, tanggal_servis) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM bengkeloke ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_teknisi_lama = result["nama_teknisi"]
        nama_pelanggan_lama = result["nama_pelanggan"]
        jenis_kelamin_lama = result["jenis_kelamin"]
        kendala_lama = result["kendala"]
        nomor_telepon_lama = result["nomor_telepon"]
        alamat_lama = result["alamat"]
        waktu_lama = result["waktu"]
        tanggal_servis_lama = result["tanggal_servis"]

        with st.expander(f'a.n. {nama_pelanggan_lama}'):
            with st.form(f'data-{id}'):
                nama_teknisi_baru = st.selectbox("nama_teknisi", list_teknisi, list_teknisi.index(nama_teknisi_lama))
                nama_pelanggan_baru = st.text_input("nama_pelanggan", nama_pelanggan_lama)
                jenis_kelamin_baru = st.selectbox("jenis_kelamin", list_kendala, list_kendala.index(jenis_kelamin_lama))
                kendala_baru = st.multiselect("kendala", ['Ganti oli', 'Tune up', 'Servis rutin', 'Sepul mati', 'Ganti rantai', 'Full servis berat'], eval(kendala_lama))
                nomor_telepon_baru = st.text_input("nomor_telepon", nomor_telepon_lama)
                alamat_baru = st.text_input("alamat", alamat_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_servis_baru = st.date_input("tanggal_servis", tanggal_servis_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE bengkeloke \
                                          SET nama_teknisi=:1, nama_pelanggan=:2, jenis_kelamin=:3, kendala=:4, \
                                          nomor_telepon=:5, alamat=:6, waktu=:7, tanggal_servis=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':nama_teknisi_baru, '2':nama_pelanggan_baru, '3':jenis_kelamin_baru, '4':str(kendala_baru), 
                                                    '5':nomor_telepon_baru, '6':alamat_baru, '7':waktu_baru, '8':tanggal_servis_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM bengkeloke WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()