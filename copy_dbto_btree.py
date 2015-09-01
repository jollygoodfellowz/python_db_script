#!/usr/bin/env python
import argparse
import sys
import MySQLdb

# CREATE TABLE mylookup (id varchar(100), INDEX USING BTREE (id)) ENGINE = MEMORY;
# The above query will create a new btree table
def main():
	parser = argparse.ArgumentParser("Setup the lookup table in mysql")
	parser.add_argument('-l', "--host", type=str,
		help = "The host duh! Defaults to localhost")
	parser.add_argument('-u', "--user", type=str,
		help="The username you wish to use. The default is root")
	parser.add_argument('password', type=str, 
		help = "Password to access the database")
	parser.add_argument('database', type=str, 
		help = "The database to access")
	args = parser.parse_args()

	# Grab arguments
	host = args.host
	user = args.user
	password = args.password
	database = args.database

	# Check for flags
	if not host:
		host = "localhost"
	if not user:
		user = "root"

	list_of_webs = []

	# Make the connection and make a cursos object
	db = MySQLdb.connect(host,user,password,database)
	cursor = db.cursor()

	# Grab all of the data one row at a time
	cursor.execute("Select url from crawled")
	loop = True
	while loop:
		site = cursor.fetchone()
		list_of_webs.append(site)

		if list_of_webs[-1] is None:
			list_of_webs.pop()
			loop = False

	# Add all of the data into the new binary tree table
	for site in list_of_webs:
		new_site = str(site).split("'")
		site = new_site[1]
		sql = "INSERT INTO newcrawled (id) VALUES ("+ '"' + site + '")'
		cursor.execute(sql)
		print sql
	

	list_of_webs = []

if __name__ == "__main__":
	main()