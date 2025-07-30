# 🚀 Hướng dẫn Deploy Ứng dụng lên Streamlit Cloud

## ⚠️ **QUAN TRỌNG: BẢO MẬT DỮ LIỆU**
**Repository PHẢI ở chế độ PRIVATE để bảo vệ dữ liệu cổ đông!**

---

## 📋 **Checklist chuẩn bị**
- ✅ File `streamlit_app.py` đã hoàn thiện
- ✅ File `requirements.txt` đã có đầy đủ dependencies
- ✅ File `data_shareholders.csv` có trong dự án
- ✅ File `.gitignore` đã được tạo
- ⚠️ Git đã được cài đặt

---

## 🛠️ **Bước 1: Cài đặt Git (nếu chưa có)**

### Cách 1: Download trực tiếp
1. Truy cập: https://git-scm.com/download/win
2. Tải và cài đặt Git for Windows (64-bit)
3. Restart PowerShell sau khi cài xong

### Cách 2: Dùng winget (Windows 10/11)
```powershell
winget install --id Git.Git -e --source winget
```

### Kiểm tra cài đặt
```powershell
git --version
```

---

## 🔐 **Bước 2: Tạo Private Repository trên GitHub**

1. **Đăng nhập GitHub:** https://github.com
2. **Tạo repo mới:**
   - Nhấn dấu `+` góc trên phải → "New repository"
   - **Repository name:** `bsc-shareholder-app` (hoặc tên khác)
   - ⚠️ **QUAN TRỌNG:** Chọn 🔒 **Private**
   - Nhấn "Create repository"

3. **Lưu URL repo:** Sẽ có dạng:
   ```
   https://github.com/YOUR_USERNAME/bsc-shareholder-app.git
   ```

---

## 📤 **Bước 3: Upload code lên GitHub**

Mở PowerShell trong thư mục `bsc10` và chạy:

```powershell
# 1. Khởi tạo Git repository
git init

# 2. Cấu hình Git (nếu chưa làm bao giờ)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Thêm tất cả files
git add .

# 4. Kiểm tra files sẽ được commit
git status

# 5. Commit lần đầu
git commit -m "Initial commit: BSC shareholder lookup app"

# 6. Kết nối với GitHub repo (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/bsc-shareholder-app.git

# 7. Tạo branch main
git branch -M main

# 8. Push code lên GitHub
git push -u origin main
```

**⚠️ Lưu ý:** GitHub có thể yêu cầu đăng nhập. Sử dụng **Personal Access Token** thay vì password.

---

## 🌐 **Bước 4: Deploy lên Streamlit Cloud**

1. **Truy cập:** https://share.streamlit.io

2. **Đăng nhập bằng GitHub**

3. **Tạo app mới:**
   - Nhấn "New app"
   - **Repository:** Chọn `bsc-shareholder-app` (private repo)
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`

4. **Deploy:**
   - Nhấn "Deploy!"
   - Đợi vài phút để build

---

## 🎯 **Bước 5: Kiểm tra ứng dụng**

Sau khi deploy thành công:

1. ✅ **Kiểm tra trang chủ** hiển thị đúng
2. ✅ **Test tra cứu** với 1-2 ID mẫu
3. ✅ **Kiểm tra tính năng What-if** hoạt động
4. ✅ **Test download Excel** chạy được
5. ✅ **Kiểm tra biểu đồ** hiển thị tooltip

---

## 🔧 **Xử lý lỗi thường gặp**

### Lỗi "Module not found"
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Redeploy app

### Lỗi "File not found: data_shareholders.csv"
- Đảm bảo file CSV có trong repository
- Kiểm tra tên file chính xác
- Recheck git add . đã include file CSV

### Lỗi encoding CSV
- App đã xử lý tự động nhiều encoding
- Nếu vẫn lỗi, kiểm tra file CSV có bị corrupt không

---

## 📱 **Bước 6: Chia sẻ ứng dụng**

Sau khi deploy thành công, bạn sẽ có:

- **URL công khai:** `https://yourapp.streamlit.app`
- **Repository private:** Chỉ bạn thấy được code và data
- **Ứng dụng public:** Mọi người có thể sử dụng

**⚠️ Quan trọng:** Chỉ chia sẻ URL ứng dụng, KHÔNG chia sẻ link GitHub repository!

---

## 🔄 **Cập nhật ứng dụng sau này**

Khi cần thay đổi code hoặc dữ liệu:

```powershell
# 1. Chỉnh sửa files
# 2. Commit và push
git add .
git commit -m "Update: mô tả thay đổi"
git push

# 3. Streamlit Cloud sẽ tự động redeploy
```

---

## 📞 **Hỗ trợ**

Nếu gặp vấn đề:
1. Kiểm tra logs tại Streamlit Cloud dashboard
2. Đảm bảo repository là Private
3. Verify file CSV có trong repo và đúng encoding
4. Check requirements.txt đầy đủ 