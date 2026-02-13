# Default (no SSL warnings, no verification)
python webshell_scanner.py -u https://example.com

# With SSL verification
python webshell_scanner.py -u https://example.com --verify-ssl

# Telegram version (no warnings)
python webshell_scanner_telegram.py \
  -u https://example.com -tb "TOKEN" -tc "CHAT_ID"

# Telegram + SSL verify
python webshell_scanner_telegram.py \
  -u https://example.com \
  -tb "TOKEN" -tc "CHAT_ID" \
  --verify-ssl

