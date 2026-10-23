## 2026-10-23 - [CRITICAL] Fix hardcoded Telegram API token
**Vulnerability:** Hardcoded Telegram API keys found in testing and configuration scripts.
**Learning:** Hardcoded secrets in automation scripts can easily be leaked to version control or logs.
**Prevention:** Use environment variables (e.g. os.environ.get) or a secure secret manager for API keys.
