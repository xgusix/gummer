#Example of output
from prettytable import from_db_cursor

aid = '101' # Must be unique
name = "Default output"
desc = "Print the result on the terminal within a pretty table.\n"

def launch(data):
	table = from_db_cursor(data)
	print table