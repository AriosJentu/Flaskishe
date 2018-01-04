from columns import tables_info
from db import *

join_row = tables_info["SchedItems"][-1] #weekday by default for vertical
join_row.ascending = True

join_column = tables_info["SchedItems"][4] #group by default for horizontal
join_column.ascending = True

ordering_column = tables_info["SchedItems"][1] #lessons column by default
ordering_column.ascending = None

def generate_schedule(joining_column=join_column, joining_row=join_row, order_by=ordering_column):

	#---------------------------------------------------------------------------------------------------------
	#ORDERING COLUMNS
	if joining_column.table_from:
		column_query = "SELECT C."+joining_column.column_val_from + " FROM "
		column_query += joining_column.table_from + " AS C ORDER BY C." + joining_column.column_def_val
	else:
		column_query = "SELECT "+joining_column.name+" FROM SchedItems"
	if joining_column.ascending != None:
		column_query += " ASC" if joining_column.ascending == True else " DESC"

	cursr.execute(column_query)
	column_fetch = cursr.fetchall()
	columns = [i[0] for i in column_fetch]
	#print(columns)

	#ORDERING ROWS
	if joining_row.table_from:
		row_query = "SELECT R."+joining_row.column_val_from + " FROM "
		row_query += joining_row.table_from + " AS R ORDER BY R." + joining_row.column_def_val
	else:
		row_query = "SELECT "+joining_row.name+" FROM SchedItems"
	if joining_row.ascending != None:
		row_query += " ASC" if joining_row.ascending == True else " DESC"

	cursr.execute(row_query)
	row_fetch = cursr.fetchall()
	rows = [i[0] for i in row_fetch]
	#print(rows)
	#---------------------------------------------------------------------------------------------------------

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

	if order_by.ascending != None:
		query += "ORDER BY S."+order_by.name
		query += " ASC" if order_by.ascending == True else " DESC"

	cursr.execute(query)
	fetch = [list(i) for i in cursr.fetchall()]
	#print(fetch)
	#---------------------------------------------------------------------------------------------------------
	
	idx_column = tables_info["SchedItems"].index(joining_column)
	idx_row = tables_info["SchedItems"].index(joining_row)

	preresult = {column:{row:[] for row in rows} for column in columns}
	for values in fetch:
		clmn = values[idx_column]
		rw = values[idx_row]
		new_values = [i for i in values if i != clmn and i != rw]
		for row in rows:
			if row == rw:
				preresult[clmn][rw].append(new_values)
				break
		else:
			preresult[clmn][rw].append([])

	result = {}
	for row in rows:
		result[row] = []
		for col in columns:
			result[row].append(preresult[col][row])

	#print(result)

	#print(result[0][0]) #Понедельник (1й [0]) у первой группы (2й [0]) (в случае "3" - в 549й аудитории) - 

	return result, rows, columns

a, b, c = generate_schedule()
"""for i, v in a.items():
	print(i)
	for k, l in v.items():
		print(k)
		print(l)

	print()"""
#print(b)
#print(c)

"""x = list(a.values())
print(x, len(x))
for j in x:
	for i in range(len(j)):
		print(i)
		print(j[i].row)
		print(j[i].values)
		print()
print(a)"""