import re
import config
from flask import request 

def to_bool(value):
    if isinstance(value, str):
        return value.lower() == "yes"
    return value


def build_query(params):
    query = {}

    # Organism name (first two words, startswith, case-insensitive)
    if params.get("org_name"):
        words = params["org_name"].split()
        first_two = " ".join(words[:2])
        query["organism_name"] = {
            "$regex": f'^{re.escape(first_two)}',
            "$options": "i"
        }

    # Accession number
    if params.get("acc_num"):
        query["accession_number"] = params["acc_num"]

    # Length
    length_filter = {}
    if params.get("length_from", -1) != -1:
        length_filter["$gte"] = params["length_from"]
    if params.get("length_to", -1) != -1:
        length_filter["$lte"] = params["length_to"]
    if length_filter:
        query["length"] = length_filter

    # Number of unpaired bases
    unpaired_from = params.get("num_decoup_from")
    unpaired_to = params.get("num_decoup_to")

    unpaired_filter = {}

    def valid(x):
        return x not in (None, "", "-1", -1)

    if valid(unpaired_from):
        unpaired_filter["$gte"] = int(unpaired_from)

    if valid(unpaired_to):
        unpaired_filter["$lte"] = int(unpaired_to)

    if unpaired_filter:
        query["num_unpaired_bases"] = unpaired_filter

    # Weak bonds
    weak_filter = {}
    if params.get("weak_from", -1) != -1:
        weak_filter["$gte"] = params["weak_from"]
    if params.get("weak_to", -1) != -1:
        weak_filter["$lte"] = params["weak_to"]
    if weak_filter:
        query["num_base_pairs"] = weak_filter

    # Boolean
    if params.get("is_pseudo") != '':
        query["is_pseudoknotted"] = to_bool(params["is_pseudo"])

    if params.get("is_validated") != '':
        query["experimentally_derived"] = to_bool(params["is_validated"])

    # Simple fields
    for field, key in [
        ("rna_type", "rna_type"),
        ("genus", "genus"),
        ("core", "core"),
        ("core_plus", "core_plus"),
        ("shape", "shape"),
        ("benchmark_id", "reference_id"),
        ("db_name", "database"),
    ]:
        if params.get(field) not in ('', -1, None):
            query[key] = params[field]

    # Taxonomy
    taxonomy = params.get("taxonomy")
    rank = params.get("rank")
    value = params.get("taxon")
   
    if taxonomy and rank and value:
        query["taxonomy"] = {
            "$elemMatch": {
                "source": taxonomy,
                rank: {
                "$regex": f'^{re.escape(value)}',
                "$options": "i"
                } 
            }
        }
    elif taxonomy:
        query["taxonomy"] = {
            "$elemMatch": {
                "source": taxonomy,
                "is_classified": True
            }
        }

    return query

def get_file_with_one_taxonomy(filename, taxonomy, user_collection):
    collection = config.DB.get_collection("rna_sequences")
    string_taxonomy = 'Taxonomy.' + taxonomy + '.Classified'
    collection.aggregate([
        {
            '$match': {
                'Benchmark ID': filename
            }
        }, {
            '$unwind': {
                'path': '$Taxonomy',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$match': {
                '$or': [
                    {
                        string_taxonomy: 'No'
                    }, {
                        string_taxonomy: 'Yes'
                    }
                ]
            },

        }, {
            '$merge': {
                'into': user_collection,
                'on': '_id',
                'whenMatched': 'replace',
                'whenNotMatched': 'insert'
            }
        }
    ])
    return config.DB.get_collection(user_collection)
