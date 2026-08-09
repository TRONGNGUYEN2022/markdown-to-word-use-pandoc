import streamlit as st
import pypandoc
import os
import tempfile

st.title("Markdown sang Word (Chỉ dùng Pandoc)")

uploaded_md = st.file_uploader("Upload file .md", type=["md"])
uploaded_images = st.file_uploader("Upload ảnh (nếu có)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("Chuyển đổi"):
    if uploaded_md:
        with tempfile.TemporaryDirectory() as tmp_dir:
            # 1. Lưu file MD vào thư mục tạm
            md_path = os.path.join(tmp_dir, uploaded_md.name)
            with open(md_path, "wb") as f:
                f.write(uploaded_md.getvalue())
            
            # 2. Lưu các ảnh vào cùng thư mục đó
            for img in uploaded_images:
                with open(os.path.join(tmp_dir, img.name), "wb") as f:
                    f.write(img.getbuffer())
            
            # 3. Chuyển đổi bằng Pandoc
            # Pandoc sẽ tự quét file MD, nếu thấy ![alt](ảnh) 
            # nó sẽ tự lấy file ảnh trong cùng thư mục chèn vào Word
            output_docx = os.path.join(tmp_dir, "output.docx")
            
            try:
                # --mathjax giúp Pandoc hiểu công thức LaTeX và chuyển thành OMML (Equation chuẩn)
                pypandoc.convert_file(md_path, 'docx', outputfile=output_docx, extra_args=['--mathjax'])
                
                with open(output_docx, "rb") as f:
                    st.download_button("📥 Tải file Word", data=f, file_name="ket_qua.docx")
            except Exception as e:
                st.error(f"Lỗi Pandoc: {e}")