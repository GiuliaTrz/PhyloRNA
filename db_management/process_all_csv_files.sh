#!/bin/bash

# Controlla che venga passato un argomento
if [ $# -ne 1 ]; then
  echo "Usage: $0 /path/to/directory"
  exit 1
fi

# Directory specificata come argomento
directory="$1"

# Verifica che la directory esista
if [ ! -d "$directory" ]; then
  echo "Error: Directory $directory does not exist."
  exit 1
fi

# Itera su tutti i file nella directory
for file in "$directory"/*; do
  # Salta i file nascosti
  if [ -f "$file" ] && [[ "$(basename "$file")" != .* ]]; then
    echo "Processing file: $file"
    python command_line_create_json.py "$file"
    if [ $? -ne 0 ]; then
      echo "Error processing file: $file"
    fi
  fi
done

echo "Processing complete."