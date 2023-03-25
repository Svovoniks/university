def second(rep, line):

	mx_len = min(rep+1, len(line))

	mx = {}
	# mx: char: [total_rep, replaced[], seen[]]

	for i in range(len(line)):
		if line[i] not in mx:
			mx.update({line[i]: [0, [], [i]]})
			continue

		dist = i - mx[line[i]][2][-1] - 1

		mx[line[i]][2].append(i)
		mx[line[i]][1].append(dist)
		mx[line[i]][0] += dist
		for j in range(len(mx[line[i]][1])):
			if mx[line[i]][0] > rep:
				mx[line[i]][0] -= mx[line[i]][1].pop(0)
				mx[line[i]][2].pop(0)
			else:
				
				break

		if len(mx[line[i]][2]) >= 2:
			mx_len = max(mx_len, min(len(line), mx[line[i]][2][-1] - mx[line[i]][2][0] + 1 + rep - mx[line[i]][0]))

	return mx_len


def first(rep, line):
	mx_len = 0
	pr_len = 0
	mx_row = 0
	row = 1
	for i in range(len(line)):
		ln = 1
		rp = 0

		if line[i] == line[i-1] and i > 0:
			row += 1
			mx_len = max(mx_len, pr_len+1)
		else:
			mx_row = max(row, mx_row)
			row = 1
		for j in range(i-1, -1, -1):
			ln += 1
			if line[j] != line[i]:
				rp += 1
				if rp > rep:
					ln -= 1
					break
		pr_len = ln
		mx_len = max(mx_len, ln)

	if len(line) >= mx_row+rep:
		mx_len = max(mx_len, mx_row+rep)

	return mx_len

def test():
	from random import randint, choices
	for i in range(50):
		rep = randint(1, 40)
		line = ''.join(choices('qwertyuiopasdfghjklzxcvbnm', k=10))
		f = first(rep, line)
		s = second(rep, line)
		print(rep, line, f == s, f, s, f>=s)
		if f!=s:
			break

# print(*text1.split('\n\n'), sep='\n"""""\n\n\n""""""\n')
# day, subj, time_s, time_e, prof, room, week
# 0     1    2        3       4    5     6
def parse(text, week):
	ls = []
	cur_day = ''
	for i in text.split('\n\n'):
		t = i.strip('\n')
		if t[1] != '.':
			cur_day = t.split(' ', 1)[0]
			t = t.split('\n', 1)[1]

		if '<Нет пары>' not in t:
			tls = t.split('\n')
			# print(tls)
			ls.append([
				cur_day, 
				tls[1] + ' (' + tls[3][:tls[3].index('(')-1] + ')', 
				*tls[0].split(' ')[1::2], 
				tls[2], 
				tls[3][tls[3].index('.)')+5:],
				str(week)])

	return ls

def surround(st):
	rx = r'\d+'
	for i in range(len(st)):
		if re.fullmatch(rx, st[i]):
			continue
		st[i] = "'" + st[i] + "'"
	return st

def make_query(table, args, values, selector):
	new_line = '\n'
	start = f'INSERT INTO bot.{table} ({", ".join(args)}) VALUES\n{(", "+new_line).join("({})".format(", ".join(surround(selector(i)))) for i in values)};'
	print(start)

def unicque(l, idx):
	nls = []
	keys = []
	for i in range(len(l)):

		if l[i][idx] not in keys:
			nls.append(l[i])
			keys.append(l[i][idx])

	return nls

import copy, re

def find_key(ls, idx, key):
	for i in range(len(ls)):
		if ls[i][idx] == key:
			return str(i+1)
	return -1

