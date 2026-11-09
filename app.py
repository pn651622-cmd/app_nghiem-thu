import streamlit as st  # type: ignore[import-not-found]
import requests
import base64

# Cấu hình giao diện app trên điện thoại
st.set_page_config(page_title="App Chụp Ảnh Nghiệm Thu", page_icon="📸", layout="centered")

st.markdown("### 📱 Chụp Ảnh Nghiệm Thu")
st.write("Chụp ảnh trực tiếp từ camera điện thoại và lưu lên Google Drive.")

# Form nhập thông tin và chụp ảnh
with st.form("nghiem_thu_form"):
    ma_ct = st.text_input("Mã Công Trình / Hạng Mục", placeholder="VD: PhongKhach-01")
    noi_dung = st.text_area("Nội dung nghiệm thu", placeholder="Kiểm tra âm tường...")
    
    # Nút mở camera chụp ảnh trực tiếp trên điện thoại
    img_file = st.camera_input("Chụp 1 tấm ảnh hiện trường")
    
    submit_button = st.form_submit_button(label="🚀 Gửi lên Google Drive")

if submit_button:
    if img_file is not None and ma_ct:
        with st.spinner("Đang tải ảnh lên Google Drive, vui lòng đợi..."):
            try:
                # Đọc dữ liệu file ảnh và mã hóa Base64
                bytes_data = img_file.getvalue()
                encoded_string = base64.b64encode(bytes_data).decode('utf-8')
                
                payload = {
                    "image": encoded_string,
                    "mimeType": img_file.type,
                    "filename": f"{ma_ct}_{img_file.name}",
                    "maCT": ma_ct,
                    "noiDung": noi_dung
                }
                
                # Dán URL Web App bạn copy ở Bước 1 vào trong dấu ngoặc kép dưới đây:
                gas_url = "https://script.google.com/macros/s/AKfycbyRwMZBpnRmUc7DlwHp5TLSeuoPP7ZpPGvau2Yb_oIZkM-78461KREwoLzPTiX5ihEbSQ/exec"
                
                response = requests.post(gas_url, json=payload)
                result = response.json()
                
                if result.get("status") == "success":
                    st.success("🎉 Tải ảnh lên Google Drive thành công!")
                    st.balloons()
                else:
                    st.error(f"Lỗi từ Google: {result.get('message')}")
                    
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
    else:
        st.warning("⚠️ Vui lòng nhập Mã công trình và chụp 1 tấm ảnh trước khi gửi!")
