import sqlite3
from json import load
from tabulate import tabulate


language = input('Choose language/elige idioma (en/es): ').strip()

with open('languages.json', 'r') as f:
	lang_dict = load(f)
	lang_dict = lang_dict[language]

# Database and table creation.
con = sqlite3.connect('tasks.db')
cur = con.cursor()

try:
	cur.execute('CREATE TABLE tasks(TASK VARCHAR(100) NOT NULL, "DUE DATE" DATE, DESCRIPTION VARCHAR(300))')
	con.commit()
except:
	pass # (If table does exist, pass)


# Program itself.
while True:
	print('\n--------------------\n\t\tTO-DO\n\nPlease, choose the action you want to do:\n'
	   '1 -> Create a new task.\n'
	   '2 -> View task list.\n'
	   '0 -> Exit program.\n--------------------')
	
	match int(input()):
		case 1: # Create a new task.
			name = input('Name of new task: ')
			date = input('Due date in DD/MM/YYYY format (optional): ')
			description = input('Description (optional): ')
			data = [name, date, description]

			cur.execute('''INSERT INTO tasks
			   VALUES (?, ?, ?)
			''', data)
			con.commit()

		case 2: # View task list.
			rows = cur.execute('SELECT * FROM tasks').fetchall()
			headers = ['No.'] + [desc[0] for desc in cur.description]
			rows = [(i+1, *row) for i, row in enumerate(rows)]

			print(tabulate(rows, headers=headers, tablefmt='grid'))
					
		case 0: # Close program.
			con.close()
			print(input('End of program. Press Enter to exit.'))
			break

		case _:
			pass # Add method to report error and repeat match.

	match int(input('\n--------------------\nWhat do you want to do now?:\n'
			'1 -> Modify a task.\n'
			'2 -> Delete a task.\n'
			'3 -> View task description.\n'
			'0 -> Go to main menu.\n--------------------')):
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