from db import *
from columns import *

def is_id_in_table(table):
	for i in tables_info[table]:
		if i.name == "ID":
			return True
	else:
		return False

def get_real_values(table, values):

	new_vals = []
	for k in range(len(values)):
		clmn = tables_info[table][k]
		if clmn.table_from != None:
			
			query = "SELECT " +clmn.column_def_val+ " FROM " + clmn.table_from
			query += " WHERE " + clmn.column_val_from + " == ?"
			
			print(query, values[k])
			
			cursr.execute(query, (values[k], ) )
			new_vals.append(cursr.fetchall()[0][0])

		else:
			new_vals.append(values[k])

	return new_vals

def get_list_values_of_column(table, column):

	vals = []
	for i in tables_info[table]:
		if i.table_from != None and i.name == column:
			query = "SELECT " + i.column_val_from + " FROM " + i.table_from
			print(query)
			cursr.execute(query)
			vals = [i[0] for i in cursr.fetchall()]
			print(vals)

			return vals
	else:
		return False



def next_id(table):
	cursr.execute("SELECT Max(ID) FROM "+table)
	return cursr.fetchall()[0][0] + 1

def add_record(table, values): #values - list without id

	if is_id_in_table(table):
		values = [next_id(table)] + values

	query = "INSERT INTO " + table + " VALUES" 
	query += "("+", ".join(["?" for _ in values]) + ")"
	print(query)
	print(get_real_values(table, values))
	cursr.execute(query, tuple(get_real_values(table, values)))

	#studb.commit()

def remove_record(table, values): 
	#values = dict; key - column, value - what key equal
	
	query = "DELETE FROM "+table+" WHERE " + " AND ".join(
		[ 
			k + " == ?"
			for k in values.keys()
		]
	)
	print(query)
	cursr.execute(query, tuple([v for v in values.values()]))

	#studb.commit()

def update_record(table, upd_from, upd_to):

	query = "UPDATE " + table + " SET " + ", ".join(
		[
			j + " == ?" 
			for j in upd_to.keys()
		]
	) + " WHERE " + " AND ".join(
		[
			j + " == ?"
			for j in upd_from.keys()
		]
	)
	print(query)
	print(get_real_values(table, [v for v in upd_to.values()]) +
			get_real_values(table, [v for v in upd_from.values()]))

	cursr.execute(query, tuple(
			get_real_values(table, [v for v in upd_to.values()]) +
			get_real_values(table, [v for v in upd_from.values()])
		)
	)
	
	#studb.commit()
