GRIDOCTOR - TRỢ LÝ AI HỖ TRỢ NHẬN DIỆN VÀ TƯ VẤN
BỆNH, SÂU HẠI TRÊN CÂY DƯA LƯỚI

1. CÁCH CHẠY CHƯƠNG TRÌNH
- Nhấp đúp vào file: run_gridoctor.bat
- Chờ trình duyệt mở giao diện GRIDOCTOR.
- Nếu trình duyệt không tự mở, truy cập:
  http://localhost:8501

2. CÁCH SỬ DỤNG
- Chọn ảnh lá dưa cần kiểm tra.
- Bấm nút NHẬN DIỆN.
- Hệ thống sẽ hiển thị:
  + Tên bệnh hoặc sâu hại.
  + Độ tin cậy.
  + Thông tin tư vấn từ hệ thống RAG.

3. NGƯỠNG ĐỘ TIN CẬY
- Từ 70% trở lên: hệ thống cho phép hiển thị tư vấn RAG.
- Dưới 70%: hệ thống cảnh báo và yêu cầu chụp lại ảnh rõ hơn.

4. CÁC LỚP HỆ THỐNG HỖ TRỢ
- Cây dưa khỏe mạnh.
- Bệnh sương mai.
- Bệnh phấn trắng.
- Bọ trĩ.

5. CÁC THÀNH PHẦN CHÍNH
- YOLO: nhận diện hình ảnh.
- Sentence Transformers: tạo vector ngữ nghĩa.
- FAISS: tìm kiếm tài liệu.
- RAG: truy xuất kiến thức.
- Streamlit: giao diện người dùng.

6. LƯU Ý
GRIDOCTOR là hệ thống hỗ trợ. Kết quả không thay thế hoàn toàn
ý kiến của chuyên gia hoặc cán bộ kỹ thuật nông nghiệp.