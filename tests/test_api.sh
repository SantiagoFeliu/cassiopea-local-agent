#!/usr/bin/env bash
curl -s -X POST "http://localhost:8002/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"sistema operativo"}'
echo
