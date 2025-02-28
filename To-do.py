import gettext

def select_language(language):
	localedir = 'locales'
	translation = gettext.translation('messages', localedir, languages=[language], fallback=True)
	translation.install()
	global tr
	tr = translation.gettext

language = input('Choose language/elige idioma (en/es): ').strip()
select_language(language)

while True:
	print(tr('\n--------------------\n\t\tTO-DO\n\nPlease, choose the action you want to do:\n'
	   '1 -> Create a new task.\n'
	   '2 -> View task list.\n'
	   '0 -> Exit program.\n--------------------'))
	
	match int(input()):
		case 1: # Create a new task.
			with open('tasks.txt', 'a') as list:
				task_name = input(tr('Write task name: '))
				list.writelines(task_name)
				list.writelines('\t' + input(tr('Write date in DD/MM/YYYY format: ')) + '\n')
			
			print(tr(f'Task "{task_name}" has been created.'))
		
		case 2: # View task list.
			with open('tasks.txt', 'r') as list:
				print(tr('No.|TASK\t|DUE DATE'))

				iter = 0
				for task in list.readlines():
					iter += 1
					print(f'{iter}. {task}')
			
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
