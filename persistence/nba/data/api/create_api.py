import flask_restless as restless

from persistence.nba.data.database_connector import db_session
from persistence.nba.model import app, Player, Team
from analysis.nba.lib.basic_average_stddev import return_average_and_stddev


# add year month day params and construct date object
@app.route('/api/average_and_stddev/')
def average_and_stddev(date):
    return return_average_and_stddev(date)


def create_api():
    manager = restless.APIManager(app, session=db_session)
    manager.create_api(Player, methods=["GET"])
    manager.create_api(Team, methods=["GET"])

create_api()
app.run(debug=True)