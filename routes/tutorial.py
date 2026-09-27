from flask import Blueprint, render_template
import config 

tutorial_bp = Blueprint("tutorial",__name__)

@tutorial_bp.route('/search')
def s_tutorial():
    #before_request('/tutorial/search')
    return render_template('s_tutorial.html')

@tutorial_bp.route('/download')
def d_tutorial():
   # before_request('/tutorial/download')
    return render_template('d_tutorial.html')