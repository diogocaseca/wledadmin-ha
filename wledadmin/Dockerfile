# Imagem Python (Debian) em vez da base Alpine do HA: todas as dependências do wledadmin
# têm pacotes prontos (wheels) para amd64 e aarch64 nela, então o build no HA é rápido.
FROM python:3.12-slim-bookworm

ARG BUILD_VERSION
ARG BUILD_ARCH
# Versão (tag) do wledadmin instalada. Mantenha igual à "version" do config.yaml.
ARG WLEDADMIN_VERSION=0.5.0
ARG WLEDADMIN_SOURCE=https://github.com/diogocaseca/wledadmin/archive/refs/tags/v${WLEDADMIN_VERSION}.tar.gz

COPY --from=ghcr.io/astral-sh/uv:0.13 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/wledadmin/.venv \
    PYTHONUNBUFFERED=1

WORKDIR /opt/wledadmin
ADD ${WLEDADMIN_SOURCE} /tmp/wledadmin.tar.gz
# --frozen: instala exatamente as versões do uv.lock daquela tag
RUN tar -xzf /tmp/wledadmin.tar.gz --strip-components=1 -C /opt/wledadmin \
    && rm /tmp/wledadmin.tar.gz \
    && uv sync --frozen --no-dev \
    && rm -rf /root/.cache

COPY run.py /run.py

LABEL \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="app" \
    io.hass.arch="aarch64|amd64"

CMD ["/opt/wledadmin/.venv/bin/python", "/run.py"]
