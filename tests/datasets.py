from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert

database_path = "sqlite:///tests/requests.db"


def create_custom_table(table_name):
    # Create the engine
    engine = create_engine(database_path)

    # Create a MetaData instance
    metadata = MetaData()

    # Define the table
    custom_table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("request", String),
    )

    # Create the table
    metadata.create_all(engine)

    return custom_table


def update_database_with_new_table(table_name):
    try:
        # Create the custom table
        custom_table = create_custom_table(table_name)

        # Create a session
        engine = create_engine(database_path)
        Session = sessionmaker(bind=engine)
        session = Session()

        # You can add data to the new table here if needed
        # For example:
        # connection = engine.connect()
        # connection.execute(custom_table.insert().values(request="Sample request"))
        # connection.close()

        print(f"Table '{table_name}' has been created successfully.")

        # Close the session
        session.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def insert_row(table_name, row):
    engine = create_engine(database_path)
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    with engine.connect() as conn:
        stmt = insert(table).values(row)
        conn.execute(stmt)
        conn.commit()
