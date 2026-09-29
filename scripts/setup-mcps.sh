#!/usr/bin/env bash
# ==============================================================================
# Open Anime Tracker - Universal MCP Setup Script
# ==============================================================================
# Sets up, pre-caches, and configures all Model Context Protocol (MCP) servers
# required for AI agent debugging and full-stack development on any workstation.
# ==============================================================================

set -euo pipefail

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
NC="\033[0m"

log_info() {
    printf "${BLUE}ℹ${NC} %s\n" "$*"
}

log_success() {
    printf "${GREEN}✔${NC} %s\n" "$*"
}

log_warn() {
    printf "${YELLOW}⚠${NC} %s\n" "$*"
}

log_error() {
    printf "${RED}✖${NC} %s\n" "$*"
}

log_header() {
    printf "\n${BOLD}${CYAN}=== %s ===${NC}\n\n" "$*"
}

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Global Antigravity config path
GLOBAL_CONFIG_DIR="${HOME}/.gemini/config"
GLOBAL_CONFIG_FILE="${GLOBAL_CONFIG_DIR}/mcp_config.json"

# Workspace plugin paths
PLUGIN_DIR="${PROJECT_DIR}/.agents/plugins/oat-dev-tools"
PLUGIN_CONFIG_FILE="${PLUGIN_DIR}/mcp_config.json"

# Default execution mode
MODE="both" # "both", "project", "global"
DRY_RUN=false
CHECK_ONLY=false
SKIP_CACHE=false
SKIP_BROWSER=false

show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Installs, pre-caches, and configures Model Context Protocol (MCP) servers for Open Anime Tracker.

Options:
  -h, --help           Show this help message and exit
  --dry-run            Simulate execution and print generated configurations without modifying files
  --check              Check prerequisites, connectivity, and existing MCP config only
  --project-only       Configure only the workspace plugin (.agents/plugins/oat-dev-tools/mcp_config.json)
  --global-only        Configure only global Antigravity config (~/.gemini/config/mcp_config.json)
  --skip-cache         Skip pre-downloading and pre-caching MCP packages
  --skip-browser       Skip downloading Playwright browser binaries (Chromium)

MCP Servers Configured:
  - postgres           PostgreSQL schema & data inspection (@modelcontextprotocol/server-postgres)
  - redis              Redis session & cache inspection (redis-mcp-server)
  - playwright         React frontend browser automation & testing (@playwright/mcp@latest)
  - fetch              Backend REST & external API fetching (@modelcontextprotocol/server-fetch)
  - git                Git history & working tree inspection (@modelcontextprotocol/server-git)
  - sequential-thinking Complex multi-step reasoning & architecture analysis

EOF
}

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --check)
            CHECK_ONLY=true
            shift
            ;;
        --project-only)
            MODE="project"
            shift
            ;;
        --global-only)
            MODE="global"
            shift
            ;;
        --skip-cache)
            SKIP_CACHE=true
            shift
            ;;
        --skip-browser)
            SKIP_BROWSER=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

log_header "Open Anime Tracker - MCP Setup"

# Ensure common user binary directories are in PATH
export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${PATH}"

# ------------------------------------------------------------------------------
# 1. Prerequisite Checks
# ------------------------------------------------------------------------------
log_header "1. Checking Prerequisites"

# Node & npx
if ! command -v node >/dev/null 2>&1; then
    log_error "Node.js is not installed or not in PATH."
    log_info "Please install Node.js (v18 or v20+ recommended). E.g. via fnm, nvm, or your system package manager."
    exit 1
fi

NODE_VERSION=$(node -v)
log_success "Node.js detected: ${NODE_VERSION}"

if ! command -v npx >/dev/null 2>&1; then
    log_error "npx is not installed or not in PATH."
    exit 1
fi
log_success "npx detected: $(command -v npx)"

