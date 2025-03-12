import sqlite3
from json import load
from tabulate import tabulate


def task_list(table): # This shows task list.
	if table == 'completed':
		rows = cur.execute('SELECT * FROM completed').fetchall()
		headers = [desc[0] for desc in cur.description]
		print(tabulate(rows, headers=headers, tablefmt='grid'))
	else:
		try:
			order = int(input(lang_dict['choose_order']))
			if order not in (2, 3):
				order = 1
		except:
			order = 1
		
		rows = cur.execute(f'SELECT * FROM tasks ORDER BY {order}').fetchall()
		headers = [desc[0] for desc in cur.description]

		print(tabulate(rows, headers=headers, tablefmt='grid'))

def task_mod(lang_dict_column): # This modifies the value of the selected column of a task.
	if lang_dict_column == lang_dict["TASK_col"]:
		mod_name = input(lang_dict["mod_name"]).strip()
	elif lang_dict_column == lang_dict["DUE_DATE_col"]:
		mod_name = input(lang_dict["mod_date"]).strip()
	else:
		mod_name = input(lang_dict["mod_description"]).strip()
	
	cur.execute(f'UPDATE tasks SET "{lang_dict_column}" = ? WHERE "{lang_dict["number_col"]}" = ?', (mod_name, task_id))
	con.commit()
	print(lang_dict['task_modified'])


# Language management.
while True:
	language = input('Choose language/elige idioma (en/es): ').strip()

	with open('languages.json', 'r') as f:
		lang_dict = load(f)

		if language in lang_dict:
			lang_dict = lang_dict[language]
			break		
		else:
			print('Please, choose correct language:\nen - English\nes - Español')

print(lang_dict['chosen_lang'])


# Database and table creation/modification.
con = sqlite3.connect('tasks.db')
cur = con.cursor()

try:
	cur.execute(f'CREATE TABLE tasks("{lang_dict["number_col"]}" INT, {lang_dict["TASK_col"]} VARCHAR(100) NOT NULL, "{lang_dict["DUE_DATE_col"]}" DATE, {lang_dict["DESCRIPTION_col"]} VARCHAR(300))')
	cur.execute(f'CREATE TABLE completed("{lang_dict["number_col"]}" INT, {lang_dict["TASK_col"]} VARCHAR(100) NOT NULL, "{lang_dict["DUE_DATE_col"]}" DATE, {lang_dict["DESCRIPTION_col"]} VARCHAR(300))')
	con.commit()
except:
	try:
		cur.execute('PRAGMA table_info(tasks)')
		columns = cur.fetchall()
		names = [lang_dict['number_col'], lang_dict['TASK_col'], lang_dict['DUE_DATE_col'], lang_dict['DESCRIPTION_col']]

		for i in range(len(columns)):
			old_name = columns[i][1]
			new_name = names[i]
			
			if old_name != new_name:
				cur.execute(f'ALTER TABLE tasks RENAME COLUMN "{old_name}" TO "{new_name}"')
				cur.execute(f'ALTER TABLE completed RENAME COLUMN "{old_name}" TO "{new_name}"')
				con.commit()
	
	except Exception as e:
		print(f'Error: {e}')


# Program itself.
while True:
	match int(input(lang_dict['main_actions']).strip()):
		case 1: # Create a new task.
			id = cur.execute('SELECT COUNT(*) FROM tasks').fetchone()[0] + 1
			name = input(lang_dict['new_task']).strip()
			date = input(lang_dict['new_date']).strip()
			description = input(lang_dict['new_description']).strip()
			data = [id, name, date, description]

			cur.execute('''INSERT INTO tasks
			   VALUES (?, ?, ?, ?)
			''', data)
			con.commit()

			print(lang_dict['task_created'])

		case 2: # View task list.
			task_list('tasks')
		
		case 3: # View completed tasks.
			task_list('completed')
					
		case 0: # Close program.
			con.close()
			print(input(lang_dict['end_program']))
			break

		case _:
			continue # Back to main menu.

	match int(input(lang_dict['next_actions'])):
		case 1: # Modify a task.
			task_list('tasks')
			task_id = input(lang_dict['modify_task']).strip()
			
			if task_id == '':
				continue
			else:
				try:
					task_id = int(task_id)
				except:
					continue

			exists = cur.execute(f'SELECT EXISTS(SELECT * FROM tasks WHERE "{lang_dict["number_col"]}" = ?)', (task_id,)).fetchone()[0]
			if exists == 0: # Does not exist.
				print(lang_dict['exists_false'])
				continue
			else: # Does exist.
				match int(input(lang_dict['modify']).strip()):
					case 1: # Modify name.
						task_mod(lang_dict["TASK_col"])

					case 2: # Modify due date.
						task_mod(lang_dict["DUE_DATE_col"])

					case 3: # Modify description.
						task_mod(lang_dict["DESCRIPTION_col"])

					case _: # Cancel.
						continue

		case 2: # Delete a task.
			task_list('tasks')
			task_id = input(lang_dict['delete_task']).strip()

			if task_id == '':
				continue
			else:
				try:
					task_id = int(task_id)
				except:
					continue

			exists = cur.execute(f'SELECT EXISTS(SELECT * FROM tasks WHERE "{lang_dict["number_col"]}" = ?)', (task_id,)).fetchone()[0]
			if exists == 0: # Does not exist.
				print(lang_dict['exists_false'])
				continue
			else: # Does exist.
				confirm = input(f'{lang_dict["confirm_deletion"]}').lower().strip()

				if confirm == 'y':
					cur.execute(f'DELETE FROM tasks WHERE "{lang_dict["number_col"]}" = ?', (task_id,))
					con.commit()
					print(lang_dict['task_deleted'])
				else:
					continue
		
		case 3: # Complete a task.
			task_list('tasks')
			task_id = input(lang_dict['complete_task']).strip()

			if task_id == '':
				continue
			else:
				try:
					task_id = int(task_id)
				except:
					continue
			
			exists = cur.execute(f'SELECT EXISTS(SELECT * FROM tasks WHERE "{lang_dict["number_col"]}" = ?)', (task_id,)).fetchone()[0]
			if exists == 0: # Does not exist.
				print(lang_dict['exists_false'])
				continue
			else: # Does exist.
				cur.execute(f'''INSERT INTO completed ("{lang_dict["number_col"]}", {lang_dict["TASK_col"]}, "{lang_dict["DUE_DATE_col"]}", {lang_dict["DESCRIPTION_col"]})
				SELECT * FROM tasks WHERE "{lang_dict["number_col"]}" = ?''', (task_id,))
				cur.execute(f'DELETE FROM tasks WHERE "{lang_dict["number_col"]}" = ?', (task_id,))
				con.commit()

		case 0: # Go to main menu.
			continue

		case _:
			pass # Add method to report error and come back to match.