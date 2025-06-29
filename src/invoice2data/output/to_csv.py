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

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = None  # Writer chưa khởi tạo

        for entry in data:
            # Nếu có field "lines" → mở rộng từng dòng
            lines = entry.get("lines", [])
            if isinstance(lines, list) and lines:
                for line in lines:
                    flat_row = {}

                    # Thêm thông tin hóa đơn vào từng dòng line item
                    for k, v in entry.items():
                        if k == "lines":
                            continue
                        if isinstance(v, datetime.datetime):
                            v = v.strftime(date_format)
                        flat_row[k] = v

                    # Thêm các trường trong 1 dòng sản phẩm
                    for k, v in line.items():
                        flat_row[k] = v

                    # Khởi tạo header lần đầu
                    if writer is None:
                        writer = csv.DictWriter(csv_file, fieldnames=list(flat_row.keys()))
                        writer.writeheader()

                    writer.writerow(flat_row)

            else:
                # Không có dòng sản phẩm → ghi dòng thông thường
                row = {}
                for k, v in entry.items():
                    if isinstance(v, datetime.datetime):
                        v = v.strftime(date_format)
                    row[k] = v

                if writer is None:
                    writer = csv.DictWriter(csv_file, fieldnames=list(row.keys()))
                    writer.writeheader()

                writer.writerow(row)
