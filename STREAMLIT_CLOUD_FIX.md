# 🔧 Sửa Lỗi Streamlit Cloud Deployment

## ❌ Lỗi Thường Gặp

### Lỗi: `ConfigOptionError: The value of server.port is not allowed`

**Nguyên nhân:** File cấu hình `.streamlit/config.toml` có setting `server.port` mà Streamlit Cloud không cho phép.

## ✅ Cách Sửa

### Bước 1: Kiểm tra file config
```bash
# Kiểm tra xem có file config không
ls -la .streamlit/
```

### Bước 2: Xóa hoặc sửa file config
```bash
# Xóa file config nếu có
rm .streamlit/config.toml

# Hoặc tạo file config mới với cấu hình đúng
```

### Bước 3: Tạo file config đúng
Tạo file `.streamlit/config.toml` với nội dung:

```toml
[global]
developmentMode = false

[server]
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## ⚠️ Lưu Ý Quan Trọng

1. **KHÔNG** set `server.port` trong config
2. **KHÔNG** sử dụng `--server.port` trong lệnh chạy
3. Streamlit Cloud sẽ tự động quản lý port

## 🚀 Lệnh Chạy Đúng

```bash
# ✅ Đúng
streamlit run streamlit_app.py --server.headless true

# ❌ Sai
streamlit run streamlit_app.py --server.port 8501
```

## 📁 Cấu Trúc Dự Án Chuẩn

```
bsc10/
├── streamlit_app.py          # File chính
├── requirements.txt           # Dependencies
├── data_shareholders.csv     # Dữ liệu
├── .streamlit/
│   └── config.toml          # Config (không có server.port)
└── README.md
```

## 🔍 Kiểm Tra Trước Deploy

1. ✅ File `streamlit_app.py` tồn tại
2. ✅ File `requirements.txt` có đầy đủ dependencies
3. ✅ Không có `server.port` trong config
4. ✅ Test chạy local thành công

## 📞 Hỗ Trợ

Nếu vẫn gặp lỗi, kiểm tra:
- Logs trong Streamlit Cloud
- Cấu hình file `.streamlit/config.toml`
- Dependencies trong `requirements.txt` 