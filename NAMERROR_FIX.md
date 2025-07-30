# 🔧 Sửa Lỗi NameError trong Streamlit App

## ❌ Lỗi Thường Gặp

### Lỗi: `NameError: name 'main_transactions' is not defined`

**Nguyên nhân:** Biến `main_transactions` không được định nghĩa hoặc có lỗi trong quá trình xử lý dữ liệu.

## ✅ Cách Sửa

### Bước 1: Kiểm tra hàm main() được gọi

Đảm bảo cuối file `streamlit_app.py` có:

```python
if __name__ == "__main__":
    main()
```

### Bước 2: Kiểm tra hàm load_data()

Đảm bảo hàm `load_data()` trả về dữ liệu đúng:

```python
@st.cache_data
def load_data():
    try:
        # Đọc file CSV
        df = pd.read_csv('data_shareholders.csv', encoding='utf-8-sig')
        
        # Xử lý dữ liệu
        main_transactions = df[mask].copy()
        
        # Trả về kết quả
        return main_transactions
        
    except Exception as e:
        st.error(f"❌ **Lỗi:** {e}")
        return None
```

### Bước 3: Kiểm tra validation trong main()

```python
def main():
    # Tải dữ liệu
    df = load_data()
    if df is None:
        st.error("❌ Không thể tải dữ liệu")
        st.stop()
    
    # Kiểm tra DataFrame rỗng
    if df.empty:
        st.error("❌ DataFrame rỗng")
        st.stop()
```

## 🔍 Debug Steps

### 1. Test Import
```python
python -c "from streamlit_app import load_data; print('✅ Import OK')"
```

### 2. Test Load Data
```python
python -c "from streamlit_app import load_data; df = load_data(); print(f'Rows: {len(df)}' if df is not None else 'None')"
```

### 3. Test Main Function
```python
python -c "from streamlit_app import main; print('✅ Main function OK')"
```

## ⚠️ Các Lỗi Thường Gặp

### 1. File CSV không tồn tại
```
FileNotFoundError: [Errno 2] No such file or directory: 'data_shareholders.csv'
```
**Giải pháp:** Đảm bảo file `data_shareholders.csv` tồn tại trong thư mục.

### 2. Encoding lỗi
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```
**Giải pháp:** Thử các encoding khác: `cp1252`, `latin-1`

### 3. DataFrame rỗng
```
ValueError: No objects to concatenate
```
**Giải pháp:** Kiểm tra dữ liệu trong file CSV

### 4. Cột không tồn tại
```
KeyError: 'column_name'
```
**Giải pháp:** Kiểm tra tên cột trong file CSV

## 🚀 Lệnh Test

```bash
# Test import
python -c "import streamlit_app; print('✅ OK')"

# Test load data
python -c "from streamlit_app import load_data; df = load_data(); print(f'Data: {len(df)} rows')"

# Test run app
streamlit run streamlit_app.py --server.headless true
```

## 📋 Checklist

- ✅ File `streamlit_app.py` có `if __name__ == "__main__": main()`
- ✅ File `data_shareholders.csv` tồn tại
- ✅ Hàm `load_data()` trả về DataFrame hoặc None
- ✅ Hàm `main()` có validation cho df
- ✅ Test chạy local thành công

## 📞 Hỗ Trợ

Nếu vẫn gặp lỗi:
1. Kiểm tra logs trong terminal
2. Kiểm tra file CSV có dữ liệu không
3. Kiểm tra encoding của file CSV
4. Test từng hàm riêng lẻ 