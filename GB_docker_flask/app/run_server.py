# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/app/app/models/logreg_pipeline.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":

		race_ethnicity, parental_level_of_education, lunch,test_preparation_course, math_score, reading_score, writing_score = "", "", "", "", "", "", ""
		request_json = flask.request.get_json()
		if request_json["race_ethnicity"]:
			race_ethnicity = request_json['race_ethnicity']
		if request_json["parental_level_of_education"]:
			parental_level_of_education = request_json['parental_level_of_education']
		if request_json["lunch"]:
			lunch = request_json['lunch']
		if request_json["test_preparation_course"]:
			test_preparation_course = request_json['test_preparation_course']
		if request_json["math_score"]:
			math_score = request_json['math_score']
		if request_json["reading_score"]:
			reading_score = request_json['reading_score']

		if request_json["writing_score"]:
			writing_score = request_json['writing_score']
		# 'race_ethnicity', 'parental_level_of_education', 'lunch','test_preparation_course', 'math_score', 'reading_score', 'writing_score'
		logger.info(f'{dt} Data: race_ethnicity={race_ethnicity}, parental_level_of_education={parental_level_of_education}, lunch={lunch}, test_preparation_course={test_preparation_course}, math_score={math_score}, reading_score={reading_score}, writing_score={writing_score}')
		try:
			preds = model.predict_proba(pd.DataFrame({"race_ethnicity": [race_ethnicity],
												  "parental_level_of_education": [parental_level_of_education],
												  "lunch": [lunch],
													  "test_preparation_course": [test_preparation_course],
													   "math_score": [math_score],
														"reading_score": [reading_score],
														 "writing_score": [writing_score]}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)
