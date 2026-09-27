import datetime
import json
import os
import gridfs
import pymongo
from pymongo.errors import DuplicateKeyError

client = pymongo.MongoClient('localhost')
db = client['PhyloRNAdb']
collection = db['rna_sequences']

'''
It inserts json files into the collection in the database
'''

def insert_to_mongo(dir_path):
    print("Inizio del processo di inserimento dei file JSON in MongoDB...\n")
    try:
        # Loop sui file nella directory
        print(f"Leggendo la directory: {dir_path}")
        for file_to_read in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_to_read)

            if os.path.isfile(file_path):
                print(f"\nTrovato file: {file_to_read}. Avvio del processo...")
                try:
                    with open(file_path, 'r+') as file:
                        print(f"  Aperto il file: {file_path}")
                        try:
                            file_data = json.load(file)  # Caricamento dati JSON
                            print("  File JSON caricato con successo.")
                        except json.JSONDecodeError as e:
                            print(f"  Errore di decodifica JSON nel file {file_path}: {str(e)}")
                            continue  # Salta il file se ha un errore JSON

                        # Controlla se il file contiene una lista o un singolo documento
                        if isinstance(file_data, list):
                            print(f"  Il file contiene una lista con {len(file_data)} documenti.")
                            try:
                                collection.insert_many(file_data, ordered=False)  # `ordered=False` continua con i documenti validi
                                print(f"  Inseriti {len(file_data)} documenti nel database.")
                            except DuplicateKeyError as e:
                                print(f"  Errore: documenti duplicati nel file. Dettagli: {str(e)}")
                        else:
                            print("  Il file contiene un singolo documento.")
                            try:
                                collection.insert_one(file_data)
                                print("  Documento inserito con successo.")
                            except DuplicateKeyError as e:
                                print(f"  Errore: il documento nel file {file_path} esiste già in MongoDB. Dettagli: {str(e)}")

                except IOError as e:
                    print(f"Errore di lettura del file {file_path}: {str(e)}")
                    continue  # Continua con il prossimo file in caso di errore di I/O
    except Exception as e:
        print(f"Errore generale nell'inserimento dei dati in MongoDB: {str(e)}")

    print("\nI file JSON sono stati inseriti in MongoDB (se non ci sono stati errori).")

'''
Given a name of a field to add, adds the field to every document of the collection.
'''


def add_one_field_all_docs():
    field = input("Insert the field you want to add to the rna_sequences collection: ")
    collection.update_many({}, {'$set': {field: "--"}})
    print("The field has been successfully added to the collection.")


'''
Given an accession number of a document, it modifies a field of that document
'''


def update_one_field():
    acc_number = input("Insert the accession number of the rna sequence you want to modify: ")
    old_document = collection.find_one({"Accession number": acc_number})
    print(old_document)
    if old_document is None:
        print("Invalid Accession Number")
        update_one_field()
    field = input(("Insert the field you want to change: "))
    new_input = input("Insert the new value of the field: ")
    collection.find_one_and_update({"Accession number": acc_number}, {"$set": {field: new_input}})
    if new_input == old_document.get(field):
        print("Sorry, we couldn't update the value.")
    else:
        print("The value was changed successfully.")
        print(collection.find_one({"Accession number": acc_number}))


'''
Delete one document from a collection. To remove the document, you need to enter the accession number of the document 
'''


def delete_one():
    acc_number = input("Insert the accession number of the rna sequence you want to delete: ")
    old_document = collection.find_one({"Accession number": acc_number})
    print(old_document)
    if old_document is None:
        print("Invalid Accession Number")
        delete_one()
    print("Are you sure you want to delete this document? y/n (default: n) ")
    answer = input()
    if answer.upper() == "Y" or answer.upper() == "YES":
        collection.find_one_and_delete({"Accession number": acc_number})
        print("The document has been deleted. \n")
    else:
        print("Operation Aborted. \n")


'''
Delete all documents from a given collection
'''


def delete_all():
    col_name = input("Insert the name of the collection of the documents you want to delete: ")
    print("Are you sure you want to delete all documents of this collection? y/n (default: n) ")
    answer = input()
    if answer.upper() == "Y" or answer.upper() == "YES":
        db.get_collection(col_name).delete_many({})
        print("All documents have been deleted. \n")
    else:
        print("Operation Aborted. \n")


