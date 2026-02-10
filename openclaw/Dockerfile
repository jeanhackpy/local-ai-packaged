FROM node:22-bookworm-slim

# Set environment variables to allow Python tools to install dependencies and for better logging
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV PYTHONUNBUFFERED=1

# Add node user's local bin to PATH
ENV PATH="/home/node/.local/bin:${PATH}"

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
    && rm -rf /var/lib/apt/lists/*

# Install OpenClaw CLI, Gemini CLI, and ClawHub globally
RUN npm install -g openclaw@latest @google/gemini-cli clawhub

# Create directory structure with correct permissions
RUN mkdir -p /home/node/.openclaw/workspace /home/node/.openclaw/skills

# Set ownership to node user
RUN chown -R node:node /home/node/.openclaw

# Change node user UID/GID to match host user (phil = 1001)
RUN usermod -u 1001 node && groupmod -g 1001 node

# Switch to non-root user
USER node
WORKDIR /home/node

# Expose gateway port
EXPOSE 18789

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:18789/health || exit 1

# Start the gateway
CMD ["openclaw", "gateway", "run"]
