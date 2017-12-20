from columns import tables_info
from db import *

current_table = "Audiences"
table_size = 0
cur_page = 1
page_size = 10
order_by = None
compare_type = "AND"

comparison_chars = ["==", "!=", ">", "<", ">=", "<=", "LIKE", "NOT LIKE"]

class CmpExpression:

	def __init__(self, cmp_char=comparison_chars[0], value=None):
		self.cmp_char = cmp_char
		self.value = value


def generate_table(table_name=current_table, page=cur_page, psize=page_size, 
	order=order_by, compare_queries={}):

		global table_size

		query = "SELECT "

		query += ", ".join([
			"(SELECT F." + i.column_val_from + 
			" FROM " + i.table_from + 
			" AS F WHERE S." + i.name + " == F." + i.column_def_val + 
			") AS N_" + i.name 
			if i.table_from != None
			else "S." + i.name + " AS N_" + i.name 
			for i in tables_info[table_name]
		])

		query += " FROM " + table_name + " AS S "
		if len(compare_queries) > 0:
			query += "WHERE "
			query += (" " + compare_type + " ").join(

				["N_" + k + " " + v.cmp_char + " ?"
				for k, v in compare_queries.items()]
			)


		print(query)
		
		values = tuple(
			[v.value 
			if v.cmp_char.find("LIKE") < 0 
			else "%" + v.value + "%" 
			for _, v in compare_queries.items()
			]
		)
		
		cursr.execute(query, values)
		table_size = len(cursr.fetchall())

		if order != None:

			order_type = ("ASC" if order[0] == "+" else "DESC")
			query += " ORDER BY " + order[1:]  + " " + order_type

		query += " LIMIT " + str(psize) + " OFFSET " + str(psize*(page-1))
		cursr.execute(query, values)
		table = [[j for j in i] for i in cursr.fetchall()]

		return table

def get_table_header(table_name=current_table):

	header = []
	for i in tables_info[table_name]:
		header.append(i.title)

	return header

def get_name_from_title(table_name=current_table, title="Name"):
	
	for i in tables_info[table_name]:
		if i.title == title:
			return i.name



for i in generate_table("SchedItems", 1, 100, "+WeekdayID", {"SubjID":CmpExpression("NOT LIKE", "Анг")}):
	print(i)