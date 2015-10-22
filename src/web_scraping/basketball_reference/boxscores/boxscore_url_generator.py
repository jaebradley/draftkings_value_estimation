class BoxscoreUrlGenerator:
    def __init__(self):
        pass

    def generate_url(self, day, month, year):
        box_score_url_arguments = {
            'month': month,
            'day': day,
            'year': year
        }
        box_score_url = 'http://www.basketball-reference.com/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(**box_score_url_arguments)
        return box_score_url