def get_script():
	text1 = '''
ПОНЕДЕЛЬНИК - 6 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
Высшая математика 
Шаймарданова Л. К.
Лекция (до 16 нед.) в 514 (ОП)

3. 13:10 - 14:45
Иностранный язык 
Воронова Е. В.
Практика (до 14 нед.) в 324 (ОП)

4. 15:25 - 17:00
История 
Скляр Л. Н.
Практика (до 18 нед.) в 318 (ОП)

5. 17:15 - 18:50
Высшая математика 
Шаймарданова Л. К.
Практика (до 16 нед.) в 301 (ОП)


ВТОРНИК - 7 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
<Нет пары>

3. 13:10 - 14:45
<Нет пары>

4. 15:25 - 17:00
<Нет пары>

5. 17:15 - 18:50
<Нет пары>


СРЕДА - 8 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
Игровые виды спорта 
Волохова С. В.
Практика (до 16 нед.) в спортзале (А)

3. 13:10 - 14:45
Основы DevOps 
Городничев М. Г.
Лекция (до 16 нед.) в А-414 (А)

4. 15:25 - 17:00
<Нет пары>

5. 17:15 - 18:50
<Нет пары>


ЧЕТВЕРГ - 9 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
Физика 
Дегтярёв В. Ф.
Практика (до 18 нед.) в 332б (ОП)

3. 13:10 - 14:45
Математические основы баз данных 
Полищук Ю. В.
Практика (до 16 нед.) в 404 (ОП)

4. 15:25 - 17:00
Игровые виды спорта 
Волохова С. В.
Практика (до 16 нед.) в спортзале (ОП)

5. 17:15 - 18:50
<Нет пары>


ПЯТНИЦА - 10 марта
1. 09:30 - 11:05
Основы DevOps 
Липатов В. Н.
Лаб. занятие (до 16 нед.) в ВЦ-302 (А)

2. 11:20 - 12:55
Введение в информационные технологии 
Фурлетов Ю. М.
Лаб. занятие (до 16 нед.) в Л-207 (А)

3. 13:10 - 14:45
<Нет пары>

4. 15:25 - 17:00
<Нет пары>

5. 17:15 - 18:50
<Нет пары>


СУББОТА - 11 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
<Нет пары>

3. 13:10 - 14:45
<Нет пары>

4. 15:25 - 17:00
<Нет пары>

5. 17:15 - 18:50
<Нет пары>
'''.replace('спортзале', 'спортзал')

	text2 = '''
ПОНЕДЕЛЬНИК - 27 февр.
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
<Нет пары>

3. 13:10 - 14:45
Введение в информационные технологии 
Фурлетов Ю. М.
Лаб. занятие (3 - 17 нед.) в Л-203 (А)

4. 15:25 - 17:00
Игровые виды спорта 
Волохова С. В.
Практика (3 - 17 нед.) в спортзале (А)

5. 17:15 - 18:50
<Нет пары>


ВТОРНИК - 28 февр.
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
Введение в информационные технологии 
Фурлетов Ю. М.
Практика (1 - 15 нед.) в Л-206 (А)

3. 13:10 - 14:45
Основы DevOps 
Липатов В. Н.
Лаб. занятие (1 - 15 нед.) в ВЦ-302 (А)

4. 15:25 - 17:00
Проектный практикум 
Потапченко Т. Д.
Практика (1 - 15 нед.) в Л-205 (А)

5. 17:15 - 18:50
Игровые виды спорта 
Волохова С. В.
Практика (1 - 17 нед.) в спортзале (А)


СРЕДА - 1 марта
1. 09:30 - 11:05
Иностранный язык 
Воронова Е. В.
Практика (1 - 15 нед.) в 314 (ОП)

2. 11:20 - 12:55
Высшая математика 
Шаймарданова Л. К.
Практика (3 - 17 нед.) в 301 (ОП)

3. 13:10 - 14:45
Высшая математика 
Шаймарданова Л. К.
Лекция (1 - 17 нед.) в 514 (ОП)

4. 15:25 - 17:00
Физика 
Вальковский С. Н.
Лекция (1 - 17 нед.) в 226 (ОП)

5. 17:15 - 18:50
<Нет пары>


ЧЕТВЕРГ - 2 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
<Нет пары>

3. 13:10 - 14:45
<Нет пары>

4. 15:25 - 17:00
<Нет пары>

5. 17:15 - 18:50
<Нет пары>


ПЯТНИЦА - 3 марта
1. 09:30 - 11:05
История 
Скляр Л. Н.
Лекция (1 - 17 нед.) в 227 (ОП)

2. 11:20 - 12:55
Математические основы баз данных 
Полищук Ю. В.
Лекция (1 - 15 нед.) в 535 (ОП)

3. 13:10 - 14:45
Физика 
Тимошина М. И.
Лаб. занятие (1 - 17 нед.) в 340 (ОП)

4. 15:25 - 17:00
История 
Скляр Л. Н.
Практика (1 - 17 нед.) в 318 (ОП)

5. 17:15 - 18:50
Математические основы баз данных 
Изотова А. А.
Лаб. занятие (1 - 15 нед.) в 131 (ОП)


СУББОТА - 4 марта
1. 09:30 - 11:05
<Нет пары>

2. 11:20 - 12:55
<Нет пары>

3. 13:10 - 14:45
<Нет пары>

4. 15:25 - 17:00
<Нет пары>

5. 17:15 - 18:50
<Нет пары>
'''.replace('спортзале', 'спортзал')

	ls = parse(text1, 0)
	ls = ls + parse(text2, 1)
	# print(*parse(text2, 2), sep='\n')

	subj_ls = unicque([[ls[i][1]] for i in range(len(ls))], 0)
	make_query('subject', ['name'], copy.deepcopy(subj_ls), lambda a: a)
	print()

	make_query('teacher', ['full_name', 'subject'], unicque([[ls[i][4], find_key(subj_ls, 0, ls[i][1])] for i in range(len(ls))], 1), lambda a: a)
	print()

	make_query('timetable',
	 ['day','subject', 'start_time', 'end_time', 'room_numb', 'week'],
	 [[ls[i][0], find_key(subj_ls, 0, ls[i][1]), *ls[i][2:]] for i in range(len(ls))],
	 lambda a: [a[i] for i in list(range(4)) + list(range(5, 7))])




	# with open('table.pdr', 'wb') as file:
	# 	file.write(rq.get(r'https://mtuci.ru/upload/iblock/bdc/vii2s3gy9t889t83jucvzxba1dqp747k/BVT2204.pdf').content)

get_script()