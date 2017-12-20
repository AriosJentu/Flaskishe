
from flask import Flask, render_template, request, redirect, url_for
from math import ceil

from db import *
from tablegen import *
from editbase import *

app = Flask(__name__)

is_edit = False
qcount = 1

@app.route("/", methods=["GET", "POST"])
def open():

	global table_size, order_by, cur_page, page_size, current_table, \
		compare_type, is_edit, qcount, cmp_queries

	ptab = current_table
	current_table = request.form.get("TableChooser")
	compare_type = request.form.get("TableQueryComparation")
	page_size = request.form.get("TablePageSizes")
	
	print(current_table)
	print(compare_type)
	print(page_size)
	print()

	if current_table == None:
		current_table = "Audiences"

	if compare_type == None:
		compare_type = "AND"

	if page_size == None:
		page_size = 10

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

		if "Delete" in i:
			real_vals = get_real_values(current_table, eval(i[6:]))
			
			values = {}
			for i in range(len(tables_info[current_table])):
				column = tables_info[current_table][i].name
				values[column] = real_vals[i]

			print(values)
			remove_record(current_table, values)

		if i == "GenerateTable" and ptab != current_table:

			order_by = None
			is_edit = False
			cmp_queries = []
			qcount = 1

	cmp_queries = []

	for i in range(qcount):
		if i != removableindex:

			column = request.form.get("QueryColumn"+str(i))
			cmp_char = request.form.get("QueryCmp"+str(i))
			value = request.form.get("QueryValue"+str(i))
			
			print([column, cmp_char, value])

			if value != None and value != "" and value != " ":
				column = get_name_from_title(current_table, column)
				cmp_queries.append(CmpExpression(column, cmp_char, value))
			else:
				cmp_queries.append(-1)

	print(current_table)

	order = order_by
	containing, table_size = generate_table(
		table_name=current_table,
		psize=page_size, 
		page=cur_page, 
		order=order, 
		compare_queries=cmp_queries,
		cmp_type=compare_type
	)

	print(table_size)
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
	)


if __name__ == "__main__":
	app.run()