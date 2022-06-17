# Giới thiệu project ứng dụng quản lý thư viện
Mục tiêu của project là xây dựng thành công một web app quản lý thư viện giúp giảm bớt tính thủ công trong các hoạt động của các nhân viên thư viện cũng như của khách hàng, khiến các thao tác tìm kiếm, ghi chép dữ liệu của sách cũng như tên khách hàng mượn sách,.. trở nên dễ dàng, nhanh chóng và chính xác hơn.

Chúng tôi cung cấp các tính năng đăng nhập cho độc giả cũng như nhân viên thư viện. Đồng thời, nhân viên thư viện cũng có thể thêm, cập nhật, xóa,... các dữ liệu về sách cũng như là về khách hàng. Đồng thời độc giả cũng có thể mượn, trả sách, xem toàn bộ cơ sở dữ liệu công khai của thư viện.
# Model
![alt text](https://github.com/12-group/project-library-management-system/blob/main/erd.jpg?raw=true)
# Môi trường thực thi
- Hệ điều hành Windows 10
- Dev Tools: Visual Studio Code, Sublime Text
- Python version: 3.9.7
- Django version: 4.0.1
- Cơ sở dữ liệu: SQLite
- Python Package cần thiết: trong file "requirements.txt"
# Hướng dẫn cấu hình project chạy local PC
1. Mở **Command Prompt**, tìm đường dẫn tới project.
2. Nếu là lần đầu chạy project, hãy sử dụng lệnh dưới đây để xây dựng cơ sở dữ liệu (những lần sau thì không cần nữa):
	```
	python manage.py migrate --run-syncdb
	```
3. Chạy server bằng lệnh sau đây:
	```
	python manage.py runserver
	```
4. Mở trình duyệt và truy cập http://localhost:8000 (hoặc http://127.0.0.1:8000) để truy cập hệ thống.
5. Đăng nhập vào **tài khoản quản lý** được hệ thống cung cấp và đổi mật khẩu mới:
	``Tên đăng nhập mặc định: manager``
	``Mật khẩu mặc định: password``
6. Dùng **tài khoản quản lý** này để thêm các nhân viên khác. Từ đó, tiếp cận các chức năng của hệ thống.
# Hướng dẫn deploy project lên Heroku

# Link video demo

# Current status
- Mô hình ERD cho hệ thống.
- Hoàn thành màn hình đăng ký, đăng nhập.
- Hoàn thành màn hình cập nhật thông tin tài khoản.
- Hoàn thành các màn hình cho thủ thư, thủ quỹ, thủ kho, quản lý, độc giả, khách.
- Thêm các ràng buộc, quy định.
- Đã xong phân quyền (trang chủ, trang thông tin chi tiết của sách nhân viên có thể xem được nhưng không thể mượn)
- Chưa có chức năng lập báo cáo.
# Future works
- Demo video
- Sửa toàn bộ template thành tiếng việt
