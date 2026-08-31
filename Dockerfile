# Gunakan base image Python resmi
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy kebutuhan dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
COPY . .

# Expose port yang digunakan Streamlit
EXPOSE 8080

# Jalankan Streamlit pada port 8080 (standar Google Cloud Run)
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]