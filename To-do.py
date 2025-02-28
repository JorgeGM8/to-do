while True:
	print('\n--------------------\n\t\tTO-DO\n\nPor favor, indica la acción que quieres realizar:\n'
	   '1 -> Crear una tarea.\n'
	   '2 -> Ver lista de tareas.\n'
	   '0 -> Salir del programa.\n--------------------')
	
	match int(input()):
		case 1: # Crear una tarea.
			with open('tareas.txt', 'a') as lista:
				nombre_tarea = input('Escribe el nombre de la tarea: ')
				lista.writelines(nombre_tarea)
				lista.writelines('\t' + input('Escribe la fecha en formato DD/MM/AAAA: ') + '\n')
			
			print(f'La tarea "{nombre_tarea}" ha sido creada.')
		
		case 2: # Ver la lista de tareas.
			with open('tareas.txt', 'r') as lista:
				print('Nº|TAREA\t|FECHA LÍMITE')

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
