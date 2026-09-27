from flask import Blueprint, request, render_template

contact_bp = Blueprint("contact",__name__)
@contact_bp.route("/")
def contatti():
   # before_request('/contact/')
    print("Sono sulla pagina dei contatti")
    return render_template('contact.html')