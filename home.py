
from flask import Flask, render_template, request, redirect, url_for
from math import ceil


from db import *
from tablegen import *
from editbase import *
from olad import *

app = Flask(__name__)

is_edit = False
is_new = False
is_editing = False

qcount = 1

edit_rows = []
cmp_queries = []
hiding_cells = []
hiding_fields = []

def array(string):
	return [i[1:-1] if i.find("'") >= 0 or i.find('"') >= 0 else int(i) for i in string[1:-1].split(", ")]

@app.route("/", methods=["GET", "POST"])
def open():

	global table_size, order_by, cur_page, page_size, current_table, \
		compare_type, is_edit, qcount, cmp_queries, edit_rows, is_new, \
		is_editing

	saved_table = current_table
	saved_cmp = compare_type
	saved_psize = page_size
	
	current_table = request.form.get("TableChooser")
	compare_type = request.form.get("TableQueryComparation")
	page_size = request.form.get("TablePageSizes")
	
	##################################################################

	if current_table == None:
		current_table = saved_table

	if compare_type == None:
		compare_type = saved_cmp

	if page_size == None:
		page_size = saved_psize

	page_size = int(page_size)

	removableindex = -1
	for i in request.form:
		
		if i[:4] == "Page":
			cur_page = int(i[4:])


		if i[:5] == "Title":
			
			title = i[5:]

			if order_by != None:
				if "+"+title == order_by:
					order_by = "-"+title
			
				elif "-"+title == order_by:
					order_by = None
			
				else:
					order_by = "+"+title
			else:
				order_by = "+"+title


		if i == "ModeChanger":
			is_edit = not is_edit


		if i == "Plus":

			qcount += 1


		if "Minus" in i:

			qcount -= 1
			if qcount < 1:
				qcount = 1

			removableindex = int(i[5:])


		if i == "AddRecord":
			is_new = True
			edit_rows = []
			return redirect(url_for("edit"))


		if "EditR" in i:

			edit_rows = array(i[5:]) #eval(i[5:])
			print(edit_rows)
			is_editing = True
			return redirect(url_for("edit"))


		if "Delete" in i:

			real_vals = get_real_values(current_table, array(i[6:])) #eval(i[6:]))
			
			values = {}
			for i in range(len(tables_info[current_table])):
				column = tables_info[current_table][i].name
				values[column] = real_vals[i]

			#print(values)
			remove_record(current_table, values)


		if i == "UpdateTable":
		
			if len(edit_rows) > 0:

				columns = [i.name for i in tables_info[current_table]]
				values = []
				if "ID" in columns:
					values.append(edit_rows[columns.index("ID")])

				for i in columns:
					if i != "ID":
						val = request.form.get("EditColumn"+str(i))
						values.append(val)

				upd_frm = {columns[i]:edit_rows[i] for i in range(len(columns))}
				upd_to = {columns[i]:values[i] for i in range(len(columns))}
				edit_rows = []

				update_record(current_table, upd_frm, upd_to)


			elif is_new:

				columns = [i.name for i in tables_info[current_table]]
				values = []
				if "ID" in columns:
					columns.remove("ID")

				for i in columns:
					values.append(request.form.get("EditColumn"+str(i)))

				add_record(current_table, values)				


		if i == "GenerateTable" and saved_table != current_table:

			order_by = None
			is_edit = False
			is_new = False
			cmp_queries = []
			edit_rows = []
			qcount = 1

		if i == "SchedOverview":
			return redirect(url_for("overview"))


	if is_editing:
		is_editing = False

	else:

		cmp_queries = []
		for i in range(qcount):

			if i != removableindex:

				column = request.form.get("QueryColumn"+str(i))
				cmp_char = request.form.get("QueryCmp"+str(i))
				value = request.form.get("QueryValue"+str(i))
				
				if value != None and value != "" and value != " ":

					column = get_name_from_title(current_table, column)
					cmp_queries.append(CmpExpression(column, cmp_char, value))

				else:
					cmp_queries.append(-1)


	order = order_by
	containing, table_size = generate_table(
		table_name=current_table,
		psize=page_size, 
		page=cur_page, 
		order=order, 
		compare_queries=cmp_queries,
		cmp_type=compare_type
	)


	return render_template(
		"main.html",
		curtable=current_table,
		tables=[i for i in tables_info.keys()],
		widthes=[i.width+40 for i in tables_info[current_table]],
		cmptypes=["AND", "OR"],
		sizes=[5, 10, 20, 50, 100],
		cursize=page_size,
		curpage=cur_page,
		pagescount=ceil(table_size/page_size),
		tabsize=table_size,
		titles=[i.title for i in tables_info[current_table]],
		titles_origin=[i.name for i in tables_info[current_table]],
		compares=comparison_chars,
		cmptype=compare_type,
		containing=containing,
		orderby=(None if order == None else order[1:]),
		ordertype=(None if order == None else order[0]),
		queries=cmp_queries,
		qcount=max(qcount, len(cmp_queries)),
		realqcount=len([0 for i in cmp_queries if i != -1]),
		isedit=is_edit,
		low=min((cur_page-1) * page_size + 1, table_size),
		high=min(((cur_page) * page_size), table_size),
		editrows=edit_rows
	)

