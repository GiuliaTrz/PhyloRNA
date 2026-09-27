import argparse
import os
import create_json

def main():
    # Imposta il parser per gli argomenti della riga di comando
    parser = argparse.ArgumentParser(
        description="Script to process a single file and create a JSON file."
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the file to be processed."
    )

    # Verifica la presenza di argomenti
    args = parser.parse_args()
    file_path = args.file_path

    # Controlla se il file esiste
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return

    # Specifica il percorso di output
    output_path = "files/json_file_18-01-2025"
    os.makedirs(output_path, exist_ok=True)  # Assicura che la directory esista
    output_file_name = os.path.basename(file_path) + ".json"
    output_file_path = os.path.join(output_path, output_file_name)

    # Processa il file e crea il file JSON
    try:
        with open(file_path, 'r') as input_file:
            with open(output_file_path, 'w') as output_file:
                create_json.create_file_json(input_file, output_file)
        print(f"JSON file created successfully at: {output_file_path}")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
