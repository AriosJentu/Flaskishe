from flask import Flask, render_template
import sqlite3 as db

studb = db.connect("studb.db")
cursr = studb.cursor()
cursr.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = []
fetch_names = cursr.fetchall()
for i in range(len(fetch_names)):
	tables.append( (i, fetch_names[i][0]) )

def load_page(page, **kwargs):
	return render_template(page, items=[i[1] for i in tables], **kwargs)

def gen_items(table=[]):

	items = []
	for i in table:
		items.append("<td><center>"+"</center></td><td><center>".join([str(k) for k in i])+"</center></td>")
	
	return items

def generating_table(table_name=tables[0][1]):

	tabl = [i[1] for i in tables]
	if not table_name in tabl:
		table_name = tabl[0]

	cursr.execute("PRAGMA table_info(%s)"%table_name)
	header = []
	for i in cursr.fetchall():
		header.append(i[1])

	cursr.execute("SELECT * FROM "+table_name)

	items = []
	for i in cursr.fetchall():
		items.append(i)

	return header, gen_items(items), table_name

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    return load_page("start.html")

@app.route("/table/<table>", methods=["GET", "POST"])
def open(table="Audiences"):
	heading, gen, name = generating_table(table)
	return load_page("start.html", heading=heading, name=name, table=gen)

if __name__ == "__main__":
	app.run()