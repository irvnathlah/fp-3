import streamlit as st
from sqlalchemy import text

list_doctor = ['', 'dr. Nurita', 'dr. Yogi', 'dr. Wibowo', 'dr. Ulama', 'dr. Ping']
list_symptom = ['', 'male', 'female']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://irvnathlah:KHZeoGLtD51X@ep-broad-breeze-56976802.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS bengkeloke (id serial, nama_teknisi varchar, nama_pelanggan varchar, jenis_kelamin char(25), \
                                                       symptom text, handphone varchar, address text, tanggal date);')
    session.execute(query)

st.header('SIMPLE HOSPITAL DATA MANAGEMENT SYS')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM bengkeloke ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO bengkeloke (nama_teknisi, nama_pelanggan, jenis_kelamin, symptom, handphone, address, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM bengkeloke ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_teknisi_lama = result["nama_teknisi"]
        nama_pelanggan_lama = result["nama_pelanggan"]
        jenis_kelamin_lama = result["jenis_kelamin"]
        symptom_lama = result["symptom"]
        handphone_lama = result["handphone"]
        address_lama = result["address"]
        waktu_lama = result["waktu"]
        tanggal_lama = result["tanggal"]

        with st.expander(f'a.n. {nama_pelanggan_lama}'):
            with st.form(f'data-{id}'):
                nama_teknisi_baru = st.selectbox("nama_teknisi", list_doctor, list_doctor.index(nama_teknisi_lama))
                nama_pelanggan_baru = st.text_input("nama_pelanggan", nama_pelanggan_lama)
                jenis_kelamin_baru = st.selectbox("jenis_kelamin", list_symptom, list_symptom.index(jenis_kelamin_lama))
                symptom_baru = st.multiselect("symptom", ['cough', 'flu', 'headache', 'stomache'], eval(symptom_lama))
                handphone_baru = st.text_input("handphone", handphone_lama)
                address_baru = st.text_input("address", address_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE bengkeloke \
                                          SET nama_teknisi=:1, nama_pelanggan=:2, jenis_kelamin=:3, symptom=:4, \
                                          handphone=:5, address=:6, waktu=:7, tanggal=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':nama_teknisi_baru, '2':nama_pelanggan_baru, '3':jenis_kelamin_baru, '4':str(symptom_baru), 
                                                    '5':handphone_baru, '6':address_baru, '7':waktu_baru, '8':tanggal_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM bengkeloke WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()