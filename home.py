
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
hiding_tables = []
hiding_fields = []

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
			
			title = get_name_from_title(current_table, i[5:])

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

			edit_rows = eval(i[5:])
			is_editing = True
			return redirect(url_for("edit"))


		if "Delete" in i:

			real_vals = get_real_values(current_table, eval(i[6:]))
			
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
		values.append(get_list_values_of_column(current_table, i.name))

	columns = [i.name for i in tables_info[current_table]]
	edits = edit_rows[:]
	for i in range(len(columns)):
		if columns[i] == "ID":
			values = values[:i]+values[i+1:]
			edits = edits[:i]+edits[i+1:]
			columns.remove("ID")
			break

	return render_template(
		"edit.html",
		editrows=edits,
		columns=columns,
		values=values,
		isnew=is_new
	)

@app.route("/overview", methods=["GET", "POST"])
def overview():

	global join_column, join_row, ordering_column, tables_info, hiding_tables, hiding_fields, current_columns, current_rows

	columns_asc = None
	rows_asc = None

	col_asc_type = request.form.get("OrderTypeColumns")
	row_asc_type = request.form.get("OrderTypeRows")
	colname = request.form.get("JoiningTableColumns")
	rowname = request.form.get("JoiningTableRows")
	edit_values = str(request.form.get("DatabaseEditor"))

	if edit_values != "None" and len(edit_values) > 3 and edit_values[:3] == "Div":
		print(edit_values)

		columns = [i.name for i in tables_info["SchedItems"]]

		upd_values, cell_from, cell_to = eval(edit_values[3:])

		from_row_indx = cell_from//len(current_columns)					
		from_col_indx = cell_from - from_row_indx*len(current_columns)	

		to_row_indx = cell_to//len(current_columns)						
		to_col_indx = cell_to - from_row_indx*len(current_columns)			

		column_from_value = current_columns[from_col_indx]					
		column_to_value = current_columns[to_col_indx]							

		row_from_value = current_rows[from_row_indx]							
		row_to_value = current_rows[to_row_indx]								

		upd_from = {}
		k = 0
		for col in columns:
			if col == join_column.name:
				upd_from[col] = column_from_value
			elif col == join_row.name:
				upd_from[col] = row_from_value
			else:
				upd_from[col] = upd_values[k]
				k = k+1

		upd_to = {}
		k = 0
		for col in columns:
			if col == join_column.name:
				upd_to[col] = column_to_value
			elif col == join_row.name:
				upd_to[col] = row_to_value
			else:
				upd_to[col] = upd_values[k]
				k = k+1


		update_record("SchedItems", upd_from, upd_to)




	joining_columns = None
	joining_rows = None

	for i in tables_info["SchedItems"]:

		if i.title == colname:
			joining_columns = i

		if i.title == rowname:
			joining_rows = i


	if col_asc_type == "По Возрастанию":
		columns_asc = True

	elif col_asc_type == "По Убыванию":
		columns_asc = False


	if row_asc_type == "По Возрастанию":
		rows_asc = True

	elif row_asc_type == "По Убыванию":
		rows_asc = False

	for i in request.form:

		if i == "Back":
			return redirect("/")

		if i == "Accept":

			ordering_column.ascending = None
		
			join_column = joining_columns
			join_row = joining_rows

			hiding_tables = []
			hiding_fields = []

		if "Title" in i:
			name = i[5:]
			
			if ordering_column.name == name:
				
				if ordering_column.ascending == None:
					ordering_column.ascending = True
				
				elif ordering_column.ascending == True:
					ordering_column.ascending = False

				elif ordering_column.ascending == False:
					ordering_column.ascending = None

			else:
				for k in tables_info["SchedItems"]:
					if k.name == name:
						ordering_column = k
						ordering_column.ascending = True
						break

		if "HideRow" in i:
			row_name = i[7:]
			if row_name in hiding_tables:
				hiding_tables.remove(row_name)
			else:
				hiding_tables.append(row_name)

		if "HideField" in i:
			field = eval(i[9:])
			if field in hiding_fields:
				hiding_fields.remove(field)
			else:
				hiding_fields.append(field)


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
		hides=hiding_tables,
		hides_fields=hiding_fields
	)

if __name__ == "__main__":
	app.run()