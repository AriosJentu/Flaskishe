from columns import tables_info
from db import *

current_table = "Audiences"
cur_page = 1
page_size = 10
order_by = None
compare_type = "AND"

comparison_chars = ["==", "!=", ">", "<", ">=", "<=", "LIKE", "NOT LIKE"]

class CmpExpression:

	def __init__(self, column=None, cmp_char=comparison_chars[0], value=None):
		self.column = column
		self.cmp_char = cmp_char
		self.value = value


def generate_table(table_name=current_table, page=cur_page, psize=page_size, 
	order=order_by, compare_queries=[], cmp_type=compare_type):

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
		if len(compare_queries) > 0 and compare_queries.count(-1) != len(compare_queries):
			query += "WHERE "
			query += (" " + cmp_type + " ").join(

				["N_" + k.column + " " + k.cmp_char + " ?"
				for k in compare_queries if k != -1]
			)


		
		values = tuple(
			[k.value 
			if k.cmp_char.find("LIKE") < 0 
			else "%" + k.value + "%" 
			for k in compare_queries if k != -1]
		)
		print()
		print(values)
		print(query)
		cursr.execute(query, values)
		table_size = len(cursr.fetchall())

		if order != None:

			order_type = ("ASC" if order[0] == "+" else "DESC")
			query += " ORDER BY " + order[1:]  + " " + order_type

		query += " LIMIT " + str(psize) + " OFFSET " + str(psize*(page-1))
		
		print(query)

		cursr.execute(query, values)
		table = [[j for j in i] for i in cursr.fetchall()]

		return table, table_size

def get_table_header(table_name=current_table):

	header = []
	for i in tables_info[table_name]:
		header.append(i.title)

	return header

def get_name_from_title(table_name=current_table, title="Name"):
	
	for i in tables_info[table_name]:
		if i.title == title:
			return i.name

#for i in generate_table("SchedItems", 1, 100, "+WeekdayID", {"SubjID":CmpExpression("!=", '%')}):
#	print(i)