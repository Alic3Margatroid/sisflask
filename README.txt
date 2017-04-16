Bài này em viết trên virtualenv, anh/chị dùng nếu thấy cần thiết

- Các thư viện cần cài:
flask, flask-login, flask-wtf, flask-sqlalchemy, sqlalchemy-migrate, flask-whooshalchemy

- Chạy run.py để khởi động. Web app chạy port 5000
- Database có sẵn 2 tài khoản admin và john cùng password là 123 để test. admin có đầy đủ quyền admin
- Student List thực hiện chức năng liệt kê người dùng
  Profile để xem thông tin bản thân. Trong đó có Edit để sửa thông tin
  Exercises thực hiện việc giao bài tập để download và sv upload bài tập
  Uploadlist để gv xem list bài tập sv đã upload
  Challenges để thực hiện việc tổ chức trò chơi giải đố

- Upload file ở đây chỉ giới hạn với file .txt

- Thư mục chứa exercises và challenges sẽ được tạo động, cụ thể trên windows là trong ./instance/ex và ./instance/ch