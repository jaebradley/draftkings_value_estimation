import sqlalchemy
from data_model.nba.data_manipulation.adding_data_to_base_tables.add_data_to_draftkings_salary_table import add_data_to_draftkings_salary_table

try:
    add_data_to_draftkings_salary_table()
except sqlalchemy.exc.IntegrityError as error_message:
    pass




