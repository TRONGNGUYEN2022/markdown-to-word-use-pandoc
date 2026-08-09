import streamlit as st
import pypandoc
import os
import tempfile
import shutil

# Cấu hình trang
st.set_page_config(page_title="Pandoc Converter Pro", layout="centered")
st.title("📝 Markdown to Word (Fix Lỗi Ảnh)")

# 1. Thư mục lưu tạm trên server
UPLOAD_DIR = "server_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_md = st.file_uploader("Chọn file Markdown (.md)", type=["md"])
uploaded_images = st.file_uploader("Chọn file ảnh", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Tự động lưu ảnh vào server
if uploaded_images:
    for img in uploaded_images:
        with open(os.path.join(UPLOAD_DIR, img.name), "wb") as f:
            f.write(img.getbuffer())

if st.button("Chuyển đổi sang Word"):
    if uploaded_md:
        with st.spinner("Đang chuyển đổi..."):
            with tempfile.TemporaryDirectory() as tmp_dir:
                # 1. Copy MD và Ảnh vào thư mục làm việc của Pandoc
                md_path = os.path.join(tmp_dir, uploaded_md.name)
                with open(md_path, "wb") as f:
                    f.write(uploaded_md.getvalue())
                
                for img_name in os.listdir(UPLOAD_DIR):
                    shutil.copy(os.path.join(UPLOAD_DIR, img_name), os.path.join(tmp_dir, img_name))
                
                # DEBUG: Kiểm tra xem ảnh đã vào chưa
                st.write("---")
                st.write("Files có trong thư mục xử lý (tmp_dir):", os.listdir(tmp_dir))
                
                output_docx = os.path.join(tmp_dir, "output.docx")
                
                try:
                    # Chạy Pandoc với tham số ép buộc nhúng media
                    # --extract-media=. giúp Pandoc ưu tiên tìm file trong thư mục hiện tại
                    pypandoc.convert_file(
                        md_path, 
                        'docx', 
                        outputfile=output_docx, 
                        extra_args=['--extract-media=.'] 
                    )
                    
                    if os.path.exists(output_docx):
                        with open(output_docx, "rb") as f:
                            st.download_button("📥 Tải kết quả", data=f, file_name="Ket_Qua.docx")
                        st.success("Xử lý thành công!")
                    else:
                        st.error("Pandoc không tạo được file Word.")
                        
                except Exception as e:
                    st.error(f"Lỗi hệ thống Pandoc: {str(e)}")
    else:
        st.warning("Vui lòng tải file .md")

# Nút dọn dẹp
if st.button("Dọn dẹp ảnh trên server"):
    shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)
    st.rerun()