from flask import Blueprint, request, session, render_template, jsonify, send_file, jsonify
import uuid
import config 
from services.utils import safe_int
from services.search_script import build_query
import gridfs
import zipfile
import json
from services.search_script import get_file_with_one_taxonomy
import pandas
from bson import json_util, ObjectId
from pandas import json_normalize
import os
import threading
import tempfile
import io

#dividere anche questo per un migliore refactoring (portare su services)

phylorna_bp = Blueprint("phylorna",__name__)
@phylorna_bp.route('/search/')
def search():
    return render_template('search.html')

@phylorna_bp.route('/search/res/', methods=['POST']) #risponde solo ai post
def search_result():
    format = request.args.get('format')
    if "session_id" not in session:
        session['session_id'] = str(uuid.uuid4())

    # Read params
    params = {
        "org_name": request.form.get('Organism name', ''),
        "length_from": safe_int(request.form.get('Length_from')),
        "length_to": safe_int(request.form.get('Length_to')),
        "acc_num": request.form.get('Accession number', ''),
        "benchmark_id": request.form.get('Benchmark ID', ''),
        "weak_from": safe_int(request.form.get('Number_of_weak_bonds_from')),
        "weak_to": safe_int(request.form.get('Number_of_weak_bonds_to')),
        "is_pseudo": request.form.get('Is Pseudoknotted', ''),
        "rna_type": request.form.get('Rna Type', ''),
        "genus": safe_int(request.form.get('Genus')),
        "taxonomy": request.form.get('Taxonomy', ''),
        "core": request.form.get('Core', ''),
        "core_plus": request.form.get('Core plus', ''),
        "shape": request.form.get('Shape', ''),
        "rank": request.form.get('Taxonomy_rank', ''),
        "taxon": request.form.get('rank_value', ''),
        "db_name": request.form.get('Database', ''),
        "is_validated": request.form.get('Is Validated', ''),
        "num_decoup_from": request.form.get('num_decoup_from', ''),
        "num_decoup_to": request.form.get('num_decoup_to', ''),
    }
    print (params)
    query = build_query(params)
    skip = request.form.get("offset", 0, type=int)
    limit = request.form.get("limit", 10, type=int)
    collection = config.DB['rna_sequences']
    result = collection.find(query).skip(skip).limit(limit)
    print (result)
    if format == "json":

        results = [
            {**doc, "_id": str(doc["_id"])}
            for doc in result
        ]

        return jsonify({
            "total": collection.count_documents(query),
            "results": results
        })   
    else: 
        return render_template("search_results.html", result_list=result, search_criteria=request.form.to_dict())

@phylorna_bp.route('/search/names/', methods=['POST']) #risponde solo ai post
def search_names():
    if "session_id" not in session:
        session['session_id'] = str(uuid.uuid4())

    # Read params
    params = {
        "org_name": request.form.get('Organism name', ''),
        "length_from": safe_int(request.form.get('Length_from')),
        "length_to": safe_int(request.form.get('Length_to')),
        "acc_num": request.form.get('Accession number', ''),
        "benchmark_id": request.form.get('Benchmark ID', ''),
        "weak_from": safe_int(request.form.get('Number_of_weak_bonds_from')),
        "weak_to": safe_int(request.form.get('Number_of_weak_bonds_to')),
        "is_pseudo": request.form.get('Is Pseudoknotted', ''),
        "rna_type": request.form.get('Rna Type', ''),
        "genus": safe_int(request.form.get('Genus')),
        "taxonomy": request.form.get('Taxonomy', ''),
        "core": request.form.get('Core', ''),
        "core_plus": request.form.get('Core plus', ''),
        "shape": request.form.get('Shape', ''),
        "rank": request.form.get('Taxonomy_rank', ''),
        "taxon": request.form.get('rank_value', ''),
        "db_name": request.form.get('Database', ''),
        "is_validated": request.form.get('Is Validated', ''),
        "num_decoup_from": request.form.get('num_decoup_from', ''),
        "num_decoup_to": request.form.get('num_decoup_to', ''),
    }
    print (params)
    query = build_query(params)
    collection = config.DB['rna_sequences']
    result = [
    doc["reference_id"]
    for doc in collection.find(
        query,
        {"_id": 0, "reference_id": 1}
    )
]
    print (result)

    return jsonify({
            "total": collection.count_documents(query),
            "results": result
        })   
   
