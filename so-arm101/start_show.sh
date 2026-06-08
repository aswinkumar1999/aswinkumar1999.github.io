#!/usr/bin/env bash
# Starts a local HTTP server in this folder and opens deck.html in the browser.
# Run with:  ./start_show.sh
# Stop with: Ctrl+C   (the server is killed cleanly).
#
# If port 8765 is busy, falls through to 8766, 8767, 8800, 9000.

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Pick first free port from the list
PORT=""
for p in 8765 8766 8767 8800 9000; do
  if ! (ss -tln 2>/dev/null || netstat -tln 2>/dev/null) | grep -q "[:.]$p[[:space:]]"; then
    PORT=$p; break
  fi
done
if [ -z "$PORT" ]; then
  echo "Couldn't find a free port. Edit start_show.sh and add another." >&2
  exit 1
fi

URL="http://localhost:$PORT/deck.html"
LOG="/tmp/eval_gallery_server_$PORT.log"

echo "================================================================"
echo "  Eval Gallery launcher"
echo "  Folder: $DIR"
echo "  URL:    $URL"
echo "  Log:    $LOG"
echo "================================================================"
echo

# Start server in background
python3 -m http.server "$PORT" >"$LOG" 2>&1 &
SERVER_PID=$!

# Clean up on exit
cleanup() {
  echo
  echo "Stopping server (PID $SERVER_PID)…"
  kill "$SERVER_PID" 2>/dev/null || true
  exit 0
}
trap cleanup INT TERM

# Wait for server to come up (max ~3s)
for i in $(seq 1 20); do
  if curl -sI "$URL" 2>/dev/null | head -1 | grep -q "200 OK"; then break; fi
  sleep 0.15
done

echo "Server PID: $SERVER_PID"
echo "Opening browser…"

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then            # macOS
  open "$URL" >/dev/null 2>&1 &
elif command -v start >/dev/null 2>&1; then           # Git Bash on Windows
  start "$URL" >/dev/null 2>&1 &
else
  echo "  (Could not auto-open a browser — paste this URL yourself.)"
fi

echo
echo "Press F11 for fullscreen, →/← to navigate slides."
echo "Press Ctrl+C in this terminal to stop the server when done."
echo

# Block here so the user can Ctrl+C
wait "$SERVER_PID"
