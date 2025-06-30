import streamlit as st
import subprocess
import os
import shutil

st.title("🎯 Invoice2Data - Extract PDF to CSV")

uploaded_file = st.file_uploader("📄 Upload file hóa đơn (.pdf)", type=["pdf"])

if uploaded_file:
    # Save file tạm
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Tạo folder output
    output_csv = "src/myinvoices/invoicesaaaa.csv"
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Gọi invoice2data
    with st.spinner("🔄 Đang xử lý bằng invoice2data..."):
        try:
            result = subprocess.run([
                "invoice2data",
                "--output-format", "csv",
                "--output-name", output_csv,
                file_path
            ], capture_output=True, text=True, check=True)

            st.success("✅ Xử lý thành công!")
            with open(output_csv, "rb") as f:
                st.download_button("📥 Tải file CSV", f, file_name="invoices.csv")
        except subprocess.CalledProcessError as e:
            st.error("❌ Lỗi khi xử lý hóa đơn:")
            st.text(e.stderr)
