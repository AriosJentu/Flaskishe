import sqlite3 as db

with open("studb.db", "w") as base:
	pass

studb = db.connect("studb.db")
cursr = studb.cursor()

audiences = ["D549a", "D732", "D547", "D548", "D549", "D743", "D412/542", "D945", "D741", "D654/752", "D818", "D738", "D733a", "S", "D949"]
groups = ["B8203a", "B8203b"]
l_types = ["ПЗ", "Л", "ЛР"]
subjs = [
	"Английский язык", 
	"Дискретная математика",
	"Архитектура компьютеров",
	"Математический анализ",
	"ОСОТ",
	"Дифференциальные уравнения",
	"Физкультура",
	"Численные методы",
	"Базы данных",
	"Теория вероятностей"
]

teachers = [
	"Василенко Н.Ю.",
	"Баранов А.А.",
	"Шепелева Р.П.",
	"Клевчихин Ю.А.",
	"Колобов А.Г.",
	"Кузнецова Н.В.",
	"Лиховидов В.Н.",
	"Кленин А.С.",
	"Ефремов Е.Л.",
	"Колосова В.Е.",
	"Веремеева И.Ф."
]

shedule_dict = {

	#ID: [	ID, LESSON_ID, 	SUBJ_ID, 	AUD_ID, GRP_ID, TCHR_ID, 	TYPE_ID, 	WEEKDAY_ID	]
	1  : [	1,	1,			2,			2, 		1,		1,			2,			1			],
	2  : [	2,	2,			1,			3, 		1,		-1,			1,			1			],
	3  : [	3,	2,			1,			4, 		1,		-1,			1,			1			],
	4  : [	4,	2,			1,			15, 	1,		-1,			1,			1			],
	5  : [	5,	3,			3,			1,	 	1,		2,			3,			1			],
	6  : [	6,	4,			3,			1,	 	1,		2,			3,			1			],
	7  : [	7,	1,			9,			13,	 	1,		6,			3,			5			],
	8  : [	8,	1,			4,			6,	 	1,		9,			1,			2			],
	9  : [	9,	3,			6,			7,	 	1,		3,			1,			2			],
	10 : [	10,	2,			3,			13,	 	1,		2,			3,			5			],
	11 : [	11,	4,			6,			7,	 	1,		3,			2,			2			],
	12 : [	12,	3,			11,			9,	 	1,		7,			1,			5			],
	13 : [	13,	5,			7,			14,	 	1,		-1,			1,			2			],
	14 : [	14,	4,			11,			9,	 	1,		7,			2,			5			],
	15 : [	15,	5,			7,			14,	 	1,		-1,			1,			5			],
	16 : [	16,	2,			2,			8,	 	1,		1,			1,			3			],
	17 : [	17,	3,			4,			7,	 	1,		4,			2,			3			],
	18 : [	18,	4,			3,			12,	 	1,		8,			2,			3			],
	19 : [	19,	5,			9,			10,	 	1,		5,			2,			3			],
	20 : [	20,	1,			10,			5,	 	1,		8,			3,			4			],
	21 : [	21,	2,			10,			5,	 	1,		8,			3,			4			],
	22 : [	22,	3,			10,			11,	 	1,		8,			2,			4			],

}

subj_groups = {

	#ID: [SUBJ,	GRP	]
	1  : [1, 	1	],
	2  : [1, 	2	],
	3  : [2, 	1	],
	4  : [2, 	2	],
	5  : [3, 	1	],
	6  : [3, 	2	],
	7  : [4, 	1	],
	8  : [4, 	2	],
	9  : [5, 	1	],
	10 : [5, 	2	],
	11 : [6, 	1	],
	12 : [6, 	2	],
	13 : [7, 	1	],
	14 : [7, 	2	],
	15 : [8, 	1	],
	16 : [8, 	2	],
	17 : [9, 	1	],
	18 : [9, 	2	],
	19 : [10, 	1	],
	20 : [10, 	2	],
	21 : [11, 	1	],
	22 : [11, 	2	],
	
}

