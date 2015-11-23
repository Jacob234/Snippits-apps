"""General description

"""
import argparse
import sys
import logging
import psycopg2
# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.info("Starting snippets app")
logging.debug("connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets'")
logging.debug("Database connection established")

def put(name, snippet):
    """ Store a snippet with an associated name.  Returns the name and the snippet """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    try:
        command = "insert into snippets values (%s, %s)"
        with connection, connection.cursor() as cursor:
            cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e: 
        command = "update snippets set message=%s where keyword=%s"
        with connection, connection.cursor() as cursor:
            cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored succesfully.")
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.If there is no such snippet print snippet can't be found."""
    logging.info("Retrieving snippet {!r}".format(name))
    command = "select * from snippets where keyword= (%s)"
    with connection, connection.cursor() as cursor:
        cursor.execute(command, (name,))
        row = cursor.fetchone()
    logging.debug("Snippet retrieved succesfully.")
    if not row:
        return "%s Cannot Be Found" % name
    return row[1]
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    
if __name__ == "__main__":
    main()