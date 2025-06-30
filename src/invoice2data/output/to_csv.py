import csv
import datetime
from typing import Any, Dict, List

def write_to_file(
    data: List[Dict[str, Any]], path: str, date_format: str = "%Y-%m-%d"
) -> None:
    if not path.endswith(".csv"):
        filename = path + ".csv"
    else:
        filename = path

    # ✅ Định nghĩa danh sách field bắt buộc (theo đúng thứ tự yêu cầu)
    required_fields = [
        "invoice_number", "date", "seller", "seller_tax_code", "seller_address", "seller_phone",
        "seller_bank_account", "buyer_name", "buyer", "buyer_tax_id", "buyer_address", "payment_method",
        "buyer_bank_account", "vat_rate", "amount_untaxed", "amount_tax", "amount_total", "amount",
        "item_no","description","unit", "qty", "unit_price", "line_total"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=required_fields)
        writer.writeheader()

        for entry in data:
            lines = entry.get("lines", [])
            if isinstance(lines, list) and lines:
                for line in lines:
                    flat_row = {field: "" for field in required_fields}

                    # Gộp các field trong hóa đơn
                    for k, v in entry.items():
                        if k == "lines":
                            continue
                        if isinstance(v, datetime.datetime):
                            v = v.strftime(date_format)
                        if k in flat_row:
                            flat_row[k] = v

                    # Gộp các field trong 1 dòng sản phẩm
                    for k, v in line.items():
                        if k in flat_row:
                            flat_row[k] = v

                    writer.writerow(flat_row)
            else:
                row = {field: "" for field in required_fields}
                for k, v in entry.items():
                    if isinstance(v, datetime.datetime):
                        v = v.strftime(date_format)
                    if k in row:
                        row[k] = v
                writer.writerow(row)
