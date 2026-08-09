import streamlit as st
import pypandoc
import os
import tempfile
import shutil

st.title("Pandoc Converter (Online Ready)")

uploaded_md = st.file_uploader("Upload file .md", type=["md"])
uploaded_images = st.file_uploader("Upload ảnh (chọn tất cả ảnh cùng lúc)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("Chuyển đổi sang Word"):
    if uploaded_md and uploaded_images:
        with st.spinner("Đang xử lý..."):
            # 1. Tạo thư mục tạm
            with tempfile.TemporaryDirectory() as tmp_dir:
                # 2. Copy file MD vào tmp_dir
                md_path = os.path.join(tmp_dir, uploaded_md.name)
                with open(md_path, "wb") as f:
                    f.write(uploaded_md.getvalue())
                
                # 3. Copy tất cả ảnh vào tmp_dir
                for img in uploaded_images:
                    img_path = os.path.join(tmp_dir, img.name)
                    with open(img_path, "wb") as f:
                        f.write(img.getbuffer())
                
                # 4. GHI NHỚ: Đổi thư mục làm việc của Python vào tmp_dir
                # Đây là bước quan trọng nhất để Pandoc thấy ảnh nằm cùng chỗ với file md
                original_dir = os.getcwd()
                os.chdir(tmp_dir)
                
                output_docx = "output.docx"
                
                try:
                    # 5. Gọi Pandoc (lúc này nó đang đứng trong tmp_dir)
                    pypandoc.convert_file(uploaded_md.name, 'docx', outputfile=output_docx)
                    
                    if os.path.exists(output_docx):
                        with open(output_docx, "rb") as f:
                            st.download_button("📥 Tải kết quả", data=f, file_name="Ket_Qua.docx")
                        st.success("Chuyển đổi thành công!")
                    else:
                        st.error("Không tạo được file Word.")
                except Exception as e:
                    st.error(f"Lỗi Pandoc: {e}")
                finally:
                    # Quay về thư mục cũ
                    os.chdir(original_dir)
    else:
        st.warning("Vui lòng tải lên file .md và các file ảnh liên quan.")