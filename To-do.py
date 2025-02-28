import gettext

def select_language(language):
	localedir = 'locales'
	gettext.translation('messages', localedir, languages=[language], fallback=True).install()
	global tr
	tr = gettext.gettext

laguage = input('Choose language/elige idioma (en/es): ').strip()
select_language(language)

while True:
	print('\n--------------------\n\t\tTO-DO\n\nPlease, choose the action you want to do:\n'
	   '1 -> Create a new task.\n'
	   '2 -> View task list.\n'
	   '0 -> Exit program.\n--------------------')
	
	match int(input()):
		case 1: # Create a new task.
			with open('tasks.txt', 'a') as lista:
				nombre_tarea = input('Write task name: ')
				lista.writelines(nombre_tarea)
				lista.writelines('\t' + input('Write date in DD/MM/YYYY format: ') + '\n')
			
			print(f'Task "{nombre_tarea}" has been created.')
		
		case 2: # Ver la lista de tareas.
			with open('tasks.txt', 'r') as lista:
				print('No.|TASK\t|DUE DATE')

				iteracion = 0
				for tarea in lista.readlines():
					iteracion += 1
					print(f'{iteracion}. {tarea}')
			
			match int(input('\n--------------------\n¿Qué deseas hacer ahora?:\
				   1 -> Modificar una tarea.\
				   2 -> Eliminar una tarea.\
				   3 -> Ver la descripción de una tarea.\
				   0 -> Volver al menú principal.\n--------------------')):
				case 1: # Modificar una tarea.
					pass

				case 2: # Eliminar una tarea.
					pass

				case 3: # Ver la descripción de una tarea.
					pass

				case 0: # Volver al menú principal.
					continue

				case _:
					pass # Añadir método para mostrar error y repetir match.
					
		
		case 0: # Cerrar el programa.
			print('Fin del programa.')
			break

		case _:
			pass # Añadir método para mostrar error y repetir match.
