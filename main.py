from flask import Flask,render_template,redirect,url_for,request,flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor,CKEditorField
from wtforms import StringField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import data_required
from flask_sqlalchemy import SQLAlchemy
import random,os

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'd;lf;ldgkflg;dlf;'
ckeditor = CKEditor(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get("DATABASE_URL1",  "sqlite:///addbase.db")

# -----------------------------------------------set up form here----------------
class addform(FlaskForm):
    term = StringField(label='Term',validators=[data_required()])
    meaning = StringField(label='Meaning',validators=[data_required()])
    sentence = CKEditorField(label='Sentence',validators=[data_required()])
    submit = SubmitField('Add')
# ----------------------------------------------set up database here------------
class adddata(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    term = db.Column(db.String(1000),nullable = False)
    meaning = db.Column(db.String(1000),nullable = False)
    sentence = db.Column(db.String(1000),nullable = False)

db.create_all()
# --------------------------------------------------start here------------------
previous_word = None
@app.route('/',methods=['POST','GET'])
def home():
    global previous_word
    alldata = db.session.query(adddata).all()
    random_word = random.choice(alldata)

    if request.method == 'POST':

        if request.form.get('no') == '1':
            if previous_word:

                term = previous_word.term
                flash(f'{term} ')

    previous_word = random_word
    return render_template('index.html', data=alldata, random=random_word)

@app.route('/add',methods=['POST','GET'])
def add():

    form = addform()
    if form.validate_on_submit():

        newdata = adddata(term=form.term.data,meaning=form.meaning.data,sentence=form.sentence.data)
        db.session.add(newdata)
        db.session.commit()

        return redirect(url_for('home'))
    # <!--                {{ form.name(size=50) }}-->
    return render_template('add.html',form=form)

@app.route('/edit',methods=['POST','GET'])
def edit():

    wordid = request.args.get('id')
    word = adddata.query.get(wordid)
    form = addform(term=word.term,meaning=word.meaning,sentence=word.sentence)

    if form.validate_on_submit():

        # remember add data
        word.term = form.term.data
        word.meaning = form.meaning.data
        word.sentence = form.sentence.data
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html',form=form)

@app.route('/delete')
def delete():

    word = adddata.query.get(request.args.get('id'))
    db.session.delete(word)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)