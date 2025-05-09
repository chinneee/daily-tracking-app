# 📊 ASIN Daily & Weekly Tracking Web

**ASIN Daily & Weekly Tracking Web** là một ứng dụng web nội bộ được xây dựng dành riêng cho team **Amazon PPC**. Ứng dụng giúp tự động hóa quá trình xử lý và cập nhật dữ liệu từ các báo cáo hàng ngày, từ đó đẩy dữ liệu đã chuẩn hóa lên Google Sheets — nơi được kết nối trực tiếp với Google Looker Studio để trực quan hóa và theo dõi hiệu suất ASIN một cách hiệu quả.

---

## 🚀 Mục tiêu

- Loại bỏ quy trình cập nhật thủ công, vốn mất thời gian và dễ sai sót.
- Hỗ trợ quản lý nắm bắt nhanh các chỉ số chính như Sessions, Units Ordered, Clicks từ quảng cáo, và Ad Spend theo từng ASIN và theo ngày.
- Tự động kết nối với Google Sheets và Looker Studio để phục vụ phân tích và ra quyết định.

---

## 🧩 Tính năng

- Tải lên và xử lý đồng thời 2 báo cáo: **Business Report** và **Ads Report**.
- Hợp nhất dữ liệu, chuẩn hóa cột, và thêm cột ngày báo cáo.
- Hiển thị bảng dữ liệu đã xử lý ngay trên giao diện.
- Tải xuống file Excel chứa bảng tổng hợp.
- Tùy chọn đẩy dữ liệu lên **Google Sheets** (được kết nối với Looker Studio).
- Lọc theo khoảng ngày và chỉ định dòng bắt đầu để cập nhật dữ liệu chính xác.

---

## 📁 Yêu cầu đầu vào

- **Business Report (CSV)** với các cột:
  - `(Parent) ASIN`, `(Child) ASIN`, `Sessions - Total`, `Units Ordered`
- **Ads Report (CSV)** với các cột:
  - `Products`, `Clicks`, `Spend(USD)`
- **Ngày báo cáo** (định dạng: `YYYY-MM-DD`)
- **Google Service Account Credential JSON** (dành cho thao tác ghi vào Google Sheets)

---

## 🔧 Công nghệ sử dụng

- `Streamlit` — Xây dựng UI nhanh chóng và thân thiện.
- `Pandas` — Xử lý và làm sạch dữ liệu.
- `gspread + gspread_dataframe` — Kết nối và ghi dữ liệu lên Google Sheets.
- `Google OAuth2` — Xác thực bằng Service Account để truy cập Google Sheets.

---

## ⚙️ Cách sử dụng

1. Chạy ứng dụng:
   ```bash
   streamlit run app.py
2. Trên giao diện:

- Upload **Business Report** và **Ads Report** (định dạng CSV).
- Nhập **ngày báo cáo** theo định dạng `YYYY-MM-DD`.
- Có thể:
  - Tải xuống file Excel đã hợp nhất.
  - Hoặc đẩy dữ liệu lên **Google Sheets**.

### Nếu chọn đẩy lên Google Sheets:

- Lọc theo **khoảng ngày**.
- Nhập **dòng bắt đầu** để ghi dữ liệu chính xác.
- Upload **Google Service Account Credential JSON** để xác thực.

---

## 🔒 Bảo mật

Ứng dụng sử dụng **Google Service Account JSON file** để xác thực một cách bảo mật.  
Thông tin xác thực **không được lưu trữ hay ghi nhớ** sau khi phiên làm việc kết thúc.

---

## 🔮 Định hướng phát triển

- Tự động hóa lịch cập nhật (*schedule push*).
- Hỗ trợ thêm tracking theo **tuần/tháng**.
- Thêm **dashboard nội bộ** theo vai trò người dùng.
- Tự động gửi báo cáo định kỳ qua **email** hoặc **Slack**.

---

## 🧑‍💻 Tác giả

**Nguyễn Thùy Trinh**  
*Data Analyst Intern @ Amazon-focused eCommerce Team*

---

## 📎 Liên kết hữu ích

- [Google Looker Studio](https://lookerstudio.google.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Gspread Documentation](https://gspread.readthedocs.io/)

---

> *"Automate the manual, so you can focus on the meaningful."*