@phylorna_bp.route('/search/res/single/', methods=['GET'])
def getSingleResult():
    collection = config.DB['rna_sequences']
    singleId = request.args.get('id')

    result = collection.find_one({"_id": ObjectId(singleId)})

    if not result:
        return jsonify({"error": "not found"}), 404

    result["_id"] = str(result["_id"])

    return jsonify(result)

@phylorna_bp.route('/download_files_csv', methods=['POST'])
def download():
    if request.method == 'POST':
        data = request.json
        filenames = data.get('filenames', [])
        taxonomy = data.get('taxonomy', "").split(",")[0]

        if not filenames:
            return jsonify({"error": "No files selected"}), 400

        config.DB.get_collection(get_session_id()).delete_many({})
        for filename in filenames:
            if filename:
                get_file_with_one_taxonomy(filename, taxonomy, get_session_id())

        mongo_docs = config.DB.get_collection(get_session_id()).find({}, {'_id': False})
        sanitized_mongo_docs = json.loads(json_util.dumps(mongo_docs))
        normalized_mongo_docs = json_normalize(sanitized_mongo_docs)
        final_mongo_docs = pandas.DataFrame(normalized_mongo_docs)
        final_mongo_docs = final_mongo_docs.dropna(how="all")

        temp_file = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
        final_mongo_docs.to_csv(temp_file, sep=',', index=False, lineterminator='\n')
        return send_file(temp_file, as_attachment=True, download_name="selected_files.csv")

@phylorna_bp.route('/download_files', methods=['POST'])
def download_zip_files():
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()
        filenames = data.get('filenames', [])
        formats = data.get('formats', '').split(",")

        # 1. Inizializziamo GridFS FUORI dai cicli per migliorare le prestazioni
        fs = gridfs.GridFS(config.DB)
        
        memory_file = io.BytesIO() 
        files_added_count = 0  # Contatore per verificare se abbiamo aggiunto qualcosa

        with zipfile.ZipFile(memory_file, 'w') as zf:
            for f in formats:
                f_clean = f.strip()
                if not f_clean:
                    continue
                
                #  aggiunge il punto se manca (es. "csv" -> ".csv")
          
                if not f_clean.startswith('.'):
                    f_clean = '.' + f_clean

                for filename in filenames:
                    filename_clean = filename.strip()
                    if not filename_clean:
                        continue
                    
                    #Componiamo il nome del file pulito da spazi
                    file_to_find = filename_clean + f_clean
                    
                    try:
                        #Utilizziamo l'API nativa di GridFS (più sicura ed efficiente) -- Ma mi servono i file per gridFS-- Chiedere
                        grid_file = fs.get_last_version(filename=file_to_find)
                        output_data = grid_file.read()
                        
                        #Scriviamo nel file ZIP
                        zf.writestr(file_to_find, output_data)
                        files_added_count += 1
                        
                    except gridfs.errors.NoFile:
                        print(f"File non trovato in GridFS: {file_to_find}")
                        continue
                    except Exception as e:
                        print(f"Errore nel recupero del file '{file_to_find}': {e}")
                        continue

        #Se non è stato trovato alcun file, evitiamo di inviare uno ZIP vuoto e corrotto
        if files_added_count == 0:
            return jsonify({'error': 'Nessun file corrispondente trovato nel database. Archivio vuoto.'}), 404

        memory_file.seek(0)
        return send_file(
            memory_file, 
            as_attachment=True, 
            download_name='zipFile.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        print("Errore generale:", e)
        return jsonify({'error': 'Errore interno: ' + str(e)}), 500


def get_session_id():
    if "session_id" in session:
        return str(session["session_id"])
    else:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        return session_id