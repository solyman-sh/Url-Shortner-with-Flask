
from flask import Flask, render_template,url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from shorten import createid
import re

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///urlshorten.db'  

db = SQLAlchemy(app)



class LINKS(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    link= db.Column(db.String(1000))
    linkid= db.Column(db.String(6),unique=True)



def addnewlink(url):
    id = createid()
    if str(LINKS.query.filter_by(linkid=id).first()) !="None":
        while str(LINKS.query.filter_by(linkid = id).first()) != "None":
            id= createid()

    newlink= LINKS(link=url, linkid=id)
    db.session.add(newlink)
    db.session.commit()
    return id


@app.route('/')
def home():
    return render_template("index.html", message="Shorten The link")


@app.route('/shorten', methods=["POST"])
def shorten():
    link = request.form['link']
    if re.search('https://\w+.\w+.*', link)==None:
        return render_template("index.html", message="NOt a valid link")

    linkid = addnewlink(link)
    
    return render_template("index.html", message=linkid)



@app.route("/<linkid>")
def red(linkid):
    link = LINKS.query.filter_by(linkid=linkid).first()
    if link is not None:
        return redirect(link.link)
    else:
        return "Link not found"



if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)