# Python
if ! command -v python3 >/dev/null 2>&1; then
    log_error "python3 is not installed or not in PATH."
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
log_success "Python detected: ${PYTHON_VERSION}"

# uv & uvx
UVX_BIN=""
if command -v uvx >/dev/null 2>&1; then
    UVX_BIN="$(command -v uvx)"
elif [[ -x "${HOME}/.local/bin/uvx" ]]; then
    UVX_BIN="${HOME}/.local/bin/uvx"
elif [[ -x "${HOME}/.cargo/bin/uvx" ]]; then
    UVX_BIN="${HOME}/.cargo/bin/uvx"
fi

if [[ -z "${UVX_BIN}" ]]; then
    log_warn "uv / uvx was not found in PATH or standard user directories (~/.local/bin, ~/.cargo/bin)."
    log_info "Attempting to install uv using official installer (curl -LsSf https://astral.sh/uv/install.sh | sh)..."
    if ! ${DRY_RUN}; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="${HOME}/.local/bin:${PATH}"
        if [[ -x "${HOME}/.local/bin/uvx" ]]; then
            UVX_BIN="${HOME}/.local/bin/uvx"
            log_success "Installed uv successfully: ${UVX_BIN}"
        else
            log_error "Failed to locate uvx after installation."
            exit 1
        fi
    else
        log_info "[DRY-RUN] Would install uv via official installer script."
        UVX_BIN="${HOME}/.local/bin/uvx"
    fi
else
    log_success "uvx detected: ${UVX_BIN}"
fi

# Container runtime
CONTAINER_CMD=""
if command -v docker >/dev/null 2>&1; then
    CONTAINER_CMD="docker compose"
    log_success "Docker detected: $(docker --version)"
elif command -v podman >/dev/null 2>&1; then
    CONTAINER_CMD="podman compose"
    log_success "Podman detected: $(podman --version)"
else
    log_warn "Neither Docker nor Podman was detected. Make sure your database/redis containers can run."
fi

# ------------------------------------------------------------------------------
# 2. Environment Resolution
# ------------------------------------------------------------------------------
log_header "2. Resolving Project Environment & Connection Strings"

ENV_FILE="${PROJECT_DIR}/.env"
if [[ -f "${ENV_FILE}" ]]; then
    log_info "Reading environment variables from ${ENV_FILE}"
    # Read variables without executing arbitrary code
    PG_USER=$(grep -E '^[[:space:]]*POSTGRES_USER=' "${ENV_FILE}" | cut -d '=' -f2- | tr -d '"' | tr -d "'" | tr -d '\r' || true)
    PG_PW=$(grep -E '^[[:space:]]*POSTGRES_PASSWORD=' "${ENV_FILE}" | cut -d '=' -f2- | tr -d '"' | tr -d "'" | tr -d '\r' || true)
    PG_PORT=$(grep -E '^[[:space:]]*PG_PORT=' "${ENV_FILE}" | cut -d '=' -f2- | tr -d '"' | tr -d "'" | tr -d '\r' || true)
    REDIS_IP=$(grep -E '^[[:space:]]*REDIS_IP=' "${ENV_FILE}" | cut -d '=' -f2- | tr -d '"' | tr -d "'" | tr -d '\r' || true)
else
    log_warn ".env file not found in ${PROJECT_DIR}. Using default development settings."
fi

# Fallback defaults matching docker-compose.yml and database.py
PG_USER="${PG_USER:-postgres}"
PG_PW="${PG_PW:-postgres}"
PG_PORT="${PG_PORT:-5432}"
PG_DB="db"
REDIS_IP="${REDIS_IP:-127.0.0.1}"
REDIS_PORT="6379"

DATABASE_URL="postgresql://${PG_USER}:${PG_PW}@localhost:${PG_PORT}/${PG_DB}"
REDIS_URL="redis://${REDIS_IP}:${REDIS_PORT}/0"

