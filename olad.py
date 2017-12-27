from columns import tables_info
from db import *

join_column = tables_info["SchedItems"][-1] #weekday by default
join_column.ascending = None

ordering_column = tables_info["SchedItems"][1] #lessons column by default
ordering_column.ascending = None

def generate_schedule(joining_column=join_column, order_by=ordering_column):

	query = "SELECT "
	query += ", ".join([
		"(SELECT F." + i.column_val_from + 
		" FROM " + i.table_from + 
		" AS F WHERE S." + i.name + " == F." + i.column_def_val + 
		") AS N_" + i.name 
		if i.table_from != None
		else "S." + i.name + " AS N_" + i.name 
		for i in tables_info["SchedItems"]
	])
	query += " FROM SchedItems AS S "
	if joining_column.table_from:
		query += "INNER JOIN " + joining_column.table_from + " AS W "
		query += "WHERE S."+joining_column.name+" == W."+joining_column.column_def_val
		
		if not (joining_column.ascending == order_by.ascending == None): 
		
			query += " ORDER BY "
			
			if joining_column.ascending != None:

				query += "W."+joining_column.column_def_val+" "
				query += "ASC" if joining_column.ascending == True else "DESC"

			if order_by.ascending != None:
				
				if joining_column.ascending != None:
					query += ", "

				query += "S."+order_by.name
				query += " ASC" if order_by.ascending == True else " DESC"

	print()
	print(query)
	print()

	cursr.execute(query)
	fetch = cursr.fetchall()

	index = tables_info["SchedItems"].index(joining_column)
	result = {}

	for v in fetch:

		if v[index] not in result.keys():
			result[ v[index] ] = []

		result[ v[index] ].append([i for i in v if i != v[index] ])

	return result