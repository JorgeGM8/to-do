import sqlite3
from json import load
from tabulate import tabulate


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

print(f'{lang_dict['chosen_lang']}')


# Database and table creation/modification.
con = sqlite3.connect('tasks.db')
cur = con.cursor()

try:
	cur.execute(f'CREATE TABLE tasks({lang_dict['TASK_col']} VARCHAR(100) NOT NULL, "{lang_dict['DUE_DATE_col']}" DATE, {lang_dict['DESCRIPTION_col']} VARCHAR(300))')
	con.commit()
except:
	try:
		cur.execute('PRAGMA table_info(tasks)')
		columns = cur.fetchall()
		names = [lang_dict['TASK_col'], lang_dict['DUE_DATE_col'], lang_dict['DESCRIPTION_col']]

		for i in range(len(columns)):
			old_name = columns[i][1]
			new_name = names[i]
			
			if old_name != new_name:
				cur.execute(f'ALTER TABLE tasks RENAME COLUMN "{old_name}" TO "{new_name}"')
				con.commit()
	
	except Exception as e:
		print(f'Error: {e}')


# Program itself.
while True:
	match int(input(lang_dict['main_actions'])):
		case 1: # Create a new task.
			name = input(lang_dict['new_task'])
			date = input(lang_dict['new_date'])
			description = input(lang_dict['new_description'])
			data = [name, date, description]

			cur.execute('''INSERT INTO tasks
			   VALUES (?, ?, ?)
			''', data)
			con.commit()

			print(lang_dict['task_created'])

		case 2: # View task list.
			rows = cur.execute('SELECT * FROM tasks').fetchall()
			headers = [lang_dict['number_col']] + [desc[0] for desc in cur.description]
			rows = [(i+1, *row) for i, row in enumerate(rows)]

			print(tabulate(rows, headers=headers, tablefmt='grid'))
					
		case 0: # Close program.
			con.close()
			print(input(lang_dict['end_program']))
			break

		case _:
			pass # Add method to report error and repeat match.

	match int(input(lang_dict['next_actions'])):
		case 1: # Modify a task.
			pass

		case 2: # Delete a task.
			pass

		case 3: # View task description.
			pass

		case 0: # Go to main menu.
			continue

		case _:
			pass # Add method to report error and come back to match.