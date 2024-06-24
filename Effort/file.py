from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
# Set a secret key for your Flask app
app.config['SECRET_KEY'] = 'pailab'
username1={"bilal":"pass"}
sum=0

class MyForm(FlaskForm):
    name = StringField('Name')
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/forms', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data

        if username=="bilal" and password=="pass":
            return function()

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)