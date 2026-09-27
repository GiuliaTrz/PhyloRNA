import config 
from flask import Blueprint, render_template

home_bp = Blueprint("home",__name__)

@home_bp.route('/')

def home():
    #before_request('/')
    num_RCSB = config.COLLECTION.count_documents({'database': 'PDB'})
    num_CRW = config.COLLECTION.count_documents({'database': 'CRW'})
    num_CRW2 = config.COLLECTION.count_documents({'database': 'CRW2'})
    num_tmRNAdb = config.COLLECTION.count_documents({'database': 'tmRNAdb'})
    num_SRPdb = config.COLLECTION.count_documents({'database': 'SRPdb'})
    num_5S = config.COLLECTION.count_documents({'rna_type': '5S'})
    num_16S = config.COLLECTION.count_documents({'rna_type': '16S'})
    num_23S = config.COLLECTION.count_documents({'rna_type': '23S'})
    num_GI1 = config.COLLECTION.count_documents({'rna_type': 'Group I Introns'})
    num_GI2 = config.COLLECTION.count_documents({'rna_type': 'Group II Introns'})
    num_tRNA = config.COLLECTION.count_documents({'rna_type': 'tRNA'})
    num_tRNA_seq = config.COLLECTION.count_documents({'rna_type': 'tRNA Seq'})
    num_tmRNA = config.COLLECTION.count_documents({'rna_type': 'tmRNA'})
    num_SRP = config.COLLECTION.count_documents({'rna_type': 'SRP'})
    return render_template('home.html',
                           num_RCSB=num_RCSB, num_CRW=num_CRW, num_CRW2=num_CRW2,
                           num_tmRNAdb=num_tmRNAdb, num_SRPdb=num_SRPdb,
                           num_5S=num_5S, num_16S=num_16S, num_23S=num_23S,
                           num_GI1=num_GI1, num_GI2=num_GI2, num_tRNA=num_tRNA,
                           num_tRNA_seq=num_tRNA_seq, num_tmRNA=num_tmRNA, num_SRP=num_SRP)