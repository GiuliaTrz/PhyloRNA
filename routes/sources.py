from flask import Blueprint, render_template
import config 

sources_bp = Blueprint("sources",__name__)
@sources_bp.route("/")
def sources():
   # before_request('/sources/')
    num_docs = config.COLLECTION.count_documents({})
    return render_template('sources.html', num_docs=num_docs)
