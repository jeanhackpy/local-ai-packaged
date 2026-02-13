FROM node:22-bookworm-slim

# Set environment variables to allow Python tools to install dependencies and for better logging
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV PYTHONUNBUFFERED=1

# Add node user's local bin to PATH
ENV PATH="/home/node/.local/bin:${PATH}"

# Configure npm to use a global directory owned by node user
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH="/home/node/.npm-global/bin:${PATH}"

# Install basic dependencies and tools for the bot
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    build-essential \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libxkbcommon0 \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Change node user UID/GID to match host user (phil = 1001) - must be done as root
RUN usermod -u 1001 node && groupmod -g 1001 node

# Create npm global directory and set ownership
RUN mkdir -p /home/node/.npm-global && chown -R node:node /home/node/.npm-global

# Create directory structure with correct permissions
RUN mkdir -p /home/node/.openclaw/workspace /home/node/.openclaw/skills && \
    chown -R node:node /home/node/.openclaw

# Install OpenClaw CLI, Gemini CLI, and ClawHub globally as node user
USER node
RUN npm install -g openclaw@latest @google/gemini-cli clawhub

# Copy entrypoint script (as root for permissions, then switch back)
USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /home/node

# Expose gateway port
EXPOSE 18789

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:18789/health || exit 1

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
