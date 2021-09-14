from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import json
import re

with open("dics/seesdic.json","r") as fp:
    seesdic = json.load(fp)

with open("dics/pagesdic.json","r") as fp:
    pagesdic = json.load(fp)

with open("dics/tokendic.json","r") as fp:
    tokendic = json.load(fp)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

basic_dic = {"a":"Hello","b":"world"}

class Entries(db.Model):
    __tablename__ = 'entries_main'
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String)
    #variants = db.Column(db.String)
    #pages = db.Column(db.String)


@app.route('/')
def index():
    entries = Entries.query.all()
    #returns all records in the table.
    return render_template('entry_list.html', entries=entries)

@app.route('/render/<page_number_current>')
def render_page(page_number_current):
    twoargs = re.split(',', page_number_current, 1)
    page_number = twoargs[0]
    entrynow = twoargs[1]
    #entrynow = entrynow + ')'
    #curr_entry = re.split(',', page_number_current, 1)[1]
    #print(curr_entry)
    return send_from_directory('static/page_contents', 'plaintext' + page_number + '.html')

@app.route('/indiv_entry/<int:id>')
def indiv_entry(id):
    current_entry = Entries.query.get_or_404(id)
    #current_id = current_entry.id
    #entry_title = current_entry.entry
    #variants = current_entry.variants
    #pages = current_entry.pages
    return render_template('entry_page.html', current_entry=current_entry, seesdic=seesdic, tokendic=tokendic, pagesdic=pagesdic)


if __name__ == "__main__":
    app.run(debug=True)