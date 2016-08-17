# importing the logging & argparse is bringing the already written code.  It's called abstraction.  
import logging  #allow you to track what happens in the application, and will help you identify any problems in the code
import argparse #allow you to access the ArgumentParser object to describe your interface and parse the list of arguments
import psycopg2

# Set the log output file, and the log level (DEBUG is one of five log levels)
#basicconfig calls the library named "snippets.log", (oven scenario)
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

# Connect to DB
# line 13 calls the database into the python
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

# CreateReadUpdateDelete put is Create. it overwrites any kind of key entry.

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet)) # google python loggin module info
    with connection, connection.cursor() as cursor:
        try:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet)) 
        except psycopg2.IntegrityError as e:
            connection.rollback()
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet

print("this works end of file")
    
def get(name):
    """
    Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        result = cursor.fetchone()
    if not result:
        # No snippet was found with that name.
        logging.info("Snippet not found")
        return "404: Snippet Not Found"
    logging.debug("Snippet retrieved successfully.")
    return result[0]
    
def catalog():
    """
    Returns a list of keywords in the DB
    """
    logging.info("Retrieving keywords from DB")
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword")
        result = cursor.fetchall()
    if not result:
        # No keywords found in the
        logging.info("No keywords found")
        return "404: No Keywords Found"
    logging.debug("Keywords retrieved successfully")
    return result
    
def search(string):
    """
    Returns a list of snippets containing a string
    """
    logging.info("Retrieving keywords from DB containing '{!r}'".format(string))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where message like '%{}%' order by keyword".format(string))
        results = cursor.fetchall()
    if not results:
        # No results found
        logging.info("No snippets found")
        return "404: No Messages Found"
    logging.debug("Snippets retrieved successfully")
    return results

def remove(name):
    """
    Remove a snippet with a given name
    If there is no such snippet, return '404: Snippet Not Found'.
    """
    logging.error("FIXME: Unimplemented - remove({!r}".format(name))
    return ""
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text") 

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Name of the snippet")
    
    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve all keywords")
    
    # Subparser for the catalog command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Retrieve all snippets containing a string")
    search_parser.add_argument("string", help="String to search")

    arguments = parser.parse_args()
    
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        result = catalog(**arguments)
        if isinstance(result,str):
            print(result)
        else:
            print("Keywords: ")
            for i in result:
                print(i[0])
    elif command == "search":
        results = search(**arguments)
        if isinstance(results,str):
            print(results)
        else:
            print("Snippets:")
            for result in results:
                print(result[0])

if __name__ == "__main__":
    main()
