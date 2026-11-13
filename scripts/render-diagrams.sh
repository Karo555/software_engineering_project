#!/usr/bin/env bash
# Render every PlantUML file in docs/diagrams to SVG and PNG next to its source.
# Needs Docker; no local Java or PlantUML install required.
#
#   scripts/render-diagrams.sh               # all diagrams
#   scripts/render-diagrams.sh use-case.puml # one diagram
set -euo pipefail

cd "$(dirname "$0")/../docs/diagrams"

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  files=(*.puml)
fi

for format in svg png; do
  docker run --rm -v "$PWD":/data -w /data plantuml/plantuml:1.2024.8 -t"$format" "${files[@]}"
done

echo "Rendered: ${files[*]}"
