#!/usr/bin/env bash
# FreeMium JayRain audio node launcher (macOS / Linux)
# First run: asks for a node password and writes it into application.yml
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v java >/dev/null 2>&1; then
  echo ""
  echo " Java 17 or newer is required but was not found."
  echo " Download it here: https://adoptium.net"
  echo " Install it, then run this script again."
  echo ""
  exit 1
fi

if grep -q "__NODE_PASSWORD__" application.yml 2>/dev/null; then
  echo ""
  echo " First-time setup: choose a password for your node."
  echo " You'll paste this same password into the FreeMium JayRain dashboard."
  echo ""
  read -rsp "Node password (min 4 characters): " NJPW
  echo ""
  if [ "${#NJPW}" -lt 4 ]; then
    echo "Use at least 4 characters. Run the script again."
    exit 1
  fi
  ESCAPED=$(printf '%s' "$NJPW" | sed -e 's/[\/&]/\\&/g')
  sed -i "s/__NODE_PASSWORD__/${ESCAPED}/" application.yml
  echo "Password saved."
fi

echo ""
echo " Starting your FreeMium JayRain audio node..."
echo " Keep this terminal open while you want music. Ctrl+C to stop."
echo ""
exec java -jar Lavalink.jar
