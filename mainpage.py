class Converter():

	"""def to_ascii(h):
		strs = ""
		for i in range(len(h)//2):
			strs += chr(int(h[(i*2):(i*2)+2], 16))
		#print(strs)
		return strs
				
	def to_hex(s):
		strs = ""
		for i in range(len(s)):
			strs += "%x"%(ord(s[i]))
		#print(strs)
		return strs"""

	def encode(w):
		w = w.replace("[", "!$lo$!")
		w = w.replace("]", "!$lc$!")
		w = w.replace("'", "!$sa$!")
		w = w.replace('"', "!$da$!")
		w = w.replace(" ", "!$sp$!")
		w = w.replace(",", "!$cm$!")
		w = w.replace(".", "!$dt$!")
		w = w.replace("-", "!$mn$!")
		return w

	def decode(w):
		w = w.replace("!$lo$!", "[")
		w = w.replace("!$lc$!", "]")
		w = w.replace("!$sa$!", "'")
		w = w.replace("!$da$!", '"')
		w = w.replace("!$sp$!", " ")
		w = w.replace("!$cm$!", ",")
		w = w.replace("!$dt$!", ".")
		w = w.replace("!$mn$!", "-")
		return w

class Column:

	def __init__(self, table_from=None, cname="Name", width=100, title="Title", column="ColName"):
		self.table = table_from
		self.cname = cname
		self.width = width
		self.title = title
		self.column = column

	def __eq__(self, val):
		return val == self.name

class Query:

	def __init__(self, name="-1", cmp_char=">", value=""):
		self.name = name
		self.cmp = cmp_char
		self.value = value
	
	def __str__(self):
		return "['"+self.name+"', '"+self.cmp+"', '"+self.value+"']"

	def __eq__(self, val):
		return val == self.cname


from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as db
from math import ceil

studb = db.connect("studb.db")
cursr = studb.cursor()
cursr.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = []
fetch_names = cursr.fetchall()
for i in range(len(fetch_names)):
	tables.append( (i, fetch_names[i][0]) )


###GLOBAL VARIABLES

QUERIES_COUNT = 1
SELECTED_TABLE="Audiences"
PAGE_NUM = 1
PAGE_SIZE = 10
TABLE_SIZE = 0
PG_COUNT = 0
CMP_MERGER = "И"

QUERIES_TABLE = []
TABLE_COLUMNS = []
TABLE_DATA = []
TABLE_DEFAULT_DATA = []
EDITED_RECORDS = []
CUR_QUERY = Converter.encode("[[]]")
ORDERED_BY = None
IS_EDIT_MODE = False

###CONSTANTS

page_size_list = [5, 10, 15, 20, 50, 100]
cmp_mrg_list = {"И":"AND", "Или":"OR"}
cmp_list = [">", "<", "==", "<=", ">=", "!=", "LIKE", "NOT LIKE"]
arrows = {"desc":"↑", "asc":"↓"}

column_names = [
	
	Column(column="LessonID", 	table_from="Lessons", 		cname="Пара", 			width=80,	title="Name"),
	Column(column="SubjID",		table_from="Subjects", 		cname="Предмет", 		width=200,	title="Name"),
	Column(column="AudienceID",	table_from="Audiences", 	cname="Аудитория", 		width=90,	title="Name"),
	Column(column="GroupID",	table_from="Groups", 		cname="Группа", 		width=90,	title="Name"),
	Column(column="TeacherID",	table_from="Teachers", 		cname="Преподаватель", 	width=150,	title="Name"),
	Column(column="TypeID",		table_from="LessonTypes", 	cname="Тип", 			width=60,	title="Name"),
	Column(column="WeekdayID",	table_from="Weekdays", 		cname="День Недели", 	width=120,	title="Name")

]


