# ---------- Build stage ----------
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ---------- Runtime stage ----------
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY src ./src
COPY scripts/bootstrap.sh .
RUN chmod +x bootstrap.sh

# Entrypoint runs the voice loop
ENTRYPOINT ["python", "-m", "src.voice_loop"]
