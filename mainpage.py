from flask import Flask, render_template
import sqlite3 as db

studb = db.connect("studb.db")
cursr = studb.cursor()
cursr.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = []
fetch_names = cursr.fetchall()
for i in range(len(fetch_names)):
	tables.append( (i, fetch_names[i][0]) )

custom_tables = [(len(tables), "Schedule")]

def load_page(page, **kwargs):
	return render_template(page, items=[i[1] for i in tables+custom_tables], **kwargs)

def gen_items(table=[]):

	items = []
	for i in table:
		items.append('<td id="elem">'+'</td><td id="elem">'.join([str(k) for k in i])+"</td>")
	
	return items

def generating_table(table_name=tables[0][1]):

	tabl = [i[1] for i in tables]
	custom = [i[1] for i in custom_tables]
	if table_name in tabl:

		cursr.execute("PRAGMA table_info(%s)"%table_name)
		header = []
		for i in cursr.fetchall():
			header.append(i[1])

		cursr.execute("SELECT * FROM "+table_name)

		items = []	
		for i in cursr.fetchall():
			items.append(i)


	elif table_name in custom:

		if table_name == custom[0]:
			header = ["Пара", "Предмет", "Аудитория", "Группа", "Преподаватель", "Тип", "День"]
			
			cursr.execute("""
				SELECT 
					(SELECT L.Name FROM Lessons AS L WHERE L.ID == S.LessonID) AS Lesson,
					(SELECT Sj.Name FROM Subjects AS Sj WHERE Sj.ID == S.SubjID) AS Subject,
					(SELECT A.Name FROM Audiences AS A WHERE A.ID == S.AudienceID) AS Audience,
					(SELECT G.Name FROM Groups AS G WHERE G.ID == S.GroupID) AS LGroup,
					(SELECT T.Name FROM Teachers AS T WHERE T.ID == S.TeacherID) AS Teacher,
					(SELECT Tp.Name FROM LessonTypes AS Tp WHERE Tp.ID == S.TypeID) AS Type,
					(SELECT W.Name FROM Weekdays AS W WHERE W.ID == S.WeekdayID) AS Weekday
				FROM SchedItems AS S, Weekdays AS W
				WHERE Weekday == W.Name
				ORDER BY W.ID
			""")

			items = []
			for i in cursr.fetchall():
				column = []
				for j in i:
					if j == None:
						j = "<i>Неизвестно</i>"
					column.append(j)
				items.append(column)
			for i in items:
				print(i)
			
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
