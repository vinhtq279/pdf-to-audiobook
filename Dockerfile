# Sử dụng Python Slim image để tối ưu dung lượng (Base Image)
FROM python:3.9-slim

# Thiết lập biến môi trường để log mượt mà hơn (không bị buffer)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file dependencies trước (tận dụng Docker Layer Caching)
COPY requirements.txt .

# Cài đặt thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào
COPY . .

# Tạo thư mục output volume (để map ra ngoài máy host)
RUN mkdir output

# Entrypoint mặc định
# Khi chạy container, người dùng chỉ cần truyền tham số file PDF
# Cập nhật lệnh chạy: Gọi module src.main thay vì file script lẻ
ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--help"]
