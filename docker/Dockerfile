# Dockerfile with optional Home Assistant API integration
# ----------------------------------------------------
# Build‑time argument to enable the optional Home Assistant API feature.
# By default it is disabled (value 0). When ENABLE_HA=1 the build will
# copy a stub of the HA integration into the image. The actual API
# implementation is left to the user – this repository only provides the
# scaffolding.

ARG ENABLE_HA=0

# ---------- Build stage ----------
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# If the HA API feature is enabled, copy the optional integration files.
COPY src /app/src
COPY optional/ha_integration /app/ha_integration

# ---------- Runtime stage ----------
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY src ./src
COPY scripts/bootstrap.sh .
RUN chmod +x bootstrap.sh

# If the optional HA integration was copied during the build it will be
# present under /app/ha_integration. The entrypoint can import it when
# ENABLE_HA is set at runtime.
ENV ENABLE_HA=${ENABLE_HA}

ENTRYPOINT ["python", "-m", "src.voice_loop"]
