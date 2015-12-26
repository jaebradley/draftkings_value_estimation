import flask_restless as restless
from flask import request
from datetime import datetime

from persistence.nba.data.database_connector import db_session
from persistence.nba.model import app, Player, Team, BoxScore
from analysis.nba.lib.basic_average_stddev import return_average_and_stddev


# add year month day params and construct date object
@app.route('/api/average_and_stddev/', methods=["GET"])
def average_and_stddev():
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    return return_average_and_stddev(datetime(year, month, day)).to_json()


def create_api():
    manager = restless.APIManager(app, session=db_session)
    manager.create_api(Player, methods=["GET"])
    manager.create_api(Team, methods=["GET"])
    manager.create_api(BoxScore, methods=["GET"])

create_api()
app.run(debug=True)