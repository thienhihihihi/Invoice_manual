import os
import csv
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates

# --- Cấu hình ---
input_folder = 'C:/Users/thien/OneDrive/Desktop/invoice2data-master/invoice2data-master/hihi'
output_csv = './all_invoices.csv'
template_folder = 'C:/Users/thien/OneDrive/Desktop/invoice2data-master/invoice2data-master/src/invoice2data/extract/templates'

# Các trường chung và sản phẩm
fieldnames = [
    'invoice_number', 'date', 'seller', 'seller_tax_code', 'seller_address',
    'seller_phone', 'seller_bank_account', 'buyer_name', 'buyer', 'buyer_tax_id',
    'buyer_address', 'payment_method', 'buyer_bank_account', 'vat_rate',
    'amount_untaxed', 'amount_tax', 'amount_total', 'amount', 'source_file',
     'description', 'unit', 'qty', 'unit_price', 'line_total'
]

# --- Load templates ---
templates = read_templates(template_folder)

# --- Duyệt qua folder hóa đơn ---
all_data = []

for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(input_folder, filename)
        print(f"📄 Đang xử lý: {filename}")
        result = extract_data(file_path, templates=templates)

        if result:
            result['source_file'] = filename
            lines = result.get("lines", [])

            # Nếu có line sản phẩm, tách từng dòng sản phẩm ra
            if isinstance(lines, list) and len(lines) > 0:
                for line in lines:
                    row = {k: result.get(k, '') for k in fieldnames if k not in ['description', 'unit', 'qty', 'unit_price', 'line_total']}
                    row.update({
                        
                        'description': line.get('description', line.get('name', '')),  # name hoặc description tùy template
                        'unit': line.get('unit', ''),
                        'qty': line.get('qty', ''),
                        'unit_price': line.get('unit_price', ''),
                        'line_total': line.get('line_total', line.get('amount_after_vat', line.get('amount', '')))
                    })
                    all_data.append(row)
            else:
                # Không có line sản phẩm, vẫn ghi 1 dòng
                row = {k: result.get(k, '') for k in fieldnames}
                all_data.append(row)
        else:
            print(f"⚠️ Không tìm thấy template phù hợp cho: {filename}")

# --- Ghi ra CSV ---
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for item in all_data:
        writer.writerow(item)

print(f"\n✅ Đã lưu kết quả vào: {output_csv}")
