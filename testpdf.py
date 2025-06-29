import subprocess
import os

def pdftotext_extract(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_path}")

    # Tạo file tạm để lưu text
    txt_path = pdf_path.replace(".pdf", ".txt")

    # Gọi lệnh pdftotext thông qua subprocess
    try:
        subprocess.run(["pdftotext", "-layout", pdf_path, txt_path], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Lỗi khi gọi pdftotext:", e)
        return ""

    # Đọc kết quả text
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    else:
        return ""

# ==== CHẠY THỬ ====
if __name__ == "__main__":
    pdf_file = "VIETTEL.pdf"  # Đường dẫn đến file PDF
    text = pdftotext_extract(pdf_file)
    print("📄 TEXT EXTRACTED:")
    print("=" * 50)
    print(text)
    print("=" * 50)
