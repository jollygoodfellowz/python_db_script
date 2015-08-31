#!/usr/bin/env python
# Example for insert call INSERT INTO text (website) VALUES ("www.example.com");
import argparse, sys, MySQLdb

parser = argparse.ArgumentParser("Setup the city tables in mysql")
parser.add_argument('-l', "--host", type=str,
	help = "The host duh! Defaults to localhost")
parser.add_argument('-u', "--user", type=str,
	help="The username you wish to use. The default is root")
parser.add_argument('password', type=str, 
	help = "Password to access the database")
parser.add_argument('database', type=str, 
	help = "The database to access")
parser.add_argument('infile', nargs='?', 
	type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-v', "--verbose", action='store_true')
args = parser.parse_args()

# Grab arguments
host = args.host
user = args.user
password = args.password
database = args.database
ifp = args.infile
verbose = args.verbose

# Check for flags
if not host:
	host = "localhost"
if not user:
	user = "root"
if not verbose:
	verbose = False

db = MySQLdb.connect(host,user,password,database)
cursor = db.cursor()

for line in ifp:

	#Get rid of that annoying '\n' delimeter
	city = line.split('\n')
	city = city[0]

	sql = "CREATE TABLE IF NOT EXISTS " + city + " (website MEDIUMTEXT, INDEX(website(10)));"

	if verbose:
		print ("Trying sql query\n" + sql)

	try:
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()

db.close()