log_info "PostgreSQL URL: postgresql://${PG_USER}:****@localhost:${PG_PORT}/${PG_DB}"
log_info "Redis URL:      redis://${REDIS_IP}:${REDIS_PORT}/0"

# ------------------------------------------------------------------------------
# 3. Connectivity Checks
# ------------------------------------------------------------------------------
log_header "3. Checking Service Connectivity"

check_port() {
    local host="$1"
    local port="$2"
    python3 -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1.5)
try:
    s.connect(('${host}', int('${port}')))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" >/dev/null 2>&1
}

if check_port "127.0.0.1" "${PG_PORT}"; then
    log_success "PostgreSQL is reachable on port ${PG_PORT}."
else
    log_warn "PostgreSQL is not responding on port ${PG_PORT}."
    if [[ -n "${CONTAINER_CMD}" ]]; then
        log_info "Start infrastructure with: ${CONTAINER_CMD} up -d"
    fi
fi

if check_port "${REDIS_IP}" "${REDIS_PORT}"; then
    log_success "Redis is reachable on port ${REDIS_PORT}."
else
    log_warn "Redis is not responding on port ${REDIS_PORT}."
    if [[ -n "${CONTAINER_CMD}" ]]; then
        log_info "Start infrastructure with: ${CONTAINER_CMD} up -d"
    fi
fi

if ${CHECK_ONLY}; then
    log_header "Check Complete"
    exit 0
fi

# ------------------------------------------------------------------------------
# 4. Package Pre-Caching & Browser Installation
# ------------------------------------------------------------------------------
if ! ${SKIP_CACHE}; then
    log_header "4. Pre-caching MCP Packages"

    if ${DRY_RUN}; then
        log_info "[DRY-RUN] Skipping package download and caching."
    else
        log_info "Pre-caching Node MCP packages to npm cache..."
        npm cache add \
            @modelcontextprotocol/server-postgres \
            @playwright/mcp@latest \
            @modelcontextprotocol/server-sequential-thinking \
            >/dev/null 2>&1 || log_warn "npm cache add completed with warnings."

        log_info "Pre-caching Python MCP packages via uv..."
        timeout 10s "${UVX_BIN}" --from redis-mcp-server@latest redis-mcp-server --help </dev/null >/dev/null 2>&1 || true
        timeout 10s "${UVX_BIN}" --from mcp-server-fetch mcp-server-fetch --help </dev/null >/dev/null 2>&1 || true
        timeout 10s "${UVX_BIN}" --from mcp-server-git mcp-server-git --help </dev/null >/dev/null 2>&1 || true

        if ! ${SKIP_BROWSER}; then
            log_info "Installing Playwright Chromium browser binaries..."
            npx playwright install chromium || log_warn "Playwright browser installation had warnings; may need system dependencies."
        fi

        log_success "MCP packages pre-cached successfully."
    fi
else
    log_info "Skipping package pre-caching (--skip-cache)."
fi

# ------------------------------------------------------------------------------
# 5. Build Configuration Payloads
# ------------------------------------------------------------------------------
log_header "5. Generating MCP Configurations"

