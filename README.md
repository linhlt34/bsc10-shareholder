# 🏦 Hệ thống Tra cứu Thông tin Cổ đông

Ứng dụng web Streamlit cho phép cổ đông tra cứu thông tin đầu tư của mình một cách dễ dàng và trực quan.

## ✨ Tính năng

- 🔍 **Tra cứu theo ID**: Nhập ID cổ đông (họ tên không dấu + 6 số cuối STK)
- 📋 **Lịch sử giao dịch**: Xem chi tiết các lần chuyển tiền
- 📊 **Tổng kết đầu tư**: 
  - Tổng số tiền đã đầu tư
  - Tổng số ĐVĐT sở hữu
  - NAV hiện tại
  - Hiệu suất đầu tư (%)
- 📈 **Biểu đồ**: Trực quan hóa lịch sử đầu tư tích lũy

## 🚀 Cách chạy ứng dụng

### 1. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
streamlit run streamlit_app.py
```

### 3. Mở trình duyệt

Ứng dụng sẽ tự động mở tại địa chỉ: `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### Bước 1: Nhập thông tin
- **ID cổ đông**: Họ tên viết liền không dấu + 6-8 số cuối số tài khoản
  - Ví dụ: `NGUYENVANABC345678`
- **Giá ĐVĐT hiện tại**: Nhập giá trị hiện tại để tính NAV

### Bước 2: Tra cứu
- Nhấn nút "🔍 Tra cứu" để xem kết quả

### Bước 3: Xem kết quả
- **Lịch sử giao dịch**: Bảng chi tiết các lần chuyển tiền
- **Tổng kết**: Các chỉ số tài chính quan trọng
- **Biểu đồ**: Trực quan hóa quá trình đầu tư

## 📁 Cấu trúc file

```
bsc10/
├── streamlit_app.py      # Ứng dụng chính
├── data_shareholders.csv # Dữ liệu cổ đông
├── requirements.txt      # Thư viện cần thiết
└── README.md            # Hướng dẫn này
```

## 🔧 Yêu cầu hệ thống

- Python 3.7+
- Streamlit 1.28.0+
- Pandas 1.5.0+
- Numpy 1.24.0+

## 💡 Lưu ý

- File `data_shareholders.csv` phải có cùng thư mục với `streamlit_app.py`
- ID cổ đông phải chính xác (họ tên không dấu + 6 số cuối STK)
- Giá ĐVĐT hiện tại do cổ đông tự nhập để tính NAV chính xác

## 🆘 Xử lý lỗi

### Lỗi không tìm thấy ID
- Kiểm tra lại format ID: họ tên viết liền không dấu + 6 số cuối STK
- Xem gợi ý ID mẫu trong ứng dụng

### Lỗi encoding file CSV  
- Ứng dụng tự động thử các encoding: utf-8-sig, cp1252, latin-1

### Lỗi không tìm thấy file
- Đảm bảo `data_shareholders.csv` có trong cùng thư mục với `streamlit_app.py` 