table_column_names = {
	
	#Table Name 	#Pairs ('Column Title', 'Width')
	"Audiences": 	[Column(cname="Аудитории", width=90)],
	"Groups":		[Column(cname="Группы", width=110)],
	"LessonTypes":	[Column(cname="Типы Занятий", width=70)],
	"Lessons":		[Column(cname="Пары", width=80), Column(cname="Индексы", width=80)],
	"Subjects":		[Column(cname="Предметы", width=200)],
	"Teachers":		[Column(cname="Преподаватели", width=100)],
	"Weekdays":		[Column(cname="Дни Недели", width=100), Column(cname="Индексы", width=60)],
}



def load_page(page, **kwargs):
	return render_template(
		page, 
		items=[i[1] for i in tables], 
		pglist=page_size_list, 
		cursize=PAGE_SIZE, 
		curpg=PAGE_NUM, 
		count=PG_COUNT,
		tabsize=TABLE_SIZE,
		mrg_id=CMP_MERGER,
		mrg_list=cmp_mrg_list,
		cmp_list=cmp_list,
		low=min((PAGE_NUM-1) * PAGE_SIZE + 1, TABLE_SIZE),
		high=min(((PAGE_NUM) * PAGE_SIZE), TABLE_SIZE),
		queries=QUERIES_TABLE,
		qlen=len(QUERIES_TABLE),
		qcnt=QUERIES_COUNT,
		curquery=CUR_QUERY,
		orderby=ORDERED_BY,
		editmode=IS_EDIT_MODE,
		edited=EDITED_RECORDS,
		**kwargs
	)

def add_record(size):

	global SELECTED_TABLE

	if size > 0:
		query = "INSERT INTO "+SELECTED_TABLE+" VALUES (" + ("-1, "*size)[:-2] + ")"
		print("APPEND QUERY")
		print(query)
		print("EXECUTING APPEND")
		cursr.execute(query)

	studb.commit()


def remove_record(elements):

	global SELECTED_TABLE, TABLE_DATA, TABLE_DEFAULT_DATA, TABLE_COLUMNS
	
	for i, v in enumerate(elements):
		if v == "<i>Неизвестно</i>":
			elements[i] = "None"

	query = "DELETE FROM "+SELECTED_TABLE+" WHERE "

	indx = -1
	print()
	print(elements)
	print()
	for i in range(len(TABLE_DATA)):
		print(TABLE_DATA[i])
		if elements == TABLE_DATA[i]:
			indx = i
			break

	print(indx)

	for i in range(len(TABLE_COLUMNS)):
		query += TABLE_COLUMNS[i] + " == '" + TABLE_DEFAULT_DATA[indx][i] + "' "

		if i < len(TABLE_COLUMNS)-1:
			query += "AND "

	print("REMOVE QUERY")
	print(query)
	if len(elements) == len(TABLE_COLUMNS) and indx != -1:
		print("EXECUTING REMOVE")
		cursr.execute(query)

	studb.commit()

def update_record(upd_from, upd_to):
	global SELECTED_TABLE, TABLE_DATA, TABLE_COLUMNS, TABLE_DEFAULT_DATA

	for i, v in enumerate(upd_from):
		if v == "<i>Неизвестно</i>":
			upd_from[i] = "None"


	query = "UPDATE "+SELECTED_TABLE +" SET "

	indx = -1
	for i in range(len(TABLE_DATA)):
		if upd_from == TABLE_DATA[i]:
			indx = i
			break

	print(indx)
	print(upd_from)

	for i in range(len(TABLE_COLUMNS)):
		query += TABLE_COLUMNS[i] + " = '" + upd_to[i] + "'"
 
		if i < len(TABLE_COLUMNS)-1:
			query += ","

		query += " "

	query += "WHERE "
	for i in range(len(TABLE_COLUMNS)):
		query += TABLE_COLUMNS[i] + " == '" + TABLE_DEFAULT_DATA[indx][i] + "' "
		if i < len(TABLE_COLUMNS)-1:
			query += "AND "

	print("UPDATE QUERY")
	print(query)
	if len(upd_to) == len(TABLE_COLUMNS) and indx != -1:
		print("EXECUTING UPDATE")
		cursr.execute(query)

	studb.commit()