# Generate servers JSON dictionary
SERVERS_JSON=$(python3 -c "
import json

servers = {
    'postgres': {
        'command': 'npx',
        'args': [
            '-y',
            '@modelcontextprotocol/server-postgres',
            '${DATABASE_URL}'
        ]
    },
    'redis': {
        'command': '${UVX_BIN}',
        'args': [
            '--from',
            'redis-mcp-server@latest',
            'redis-mcp-server',
            '--url',
            '${REDIS_URL}'
        ],
        'env': {
            'PYTHONUNBUFFERED': '1'
        }
    },
    'playwright': {
        'command': 'npx',
        'args': [
            '-y',
            '@playwright/mcp@latest'
        ]
    },
    'fetch': {
        'command': '${UVX_BIN}',
        'args': [
            '--from',
            'mcp-server-fetch',
            'mcp-server-fetch'
        ]
    },
    'git': {
        'command': '${UVX_BIN}',
        'args': [
            '--from',
            'mcp-server-git',
            'mcp-server-git',
            '--repository',
            '${PROJECT_DIR}'
        ]
    },
    'sequential-thinking': {
        'command': 'npx',
        'args': [
            '-y',
            '@modelcontextprotocol/server-sequential-thinking'
        ]
    }
}
print(json.dumps(servers))
")

# Helper to merge JSON into a destination file
merge_mcp_config() {
    local target_file="$1"
    local servers_data="$2"

    python3 -c "
import json, os, sys

target_path = os.path.expanduser('${target_file}')
os.makedirs(os.path.dirname(target_path), exist_ok=True)

existing_data = {}
if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except Exception as e:
        print(f'Warning: Could not parse existing {target_path} ({e}), creating backup.', file=sys.stderr)
        os.rename(target_path, target_path + '.backup')
        existing_data = {}

if not isinstance(existing_data, dict):
    existing_data = {}

if 'mcpServers' not in existing_data or not isinstance(existing_data['mcpServers'], dict):
    existing_data['mcpServers'] = {}

new_servers = json.loads('''${servers_data}''')
for name, config in new_servers.items():
    existing_data['mcpServers'][name] = config

with open(target_path, 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, indent=2)
    f.write('\n')

print(f'Successfully updated {target_path}')
"
}

# 1. Workspace Plugin Configuration
if [[ "${MODE}" == "both" || "${MODE}" == "project" ]]; then
    if ${DRY_RUN}; then
        log_info "[DRY-RUN] Target Workspace Plugin: ${PLUGIN_CONFIG_FILE}"
        python3 -c "import json; print(json.dumps({'mcpServers': json.loads('''${SERVERS_JSON}''')}, indent=2))"
    else
        mkdir -p "${PLUGIN_DIR}"
        merge_mcp_config "${PLUGIN_CONFIG_FILE}" "${SERVERS_JSON}"
        log_success "Configured workspace plugin: ${PLUGIN_CONFIG_FILE}"
    fi
fi

# 2. Global Antigravity Configuration
if [[ "${MODE}" == "both" || "${MODE}" == "global" ]]; then
    if ${DRY_RUN}; then
        log_info "[DRY-RUN] Target Global Config: ${GLOBAL_CONFIG_FILE}"
        log_info "[DRY-RUN] Would merge servers into ${GLOBAL_CONFIG_FILE}"
    else
        mkdir -p "${GLOBAL_CONFIG_DIR}"
        merge_mcp_config "${GLOBAL_CONFIG_FILE}" "${SERVERS_JSON}"
        log_success "Merged into global config: ${GLOBAL_CONFIG_FILE}"
    fi
fi

# ------------------------------------------------------------------------------
# 6. Final Summary
# ------------------------------------------------------------------------------
log_header "Setup Summary"

printf "The following MCP servers have been configured for Open Anime Tracker:\n\n"
printf "  ${BOLD}%-22s${NC} PostgreSQL database queries and migration inspections\n" "postgres"
printf "  ${BOLD}%-22s${NC} Session store and cache inspection\n" "redis"
printf "  ${BOLD}%-22s${NC} React frontend UI testing and DOM inspection\n" "playwright"
printf "  ${BOLD}%-22s${NC} Backend REST and external API requests\n" "fetch"
printf "  ${BOLD}%-22s${NC} Git repository history and status\n" "git"
printf "  ${BOLD}%-22s${NC} Architecture reasoning and multi-step workflows\n\n" "sequential-thinking"

printf "${GREEN}✔ Setup complete!${NC}\n"
printf "Restart or reload Antigravity to activate the new tools.\n"
printf "You can view active servers in Antigravity under:\n"
printf "  ${BOLD}Additional Options (...) > MCP Servers${NC}\n\n"
