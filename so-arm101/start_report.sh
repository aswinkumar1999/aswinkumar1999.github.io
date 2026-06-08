#!/usr/bin/env bash
# Starts a local HTTP server in this folder and opens final_report.html.

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PORT=""
for p in 8765 8766 8767 8800 9000; do
  if ! (ss -tln 2>/dev/null || netstat -tln 2>/dev/null) | grep -q "[:.]$p[[:space:]]"; then
    PORT=$p
    break
  fi
done

if [ -z "$PORT" ]; then
  echo "Couldn't find a free port. Edit start_report.sh and add another." >&2
  exit 1
fi

URL="http://localhost:$PORT/final_report.html"
LOG="/tmp/final_report_server_$PORT.log"

echo "================================================================"
echo "  Final report website launcher"
echo "  Folder: $DIR"
echo "  URL:    $URL"
echo "  Log:    $LOG"
echo "================================================================"
echo

python3 -m http.server "$PORT" >"$LOG" 2>&1 &
SERVER_PID=$!

cleanup() {
  echo
  echo "Stopping server (PID $SERVER_PID)..."
  kill "$SERVER_PID" 2>/dev/null || true
  exit 0
}
trap cleanup INT TERM

for i in $(seq 1 20); do
  if curl -sI "$URL" 2>/dev/null | head -1 | grep -q "200 OK"; then
    break
  fi
  sleep 0.15
done

echo "Server PID: $SERVER_PID"
echo "Opening browser..."

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then
  open "$URL" >/dev/null 2>&1 &
elif command -v start >/dev/null 2>&1; then
  start "$URL" >/dev/null 2>&1 &
else
  echo "  (Could not auto-open a browser - paste this URL yourself.)"
fi

echo
echo "Press Ctrl+C in this terminal to stop the server when done."
echo

wait "$SERVER_PID"
