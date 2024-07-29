from MySQLConnector import MySQLConnector

from dotenv import load_dotenv
import os



# if __name__ == "__main__":
#     load_dotenv()  # Load environment variables from .env file
#     connection = MySQLConnector()
#     connection.connect()
#     connection.disconnect()

    # Usage example
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env 
    test_files = ["mysql-config/authors.sql", "mysql-config/posts.sql","mysql-config/mastodon.sql"]
    db_name = 'testing_db'
    db = MySQLConnector()
    db.connect()
    db.create_database(db_name)  # Replace 'new_database' with the desired database name
    db.use_database(db_name)  # Use the specified database from .env
    for file in test_files:
        db.execute_script_from_file(file)
    db.drop_database(db_name)
    db.disconnect()