'''
It inserts additional files into the database (the files can have the extensions .ct, .bpseq, .fasta, .dbn).
'''

def insert_files():
    print("Inizio del processo di caricamento dei file in GridFS...\n")
    dir_path = input("Inserisci il percorso della directory contenente i file da inserire: ")
    print(f"Percorso della directory specificato: {dir_path}\n")
    
    fs = gridfs.GridFS(db)  # Assumendo che 'db' sia stato già definito correttamente

    def process_directory(directory):
        print(f"Esplorazione della directory: {directory}\n")
        for root, dirs, files in os.walk(directory):
            print(f"Entrando nella directory: {root}")
            for file_to_read in files:
                file_location = os.path.join(root, file_to_read)
                if os.path.isfile(file_location):
                    print(f"\nTrovato file: {file_to_read}. Percorso completo: {file_location}")
                    try:
                        with open(file_location, "rb") as file_data:
                            print(f"  Aperto il file: {file_to_read}")
                            data = file_data.read()
                            print(f"  Contenuto del file letto con successo. Dimensione: {len(data)} bytes.")

                            # Verifica se il file esiste già in GridFS
                            if fs.exists({"_id": file_to_read}):
                                print(f"  Il file '{file_to_read}' esiste già in GridFS. Inserimento saltato.")
                            else:
                                # Inserisci il file in GridFS
                                fs.put(data, filename=file_to_read, _id=file_to_read)
                                print(f"  File '{file_to_read}' inserito correttamente in GridFS.")
                    except DuplicateKeyError as e:
                        print(f"  Errore: il file '{file_to_read}' esiste già nel database. Dettagli: {str(e)}")
                    except Exception as e:
                        print(f"  Errore durante l'inserimento del file '{file_to_read}': {str(e)}")
            print(f"Tutti i file nella directory '{root}' sono stati processati.\n")

    # Chiamata alla funzione per processare la directory principale e le sotto-directory
    try:
        process_directory(dir_path)
        print("Tutti i file sono stati caricati in GridFS con successo.\n")
    except Exception as e:
        print(f"Errore generale durante il caricamento dei file: {str(e)}")
        
'''
Delete collections that have not been used within 10 days from their creation.
'''


def delete_unused_collection():
    print("Inizio del processo per eliminare collezioni inutilizzate...\n")
    
    time_format = '%Y-%m-%d'
    current_time = str(datetime.datetime.utcnow().date())
    current_time = datetime.datetime.strptime(current_time, time_format)
    print(f"Data corrente UTC: {current_time.strftime(time_format)}\n")

    lists_to_check = db.list_collection_names()
    print(f"Collezioni trovate nel database: {lists_to_check}\n")

    for l in lists_to_check:
        print(f"Controllo della collezione: {l}")
        if l not in ['fs.chunks', 'fs.files', 'rna_sequences']:
            print(f"  La collezione '{l}' non è una collezione protetta. Procedo con i controlli...")
            if db.get_collection(l).count_documents({}) == 0:
                print(f"  La collezione '{l}' è vuota. Verrà eliminata.")
                db.get_collection(l).drop()
                print(f"  Collezione '{l}' eliminata con successo.\n")
            else:
                l_time = db.get_collection(l).find_one().get('_id').generation_time.date()
                l_time = datetime.datetime.strptime(str(l_time), time_format)
                print(f"  La collezione '{l}' non è vuota. Data di generazione più vecchia: {l_time.strftime(time_format)}")

                ten_days_ago = (current_time - datetime.timedelta(days=10)).date()
                if ten_days_ago >= l_time.date():
                    print(f"  La collezione '{l}' non è stata aggiornata negli ultimi 10 giorni (limite: {ten_days_ago}). Verrà eliminata.")
                    db.get_collection(l).drop()
                    print(f"  Collezione '{l}' eliminata con successo.\n")
                else:
                    print(f"  La collezione '{l}' è recente e non sarà eliminata.\n")
        else:
            print(f"  La collezione '{l}' è protetta e non sarà eliminata.\n")

    print("Processo di eliminazione delle collezioni inutilizzate completato.\n")