subj_teachers = {
	
	#KEY: [SUBJ,	TEACH	]
	1   : [2, 		1		],
	2   : [3, 		2		],
	3   : [3, 		8		],
	4   : [4, 		4		],
	5   : [4, 		9		],
	6   : [5, 		10		],
	7   : [6, 		3		],
	8   : [9, 		5		],
	9   : [9, 		6		],
	10  : [10, 		8		],
	11  : [11, 		7		],

}

weekdayz = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресение"]

#Audiences:
cursr.execute("CREATE TABLE `Audiences` ( `ID` INTEGER NOT NULL DEFAULT -1, `Name` TEXT )")
#Groups:
cursr.execute("CREATE TABLE `Groups` ( `ID` INTEGER NOT NULL DEFAULT -1, `Name` INTEGER )")
#Lesson Types:
cursr.execute("CREATE TABLE `LessonTypes` ( `ID` INTEGER NOT NULL, `Name` TEXT )")
#Lessons:
cursr.execute("CREATE TABLE `Lessons` ( `ID` INTEGER NOT NULL DEFAULT -1, `Name` TEXT, `OrderNumber` TEXT )")
#Shedule Items:
cursr.execute("CREATE TABLE `SchedItems` ( `ID` INTEGER NOT NULL DEFAULT -1, `LessonID` INTEGER, `SubjID` INTEGER, `AudienceID` INTEGER, `GroupID` INTEGER, `TeacherID` INTEGER, `TypeID` INTEGER, `WeekdayID` INTEGER )")
#Subjects for Group:
cursr.execute("CREATE TABLE `SubjectGroup` ( `SubjID` INTEGER, `GroupID` INTEGER )")
#Subject Teacher:
cursr.execute("CREATE TABLE `SubjectTeacher` ( `SubjID` INTEGER, `TeacherID` INTEGER )")
#Subjects:
cursr.execute("CREATE TABLE `Subjects` ( `ID` INTEGER NOT NULL DEFAULT -1, `Name` TEXT )")
#Teachers:
cursr.execute("CREATE TABLE `Teachers` ( `ID` INTEGER NOT NULL DEFAULT -1, `Name` TEXT )")
#Weekdays:
cursr.execute("CREATE TABLE `Weekdays` ( `ID` INTEGER NOT NULL DEFAULT -1, `Name` TEXT, `OrderNumber` INTEGER NOT NULL DEFAULT -1 )")


#GENERATING AUDIENCES:
for i in range(len(audiences)):
	cursr.execute("INSERT INTO Audiences VALUES (%i, '%s');"%( i+1, audiences[i] ))

#GROUPS:
for i in range(len(groups)):
	cursr.execute("INSERT INTO Groups VALUES (%i, '%s');"%( i+1, groups[i] ))

#LESSON TYPES:
for i in range(len(l_types)):
	cursr.execute("INSERT INTO LessonTypes VALUES (%i, '%s');"%( i+1, l_types[i] ))

#LESSONS:
for i in range(7):
	cursr.execute("INSERT INTO Lessons VALUES ({0}, '{0} пара', {0})".format(i+1))

#SCHEDULE ITEMS:
for _, v in shedule_dict.items():
	cursr.execute("INSERT INTO SchedItems VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(*v))

#SUBJECT GROUP:
for _, v in subj_groups.items():
	cursr.execute("INSERT INTO SubjectGroup VALUES ({}, {})".format(*v))

#SUBJECT TEACHERS:
for _, v in subj_teachers.items():
	cursr.execute("INSERT INTO SubjectTeacher VALUES ({}, {})".format(*v))

#SUBJECTS:
for i in range(len(subjs)):
	cursr.execute("INSERT INTO Subjects VALUES (%i, '%s')"%(i+1, subjs[i]))

#TEACHERS:
for i in range(len(teachers)):
	cursr.execute("INSERT INTO Teachers VALUES (%i, '%s')"%(i+1, teachers[i]))

#WEEKDAYS:
for i in range(len(weekdayz)):
	cursr.execute("INSERT INTO Weekdays VALUES (%i, '%s', %i)"%(i+1, weekdayz[i], i))


studb.commit()
studb.close()
