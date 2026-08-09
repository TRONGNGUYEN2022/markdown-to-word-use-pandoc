import streamlit as st
import pypandoc
import os
import tempfile
import shutil

st.title("Pandoc Converter Debugger")

# Tạo thư mục ảnh
UPLOAD_DIR = "server_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_md = st.file_uploader("Upload .md", type=["md"])
uploaded_images = st.file_uploader("Upload ảnh", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("Chuyển đổi"):
    if uploaded_md:
        with tempfile.TemporaryDirectory() as tmp_dir:
            md_path = os.path.join(tmp_dir, uploaded_md.name)
            with open(md_path, "wb") as f:
                f.write(uploaded_md.getvalue())
            
            # Copy ảnh
            for img in uploaded_images:
                with open(os.path.join(tmp_dir, img.name), "wb") as f:
                    f.write(img.getbuffer())
            
            output_docx = os.path.join(tmp_dir, "output.docx")
            
            try:
                # Dùng đường dẫn tuyệt đối để tránh lỗi thư mục
                pypandoc.convert_file(md_path, 'docx', outputfile=output_docx)
                
                with open(output_docx, "rb") as f:
                    st.download_button("📥 Tải kết quả", data=f, file_name="Ket_Qua.docx")
            except RuntimeError as e:
                # Nếu Pandoc lỗi, nó sẽ in ra thông báo chi tiết tại đây
                st.error(f"Pandoc Runtime Error: {e}")
                # Kiểm tra xem Pandoc đã được cài chưa
                try:
                    import subprocess
                    version = subprocess.check_output(['pandoc', '--version'])
                    st.write("Pandoc đã cài đặt:", version.decode().split('\n')[0])
                except:
                    st.error("Pandoc CHƯA ĐƯỢC CÀI ĐẶT trên server này!")
    else:
        st.warning("Vui lòng upload file .md")