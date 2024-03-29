import sqlalchemy
import pandas as pd

from data_apps_aws.password_manager import get_service_credentials_dict

def get_engine_str(db_environment):
    
    credentials_dict = get_service_credentials_dict(db_environment)

    # Retrieve username, password, url
    this_db_pwd = credentials_dict['password']
    this_db_url = credentials_dict['url']
    this_db_user = credentials_dict['user']

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


def delete_table_rows_matching_single_eq_condition(table_name, db_con, col_cond, val_cond):

    query = f"""
        DELETE FROM {table_name}
        WHERE {col_cond} = "{val_cond}"
        """

    db_con.execute(query)


def delete_table_rows_date_greater_than(table_name, db_con, date_col, val_cond):

    query = f"""
        DELETE FROM {table_name}
        WHERE {date_col} >= "{val_cond}"
        """

    db_con.execute(query)


def upload_df_to_table(this_df, table_name, db_con, index=False, if_exists='append'):

    this_df.to_sql(table_name, db_con, index=index, if_exists=if_exists)


def overwrite_db_table_from_df(this_df, table_name, db_con, index=False):

    delete_all_table_rows(table_name, db_con)
    upload_df_to_table(this_df, table_name, db_con, index=index, if_exists='append')


def overwrite_db_table_from_df_matching_single_eq_condition(this_df, table_name, db_con, col_cond, val_cond, index=False):

    delete_table_rows_matching_single_eq_condition(table_name, db_con, col_cond, val_cond)
    upload_df_to_table(this_df, table_name, db_con, index=index, if_exists='append')


def overwrite_db_table_from_df_date_greater_than(this_df, table_name, db_con, date_col, val_cond, index=False):

    delete_table_rows_date_greater_than(table_name, db_con, date_col, val_cond)
    upload_df_to_table(this_df, table_name, db_con, index=index, if_exists='append')


def overwrite_db_table_from_df_matching_multiple_eq_condition(this_df, table_name, db_con, **kwargs):

    delete_table_rows_matching_multiple_eq_condition(table_name, db_con, **kwargs)
    upload_df_to_table(this_df, table_name, db_con, if_exists='append')


def delete_table_rows_matching_multiple_eq_condition(table_name, db_con, **kwargs):

    condition_strings = []

    # Loop through each kwargs to add condition to list
    counter = 0
    for key, value in kwargs.items():
        if value is None:
            continue

        if counter == 0:
            condition_strings.append("WHERE ")
        else:
            condition_strings.append("AND ")

        if isinstance(value, str):
            condition = f"{key} = '{value}'"
        else:
            condition = f"{key} = {value}"

        condition_strings.append(condition)

        counter += 1

    condition_str = " ".join(condition_strings)

    query = f"""
        DELETE FROM {table_name}
        {condition_str}
        """

    db_con.execute(query)



