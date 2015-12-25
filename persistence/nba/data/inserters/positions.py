from persistence.nba.data.utils.functions import get_or_create
from persistence.nba.model import Position


class PositionInserter:
    def __init__(self):
        self.positions = [
            {
                'name': 'Point Guard',
                'abbreviation': 'PG'
            },
            {
                'name': 'Shooting Guard',
                'abbreviation': 'SG'
            },
            {
                'name': 'Small Forward',
                'abbreviation': 'SF'
            },
            {
                'name': 'Power Forward',
                'abbreviation': 'PF'
            },
            {
                'name': 'Center',
                'abbreviation': 'C'
            }
        ]

    def insert_positions(self, session):
        for position in self.positions:
            get_or_create(session, Position, name=position['name'], abbreviation=position['abbreviation'])