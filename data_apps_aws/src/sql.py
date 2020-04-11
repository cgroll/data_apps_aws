import sqlalchemy
import pandas as pd

from data_apps_aws.src.passwords import get_db_password, get_db_url, get_db_user

def get_engine_str(db_environment):
    # Retrieve username, password, url
    this_db_pwd = get_db_password(db_environment)
    this_db_url = get_db_url(db_environment)
    this_db_user = get_db_user(db_environment)

    # SQLalchemy way
    engine = 'mysql+pymysql://' + this_db_user + ':' + this_db_pwd + '@' + this_db_url

    return engine


def get_db_engine(db_environment):
    """
    Create MySQL engine
    Args:
        db_environment: Name of the MySQL User/Environment
            Options: 'bi_read_only', 'ai_read_only', 'ai_dev', 'ai_prod'

    Returns:
        DB engine
    """
    engine = get_engine_str(db_environment)
    db_engine = sqlalchemy.create_engine(engine)

    return db_engine


def get_db_data(query, db_con):

    return pd.read_sql(sql=query, con=db_con)


def delete_all_table_rows(table_name, db_con):
    query = f"""
    DELETE FROM {table_name}
    """

    db_con.execute(query)


def upload_df_to_table(this_df, table_name, db_con, index=False, if_exists='append'):

    this_df.to_sql(table_name, db_con, index=index, if_exists=if_exists)


def overwrite_db_table_from_df(this_df, table_name, db_con, index=False):

    delete_all_table_rows(table_name, db_con)
    upload_df_to_table(this_df, table_name, db_con, index=index, if_exists='append')

