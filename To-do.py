import gettext
import sqlite3

def select_language(language):
	localedir = 'locales'
	translation = gettext.translation('messages', localedir, languages=[language], fallback=True)
	translation.install()
	global tr
	tr = translation.gettext

language = input('Choose language/elige idioma (en/es): ').strip()
select_language(language)

con = sqlite3.connect('tasks.db')
cur = con.cursor()

try:
	cur.execute(f'CREATE TABLE tasks({tr('TASK, DUE DATE, DESCRIPTION')})')
except:
	pass # Check if this works properly - should create table if doesn't exist, else pass.


while True:
	print(tr('\n--------------------\n\t\tTO-DO\n\nPlease, choose the action you want to do:\n'
	   '1 -> Create a new task.\n'
	   '2 -> View task list.\n'
	   '0 -> Exit program.\n--------------------'))
	
	match int(input()):
		case 1: # Create a new task.
			pass
		
		case 2: # View task list.
			pass
			
			match int(input(tr('\n--------------------\nWhat do you want to do now?:\
				   1 -> Modify a task.\
				   2 -> Delete a task.\
				   3 -> View task description.\
				   0 -> Go to main menu.\n--------------------'))):
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
					
		case 0: # Close program.
			print(input(tr('End of program. Clic Enter to exit.')))
			break

		case _:
			pass # Add method to report error and come back to match.
