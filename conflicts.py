from random import randint
from db import *
from columns import *

wdcnt = 7
def get_schedule_conflicts(values):

	teacher_time = {}
	audience_time = {}
	group_time = {}

	conflicts = []
	for i in values:

		value_id = i[0]
		teacher_id = i[5]
		lesson_id = (i[1]*wdcnt) + i[7] #lesson*count_of_weekdays + weekday
		audience_id = i[3]
		group_id = i[4]

		#print(lesson_id, group_id, audience_id, teacher_id)
		if teacher_id == 12:
			teacher_id = randint(10000, 20000)

		pair_t_t = (teacher_id, lesson_id)
		pair_a_t = (audience_id, lesson_id)
		pair_g_t = (group_id, lesson_id)
		pair_a_g = (audience_id, group_id)

		if pair_t_t in teacher_time.keys():
			teacher_time[pair_t_t].append(value_id)
			conflicts.append((value_id, "Этот преподаватель в это время занят"))
		else:
			teacher_time[pair_t_t] = [value_id]

		if pair_a_t in audience_time.keys():
			audience_time[pair_a_t].append(value_id)
			conflicts.append((value_id, "Эта аудитория в это время занята"))
		else:
			audience_time[pair_a_t] = [value_id]

		if pair_g_t in group_time.keys() and teacher_id < 10000:
			group_time[pair_g_t].append(value_id)
			conflicts.append((value_id, "Эта группа в это время занята"))
		else:
			group_time[pair_g_t] = [value_id]

	#print()
	#print(conflicts)
	for i, v in teacher_time.items():
		if len(v) > 1:
			conflicts.append((v[0], "Этот преподаватель в это время занят"))
				
	for i, v in audience_time.items():
		if len(v) > 1:
			conflicts.append((v[0], "Эта аудитория в это время занята"))
				
	for i, v in group_time.items():
		if len(v) > 1:
			conflicts.append((v[0], "Эта группа в это время занята"))


	#print(teacher_time.values())
	#print(audience_time.values())
	#print(group_time.values())
	
	return conflicts

	