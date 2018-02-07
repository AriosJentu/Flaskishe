class Column:

	def __init__(self, table_from=None, column_def_val=None, 
		column_val_from=None, name="Name", title="Title", width=100):
		
			self.table_from = table_from
			self.column_def_val = column_def_val
			self.column_val_from = column_val_from
			self.name = name
			self.width = width
			self.title = title

tables_info = {
	"Audiences": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="Аудитория", width=90)
	],

	"Groups": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="Группа", width=90)
	],

	"LessonTypes": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="Тип", width=90)
	],

	"Lessons": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="Номер", width=80),
		Column(name="OrderNumber", title="Порядок", width=50)
	],

	"SubjectGroup": [
		Column(name="SubjID", title="Предмет", width=150, table_from="Subjects", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="GroupID", title="Группа", width=100, table_from="Groups", 
			column_def_val="ID", column_val_from="Name")
	],

	"SubjectTeacher": [
		Column(name="SubjID", title="Предмет", width=150, table_from="Subjects", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="TeacherID", title="Преподаватель", width=150, 
			table_from="Teachers", column_def_val="ID", column_val_from="Name")
	],

	"Subjects": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="Предмет", width=150)
	],

	"Teachers": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="Преподаватель", width=150)		
	],

	"Weekdays": [
		Column(name="ID", title="ID", width=50),
		Column(name="Name", title="День Недели", width=80),
		Column(name="OrderNumber", title="Порядок", width=50)
	],

	"SchedItems": [
		Column(name="ID", title="ID", width=50),

		Column(name="LessonID", title="Пара", width=50, table_from="Lessons", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="SubjID", title="Предмет", width=150, table_from="Subjects", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="AudienceID", title="Аудитория", width=90, 
			table_from="Audiences", column_def_val="ID", 
			column_val_from="Name"),

		Column(name="GroupID", title="Группа", width=80, table_from="Groups", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="TeacherID", title="Преподаватель", width=150, 
			table_from="Teachers", column_def_val="ID", column_val_from="Name"),

		Column(name="TypeID", title="Тип", width=50, table_from="LessonTypes", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="WeekdayID", title="День Недели", width=100, 
			table_from="Weekdays", column_def_val="ID", column_val_from="Name"),
	],
	"SchedItemsCnf": [
		Column(name="ID", title="ID", width=50),

		Column(name="LessonID", title="Пара", width=50, table_from="Lessons", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="SubjID", title="Предмет", width=150, table_from="Subjects", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="AudienceID", title="Аудитория", width=90, 
			table_from="Audiences", column_def_val="ID", 
			column_val_from="Name"),

		Column(name="GroupID", title="Группа", width=80, table_from="Groups", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="TeacherID", title="Преподаватель", width=150, 
			table_from="Teachers", column_def_val="ID", column_val_from="Name"),

		Column(name="TypeID", title="Тип", width=50, table_from="LessonTypes", 
			column_def_val="ID", column_val_from="Name"),

		Column(name="WeekdayID", title="День Недели", width=100, 
			table_from="Weekdays", column_def_val="ID", column_val_from="Name"),
	]

}