class Column:

	def __init__(self, table_from, name, width):
		self.table = table_from
		self.name = name
		self.width = width

from flask import Flask, render_template
import sqlite3 as db

studb = db.connect("studb.db")
cursr = studb.cursor()
cursr.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = []
fetch_names = cursr.fetchall()
for i in range(len(fetch_names)):
	tables.append( (i, fetch_names[i][0]) )

column_names = {
	
	"LessonID":		Column("Lessons", "Пара", 80),
	"SubjID":		Column("Subjects", "Предмет", 200),
	"AudienceID":	Column("Audiences", "Аудитория", 90),
	"GroupID":		Column("Groups", "Группа", 90),
	"TeacherID":	Column("Teachers", "Преподаватель", 150),
	"TypeID":		Column("LessonTypes", "Тип", 60),
	"WeekdayID":	Column("Weekdays", "День Недели", 120)

}

table_column_names = {
	
	#Table Name 	#Pairs ('Column Title', 'Width')
	"Audiences": 	[("Аудитории", 90)],
	"Groups":		[("Группы", 110)],
	"LessonTypes":	[("Типы Занятий", 70)],
	"Lessons":		[("Пары", 80), ("Индексы", 80)],
	"Subjects":		[("Предметы", 200)],
	"Teachers":		[("Преподаватели", 100)],
	"Weekdays":		[("Дни Недели", 100), ("Индексы", 60)]
}

def load_page(page, **kwargs):
	return render_template(page, items=[i[1] for i in tables], **kwargs)

def gen_items(table=[]):

	items = []
	for i in table:
		items.append('<td id="elem">' + '</td><td id="elem">'.join([str(k) for k in i]) + "</td>")
	
	return items

def generating_table(table_name=tables[0][1]):

	tabl = [i[1] for i in tables]
	if table_name in tabl:

		cursr.execute("PRAGMA table_info(%s)"%table_name)
		header = []
		
		header_data = cursr.fetchall()
		for i in header_data:
			if i[1] != "ID":
				header.append(i[1])

		####QUERY_GENERATOR ########################
		
		query = "SELECT "
		for i in header:
			if i in column_names.keys():
				query += "(SELECT Name FROM " + column_names[i].table + " WHERE ID == S." + i + ") AS '" + column_names[i].name + "', "
			else:
				query += i+", "

		query = query[:-2] + " "
		query += "FROM " + table_name + " AS S"
		
		if "WeekdayID" in header:
			query += ", Weekdays AS W WHERE W.ID == S.WeekdayID ORDER BY W.ID"

		####END_QUERY_GENERATOR ####################

		#Get column widthes:
		column_widthes = []
		if table_name in table_column_names.keys():

			#From table's column widthes
			column_widthes = [i[1] for i in table_column_names[table_name]]
		
		else:
			
			#As header width
			for i in range(len(header)):
				if header[i] in column_names.keys():
					column_widthes.append(column_names[header[i]].width)


		#Get translated header:
		if table_name in table_column_names.keys():
			
			#from table's column names
			header = [i[0] for i in table_column_names[table_name]]
		else:

			#As names from table where ID translates to Names
			for i in range(len(header)):
				if header[i] in column_names.keys():
					header[i] = column_names[header[i]].name

		#Item generator
		items = []	
		cursr.execute(query) 	#Executing current query
		data = cursr.fetchall()

		#Replacing cycle (Nones to default values for 'None')
		for i in data:
			items.append(["<i>Неизвестно</i>" if j == None else j for j in i])

		return header, gen_items(items), table_name, column_widthes


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    return load_page("start.html")

@app.route("/table/<table>", methods=["GET", "POST"])
def open(table="Audiences"):
	heading, gen, name, widthes = generating_table(table)
	return load_page("start.html", heading=heading, name=name, table=gen, widthes=widthes)

if __name__ == "__main__":
	app.run()