def gen_items(table=[]):

	items = []
	for i in table:
		tab = []
		for j in i:
			tab.append(str(j))

		items.append(tab)
		#items.append('<td id="elem">' + '</td><td id="elem">'.join([str(k) for k in i]) + "</td>")
	
	return items

def generating_table(table_name=tables[0][1]):

	global PG_COUNT, TABLE_COLUMNS, QUERIES_TABLE, TABLE_SIZE, DEFAULT_TAB_COL_NAMES, TABLE_DATA, TABLE_DEFAULT_DATA

	tabl = [i[1] for i in tables]
	if table_name in tabl:

		cursr.execute("PRAGMA table_info(%s)"%table_name)
		header = []
		
		header_data = cursr.fetchall()
		print("HEADER DATA:")
		print(header_data)
		for i in header_data:
			header.append(i[1])

		TABLE_COLUMNS = header[:]

		#### QUERY_GENERATOR ########################
		
		basequery = "SELECT "
		for i in header:
			for j in column_names:
				if j.column == i and i != "ID":
					basequery += "(SELECT " + j.title + " FROM " + j.table + " WHERE ID == S." + i + ') AS "' + j.cname

					if ORDERED_BY != None and j.cname in ORDERED_BY:
						basequery += arrows["asc" if ORDERED_BY[0] == "+" else "desc"]

					basequery += '", '
					break
			else:

				name = i
				if i != "ID":
					tab = table_column_names[table_name]
					for k in range(len(tab)):
						print(k+1, header.index(i))
						if k+1 == header.index(i):
							name = tab[k].cname

				basequery += "S." + i

				if ORDERED_BY != None and name in ORDERED_BY:
					basequery += ' AS "' + name + arrows["asc" if ORDERED_BY[0] == "+" else "desc"] + '"'

				basequery += ', '


		basequery = basequery[:-2] + " "
		basequery += "FROM " + table_name + " AS S"
		
		where = False
		#if "WeekdayID" in header:
		#	basequery += ", Weekdays AS W WHERE W.ID == S.WeekdayID "
		#	where = True

		for i in QUERIES_TABLE:
			
			name = i.name
			if ORDERED_BY != None and name in ORDERED_BY:
				name += arrows["asc" if ORDERED_BY[0] == "+" else "desc"]

			local_query = '"' + name + '" ' + i.cmp + ' "' + i.value + '"'

			if i.cmp == "LIKE":
				local_query = 'instr("' + name  + '", "' + i.value + '") > 0'

			elif i.cmp == "NOT LIKE":
				local_query = 'instr("' + name + '", "' + i.value + '") == 0'

			if not where:
				basequery += ' WHERE ' + local_query
				where = True
					
			else:
				basequery += " " + cmp_mrg_list[CMP_MERGER] + " "
				basequery += local_query

		#if "WeekdayID" in header:
		#	basequery += " ORDER BY W.ID"

		if ORDERED_BY != None:
			ordertype = "ASC" if ORDERED_BY[0] == "+" else "DESC"
			char = arrows["asc" if ORDERED_BY[0] == "+" else "desc"]
			name = ORDERED_BY[1:]
			if name[-1] in arrows.values():
				name = name[:-1]

			basequery += ' ORDER BY "'+name+char+'" '+ordertype

		#Element Count
		basequery += " LIMIT " + str(PAGE_SIZE) + " OFFSET " + str(PAGE_SIZE*(PAGE_NUM-1))

		#### END_QUERY_GENERATOR ####################

		#Get column widthes:
		column_widthes = []
		if table_name in table_column_names.keys():

			is_id_in = False
			if "ID" in header:
				is_id_in = True

			#From table's column widthes
			column_widthes = [i.width for i in table_column_names[table_name]]
			
			if is_id_in:
				column_widthes = [30] + column_widthes


		else:
			
			#As header width
			for i in range(len(header)):
				for j in column_names:
					if header[i] == j.column:
						column_widthes.append(j.width)


		#Get translated header:
		#print(header)
		if table_name in table_column_names.keys():
			
			is_id_in = False
			if "ID" in header:
				is_id_in = True

			#from table's column names
			header = [i.cname for i in table_column_names[table_name]]

			if is_id_in:
				header = ["ID"] + header
		else:

			#As names from table where ID translates to Names
			for i in range(len(header)):
				for j in column_names:
					if header[i] == j.column:
						header[i] = j.cname

		query_selector = header[:]
		for i in range(len(header)):
			if ORDERED_BY != None and header[i] in ORDERED_BY:
				if header[i][-1] in arrows.values():
					header[i] = header[i][:-1]
				header[i] += arrows["asc" if ORDERED_BY[0] == "+" else "desc"]


		print()
		print()
		print(header)
		print(query_selector)
		print(basequery)
		print()
		print()

		#Count
		cursr.execute("SELECT Count(*) FROM ("+basequery[:basequery.find("LIMIT")]+")")
		data = cursr.fetchall()
		TABLE_SIZE = data[0][0] 
		PG_COUNT = ceil(TABLE_SIZE/PAGE_SIZE)
  
		#Item generator
		items = []	
		defitems = []

		cursr.execute(basequery) 	#Executing current query
		data =  [[str(j) for j in i] for i in cursr.fetchall()]
		TABLE_DATA = data

		ordered_by = ""
		if ORDERED_BY != None:	

			ordertype = "ASC" if ORDERED_BY[0] == "+" else "DESC"

			name = ORDERED_BY[1:] + arrows["asc" if ORDERED_BY[0] == "+" else "desc"]
			print(header)
			print(TABLE_COLUMNS)
			print(name)
			cname = TABLE_COLUMNS[header.index(name)]

			ordered_by = "ORDER BY "+ cname +" "+ordertype
		
		default_exec = "SELECT * FROM " + SELECTED_TABLE + " " + ordered_by + " LIMIT " + str(PAGE_SIZE) + " OFFSET " + str(PAGE_SIZE*(PAGE_NUM-1))
		print(default_exec)
		cursr.execute(default_exec)
		TABLE_DEFAULT_DATA = [[str(j) for j in i] for i in cursr.fetchall()]

		#print(PG_COUNT, TABLE_SIZE, PAGE_SIZE)

		#Cycle replacement (Nones to default values for 'None')
		for i in data:
			#items.append(i)
			items.append(["<i>Неизвестно</i>" if j == "None" else j for j in i])

		for i in TABLE_DEFAULT_DATA:
			defitems.append(["-1" if j == "None" else j for j in i])

		print()
		print("DEFITEMS IS:")
		print(defitems)
		print()

		return header, query_selector, gen_items(items), gen_items(defitems), table_name, column_widthes


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def open():
	global SELECTED_TABLE, PAGE_NUM, PAGE_SIZE, QUERIES_COUNT, QUERIES_TABLE, TABLE_COLUMNS, CUR_QUERY, CMP_MERGER, ORDERED_BY, IS_EDIT_MODE, EDITED_RECORDS, TABLE_DATA

	#ln = len(QUERIES_TABLE)

	QUERIES_TABLE = []
	
	local_query = Converter.decode(request.args.get("query", default=Converter.encode("[[]]"), type=str)) #get query from adress line, converted to ascii executable string
	
	IS_EDIT_MODE = request.args.get("edit", default=False, type=bool) or IS_EDIT_MODE
	
	print()
	print("Local Query:")
	print(local_query)

	for i in range(QUERIES_COUNT):

		qcolumn = request.form.get("QueryColumn"+str(i)) or "ID"
		qcompare = request.form.get("QueryCmp"+str(i)) or ">"
		qinput = request.form.get("QueryIn"+str(i)) or ""
		
		print(qcolumn, qinput, qcompare)
		curquery = Query(qcolumn, qcompare, qinput)
		if qinput != "":
			print("Appending")
			QUERIES_TABLE.append(curquery)

	#if table not initializate, and length of link query is good to convert it back to ascii code
	print()
	print("Current Query:")
	print(CUR_QUERY)
	if QUERIES_TABLE == [] and len(CUR_QUERY) > 24:
		QUERIES_TABLE = [Query(*i) for i in eval(Converter.decode(CUR_QUERY))]

	elif QUERIES_TABLE == [] and len(CUR_QUERY) == 24:
		CUR_QUERY = Converter.encode(local_query) 

	print()
	print("Query After:")
	print(CUR_QUERY)

	print()
	print("Printing all list of queries")
	print(str([eval(str(i)) for i in QUERIES_TABLE]))

	CUR_QUERY = Converter.encode(str([eval(str(i)) for i in QUERIES_TABLE])) #current query, converted to link version

	if "plus" in request.form:
		QUERIES_COUNT += 1

	elif "minus" in request.form:
		QUERIES_COUNT -= 1

	table = request.form.get("List") or request.args.get("table", default="Audiences", type=str)
	orderby = request.args.get("orderby", default="None", type=str)

	if "go" in request.form:
		if table != SELECTED_TABLE:
			QUERIES_TABLE = []
			CUR_QUERY = Converter.encode("[[]]")
			QUERIES_COUNT = 1
			ORDERED_BY = None
			PAGE_NUM = 1

	elif "ModeChanger" in request.form:
		IS_EDIT_MODE = not IS_EDIT_MODE

	elif "AddRecord" in request.form:
		print("TABLE_COLUMNS:")
		print(TABLE_COLUMNS)
		add_record(len(TABLE_COLUMNS))
		print(TABLE_DATA)


	print("REQUEST FORM:")
	for i in request.form:
		print(i)
		if "Title" in i:
			print("Title found, its '"+i[5:]+"'")
			asc = i.find(arrows["asc"]) >= 0
			desc = i.find(arrows["desc"]) >= 0

			
			if not asc and not desc: #set it asc
				ORDERED_BY = "+"+i[5:]
			elif asc: #set it desc
				ORDERED_BY = "-"+i[5:]
			else:
				ORDERED_BY = None

		elif "Edit" in i:
			
				val = eval(i[4:])
				print(val)
				print()
				if val not in EDITED_RECORDS:
					EDITED_RECORDS.append(val)
				else:
					val_to = []
					for k in range(len(TABLE_COLUMNS)):
						print()
						print()
						print("Changing"+str(val)+"Column"+str(k))
						print("Changing"+str(val)+"Column"+str(k) in request.form)
						print()
						print()

						if "Changing"+str(val)+"Column"+str(k) in request.form:
							val_to.append(request.form.get("Changing"+str(val)+"Column"+str(k)))

					print(val_to)
					update_record(val, val_to)
					EDITED_RECORDS.remove(val)

		elif "Delete" in i:

				val = eval(i[6:])
				print(val)
				print()
				if val in EDITED_RECORDS:
					EDITED_RECORDS.remove(val)
				else:
					remove_record(val)
	
	print("REQUEST FORM ENDED")
	print(EDITED_RECORDS)



	ORDERED_BY = ORDERED_BY or (None if orderby == "None" else orderby)
	
	SELECTED_TABLE = table

	PAGE_NUM = request.args.get("page", default=PAGE_NUM,  type=int)
	PAGE_SIZE = request.form.get("PageSize") or request.args.get("count", default=10, type=int)
	CMP_MERGER = request.form.get("MrgType") or request.args.get("mrg", default="AND", type=str)

	for i, v in cmp_mrg_list.items():
		if v == CMP_MERGER:
			CMP_MERGER = i 

	PAGE_SIZE = int(PAGE_SIZE)

	heading, query_sel, gen, gen_def, name, widthes = generating_table(table)
	
	return load_page(
		"start.html", 
		heading=heading, 
		name=name, 
		table=gen, 
		tabdef=gen_def,
		widthes=widthes, 
		selected=SELECTED_TABLE,
		qsel=query_sel
	)

if __name__ == "__main__":
	app.run()
