
from flask import Flask, render_template, request, redirect, url_for
from math import ceil

from db import *
from tablegen import *

app = Flask(__name__)

is_edit = False

@app.route("/", methods=["GET", "POST"])
def open():

	global table_size

	cmp_queries = []
	order = order_by
	containing, table_size = generate_table(order=order, compare_queries=cmp_queries)
	print(table_size)

	return render_template(
		"main.html",
		curtable=current_table,
		tables=[i for i in tables_info.keys()],
		widthes=[i.width for i in tables_info[current_table]],
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
		qcount=max(1, len(cmp_queries)),
		isedit=is_edit,
		low=min((cur_page-1) * page_size + 1, table_size),
		high=min(((cur_page) * page_size), table_size),
	)


if __name__ == "__main__":
	app.run()