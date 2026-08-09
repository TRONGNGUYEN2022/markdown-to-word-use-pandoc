import streamlit as st
import pypandoc
import os
import tempfile
import shutil

# Cấu hình trang
st.set_page_config(page_title="Pandoc Converter Pro", layout="centered")
st.title("📝 Markdown to Word (Pandoc)")

# 1. Định nghĩa thư mục lưu ảnh tạm trên server
UPLOAD_DIR = "server_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 2. Upload file Markdown
uploaded_md = st.file_uploader("Chọn file Markdown (.md)", type=["md"])

# 3. Upload ảnh (Tự động lưu vào server khi chọn)
uploaded_images = st.file_uploader(
    "Chọn các file ảnh (Được lưu vào server ngay khi chọn)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

# Lưu ảnh vào server ngay lập tức khi người dùng upload
if uploaded_images:
    for img in uploaded_images:
        file_path = os.path.join(UPLOAD_DIR, img.name)
        with open(file_path, "wb") as f:
            f.write(img.getbuffer())
    st.sidebar.success(f"Đã lưu {len(uploaded_images)} ảnh vào server!")

# 4. Nút xử lý
if st.button("Chuyển đổi sang Word"):
    if uploaded_md:
        with st.spinner("Đang xử lý bằng Pandoc..."):
            # Tạo thư mục tạm để Pandoc làm việc
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Sao chép file MD vào thư mục tạm
                md_path = os.path.join(tmp_dir, uploaded_md.name)
                with open(md_path, "wb") as f:
                    f.write(uploaded_md.getvalue())
                
                # Sao chép tất cả ảnh từ thư mục server vào thư mục tạm của Pandoc
                for img_name in os.listdir(UPLOAD_DIR):
                    shutil.copy(os.path.join(UPLOAD_DIR, img_name), tmp_dir)
                
                # Chuyển hướng tới thư mục tạm để Pandoc tìm thấy ảnh dễ dàng
                old_cwd = os.getcwd()
                os.chdir(tmp_dir)
                
                output_docx = "output.docx"
                
                try:
                    # Gọi Pandoc
                    pypandoc.convert_file(uploaded_md.name, 'docx', outputfile=output_docx, extra_args=['--mathjax'])
                    
                    # Trả lại thư mục cũ
                    os.chdir(old_cwd)
                    
                    with open(output_docx, "rb") as f:
                        st.download_button("📥 Tải xuống file Word", data=f, file_name="Ket_Qua.docx")
                    st.success("Xử lý thành công!")
                except Exception as e:
                    os.chdir(old_cwd)
                    st.error(f"Lỗi Pandoc: {e}")
    else:
        st.warning("Vui lòng tải lên file Markdown.")

# Dọn dẹp: (Tùy chọn) Xóa ảnh trong thư mục server sau mỗi lần chạy
if st.button("Xóa sạch ảnh trên server"):
    shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)
    st.experimental_rerun()