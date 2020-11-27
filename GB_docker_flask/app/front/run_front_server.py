import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField, FloatField
from wtforms.validators import DataRequired





import urllib.request
import json

class ClientDataForm(FlaskForm):
    #race_ethnicity = StringField('race_ethnicity', validators=[DataRequired()])
    race_ethnicity = SelectField('race_ethnicity', choices=[  
        ('group C', 'group C'),
        ('group D', 'group D'),
        ('group B', 'group B'),
        ('group E', 'group E'),
        ('group A', 'group A'),
    ])
    parental_level_of_education = SelectField('parental_level_of_education', choices=[
        ('some college', 'some college'),
        ("associate's degree", "associate's degree"),
        ('high school', 'high school'),
        ('some high school', 'some high school'),
        ("bachelor's degree", "bachelor's degree"),
        ("master's degree", "master's degree"),
    ])
    lunch = SelectField('lunch', choices=[
        ('standard', 'standard'),
        ('free/reduced', 'free/reduced'),
    ])
    test_preparation_course = SelectField('test_preparation_course', choices=[
        ('none', 'none'),
        ('completed', 'completed'),
    ])
    math_score = FloatField('math_score', validators=[DataRequired()])
    reading_score = FloatField('reading_score', validators=[DataRequired()])
    writing_score = FloatField('writing_score', validators=[DataRequired()])
    



app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(race_ethnicity, parental_level_of_education, lunch, test_preparation_course, math_score, reading_score, writing_score):
    body = {'race_ethnicity': race_ethnicity,
            'parental_level_of_education': parental_level_of_education,
            'lunch': lunch,
            'test_preparation_course': test_preparation_course,
            'math_score': math_score,
            'reading_score': reading_score,
            'writing_score': writing_score}

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    # 'race_ethnicity', 'parental_level_of_education', 'lunch',
    #       'test_preparation_course', 'math_score', 'reading_score',
    #       'writing_score'
    if request.method == 'POST':
        data['race_ethnicity'] = request.form.get('race_ethnicity')
        data['parental_level_of_education'] = request.form.get('parental_level_of_education')
        data['lunch'] = request.form.get('lunch')
        data['test_preparation_course'] = request.form.get('test_preparation_course')
        data['math_score'] = request.form.get('math_score')
        data['reading_score'] = request.form.get('reading_score')
        data['writing_score'] = request.form.get('writing_score')


        try:
            response = str(get_prediction(data['race_ethnicity'],
                                      data['parental_level_of_education'],
                                      data['lunch'],
                                          data['test_preparation_course'],
                                          data['math_score'],
                                          data['reading_score'],
                                          data['writing_score']
                                          ))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