@app.route("/edit", methods=["GET", "POST"])
def edit():

	global edit_rows, current_table, is_new

	values = []
	for i in tables_info[current_table]:
		if i.name != "ID":
			values.append(get_list_values_of_column(current_table, i.name))

	columns = [i.name for i in tables_info[current_table]]
	id_ = columns.index("ID")
	columns.remove("ID")
	edits = edit_rows[:id_] + edit_rows[id_+1:]
	#for i in range(len(columns)):
	#	if columns[i] == "ID":
	#		values = values[:i]+values[i+1:]
	#		edits = edits[:i]+edits[i+1:]
	#		columns.remove("ID")
	#		break

	print("EDIT:")
	print(edits)
	print(columns)
	print(values)

	return render_template(
		"edit.html",
		editrows=edits,
		columns=columns,
		values=values,
		isnew=is_new,
		pagetoload="/"

	)

edit_field = -1
@app.route("/overview", methods=["GET", "POST"])
def overview():

	global join_column, join_row, ordering_column, tables_info, hiding_cells, current_columns, current_rows, hiding_fields, edit_field

	col_asc_type = request.form.get("OrderTypeColumns", type=int)
	row_asc_type = request.form.get("OrderTypeRows", type=int)
	colname = request.form.get("JoiningTableColumns")
	rowname = request.form.get("JoiningTableRows")
	edit_values = request.form.get("DatabaseEditor")

	if edit_values != None and edit_values != "":
		print(edit_values)

		columns = [i.name for i in tables_info["SchedItems"]]

		edit_values = edit_values.replace("\t", "")
		obj_id, row_val, col_val = str(edit_values[3:]).split(", ")
		obj_id = int(obj_id)

		update_sched_record(obj_id, join_column, join_row, col_val, row_val)


	joining_columns = None
	joining_rows = None

	for i in tables_info["SchedItems"]:

		if i.title == colname:
			joining_columns = i

		if i.title == rowname:
			joining_rows = i


	rows_asc = {None:None, 0:None, 1:True, 2:False}[row_asc_type]
	columns_asc =  {None:None, 0:None, 1:True, 2:False}[col_asc_type]

	for i in request.form:
		print(i)

	for i in request.form:
		if i == "Back":
			return redirect("/")

		if i == "Accept":

			ordering_column.ascending = None
			
			if joining_columns.name != join_column.name or join_row.name != joining_rows.name:
				hiding_cells = []
				hiding_fields = []
				

			join_column = joining_columns
			join_row = joining_rows


		if "HideField" in i:

			hideindex = int(i[9:])
			if hideindex in hiding_fields:
				hiding_fields.remove(hideindex)
			else:
				hiding_fields.append(hideindex)

		if "HideCell" in i:

			hideindex = int(i[8:])
			if hideindex in hiding_cells:
				hiding_cells.remove(hideindex)
			else:
				hiding_cells.append(hideindex)

		if "EditField" in i:
			
			values = []
			for k in tables_info["SchedItems"][1:]:
				values.append(get_list_values_of_column("SchedItems", k.name))

			columns = [k.name for k in tables_info["SchedItems"][1:]]
			
			query = "SELECT * FROM SchedItems WHERE ID == ?"
			cursr.execute(query, (int(i[9:]),))
			edits = list(cursr.fetchall()[0])
			print("EDITS")
			print(edits)
			edits = get_real_values("SchedItems", edits, True)[1:]

			col_id = tables_info["SchedItems"].index(join_column) - 1
			row_id = tables_info["SchedItems"].index(join_row) - 1

			values[col_id] = edits[col_id]
			values[row_id] = edits[row_id]

			print("FIELDS:")
			print(edits)
			print(columns)
			print(values)
			edit_field = int(i[9:])
			print("EDIT FIELD:")
			print(edit_field)

			return render_template(
				"edit.html",
				editrows=edits,
				columns=columns,
				values=values,
				isnew=False,
				pagetoload="/overview"

			)

		if "DeleteField" in i:

			id_ = int(i[11:])
			query = "DELETE FROM SchedItems WHERE ID == "+str(id_)
			cursr.execute(query)


		if i == "UpdateTable":
		
			if edit_field >= 0:

				columns = [k.name for k in tables_info["SchedItems"] if k.name != "ID"]
				values = []

				for k in columns:
					val = request.form.get("EditColumn"+str(k))
					values.append(val)

				print("VALUES")
				print(values)
				values = get_real_values("SchedItems", [edit_field] + values)[1:]
				print(values)
				query = "UPDATE SchedItems SET " + ", ".join([k + " == ? " for k in columns] ) + " WHERE ID == " + str(edit_field)
				print("VALUES IPAL:")
				print(query, values)
				cursr.execute(query, tuple(values))



		if "Title" in i:
			name = i[5:]
			
			if ordering_column.name == name:
				
				ordering_column.ascending = {None:True, True:False, False:None}[ordering_column.ascending]

			else:
				for k in tables_info["SchedItems"]:
					if k.name == name:
						ordering_column = k
						ordering_column.ascending = True
						break



	join_column.ascending = columns_asc
	join_row.ascending = rows_asc
	table, rows, columns = generate_schedule(join_column, join_row, ordering_column)

	current_columns = columns 
	current_rows = rows

	print("PAGE LOADED")
	return render_template(
		"overview.html",
		jcols=columns,
		jrows=rows,
		table=table,
		widthes=[i.width+40 for i in tables_info["SchedItems"] if i != join_column and i != join_row],
		titles=[i.title for i in tables_info["SchedItems"] if i != join_column and i != join_row],
		titles_origin=[i.name for i in tables_info["SchedItems"] if i != join_column and i != join_row],
		join_col=join_column,
		join_row=join_row,
		orderby=ordering_column,
		columns=[i for i in tables_info["SchedItems"]],
		hidecells=hiding_cells,
		hidefields=hiding_fields
	)

if __name__ == "__main__":
	app.run()