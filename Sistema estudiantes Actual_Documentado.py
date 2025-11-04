import csv 
import os

# Ruta base donde se guardarán todos los archivos CSV
RUTA_BASE_CSV = r"C:\Users\dafet\Desktop\Proyecto Poo"

# ============================================================
# CLASE GESTORCSV
# Encargada de manejar toda la lectura y escritura en archivos CSV
# ============================================================

class GestorCSV:
    @staticmethod
    def guardar_datos_csv(nombre_archivo, encabezados, datos, ruta_guardado=RUTA_BASE_CSV):
        # Construye la ruta completa del archivo CSV
        ruta_completa_archivo = os.path.join(ruta_guardado, nombre_archivo)

        # Verifica si la carpeta base existe, y si no, la crea
        if not os.path.exists(ruta_guardado):
            try:
                os.makedirs(ruta_guardado, exist_ok=True)
                print(f" Directorio creado: '{ruta_guardado}'")
            except Exception as e:
                print(f" Error al crear el directorio '{ruta_guardado}': {e}")
                return
        
        # Intenta escribir los datos en el archivo CSV (modo escritura 'w')
        try:
            with open(ruta_completa_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
                escritor = csv.writer(archivo_csv)
                escritor.writerow(encabezados)   # Escribe la fila de encabezados
                escritor.writerows(datos)        # Escribe todas las filas de datos

            print(f"\n Datos exportados a: '{ruta_completa_archivo}'")
            return True

        except Exception as e:
            print(f"\n Ocurrió un error al escribir el archivo: {e}")
            return False


    @staticmethod
    def añadir_datos_csv(nombre_archivo, encabezados, datos, ruta_guardado=RUTA_BASE_CSV):
        # Crea la ruta completa del archivo
        ruta_completa_archivo = os.path.join(ruta_guardado, nombre_archivo)

        # Crea el directorio si no existe
        if not os.path.exists(ruta_guardado):
            try:
                os.makedirs(ruta_guardado, exist_ok=True)
                print(f" Directorio creado: '{ruta_guardado}'")
            except Exception as e:
                print(f" Error al crear el directorio '{ruta_guardado}': {e}")
                return False

        # Verifica si el archivo ya existe
        archivo_existe = os.path.exists(ruta_completa_archivo)

        try:
            # Abre el archivo en modo 'append' para añadir sin sobrescribir
            with open(ruta_completa_archivo, mode='a', newline='', encoding='utf-8') as archivo_csv:
                escritor = csv.writer(archivo_csv)

                # Si el archivo no existía, escribe primero los encabezados
                if not archivo_existe:
                    escritor.writerow(encabezados)

                # Añade las nuevas filas
                escritor.writerows(datos)

            print(f"\n Datos añadidos a: '{ruta_completa_archivo}'")
            return True

        except Exception as e:
            print(f"\n Ocurrió un error al escribir el archivo: {e}")
            return False 
        

    @staticmethod
    def leer_csv(nombre_archivo, ruta_guardado=RUTA_BASE_CSV):
        # Permite leer el contenido de un archivo CSV y devolverlo como lista
        ruta_completa = os.path.join(ruta_guardado, nombre_archivo)
        if not os.path.exists(ruta_completa):
            print(f"El archivo {nombre_archivo} no existe.")
            return []
        with open(ruta_completa, newline='', encoding='utf-8') as f:
            lector = csv.reader(f)
            next(lector, None)  # Salta la fila de encabezados
            return list(lector)


# ============================================================
# CLASE PERSONA
# Clase base que define los atributos y métodos comunes
# ============================================================

class Persona:
    def __init__(self, id="", nombre="", edad="", direccion="", email="", fecha_nacimiento=""):
        # Atributos básicos de cualquier persona
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.direccion = direccion
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento

    # Método para solicitar los datos personales de forma interactiva
    def solicitar_datos_persona(self):
        campos = ["id", "nombre", "edad", "direccion", "email", "fecha_nacimiento"]
        datos = []
        for campo in campos:
            valor = input(f"Ingrese {campo}: ").strip()
            # Valida que el campo no esté vacío
            while not valor:
                valor = input(f"El {campo} no puede estar vacío, ingrese nuevamente: ").strip()
            datos.append(valor)
        return datos


# ============================================================
# CLASE ESTUDIANTE (hereda de Persona)
# Permite registrar y guardar estudiantes
# ============================================================

class Estudiante(Persona):
    def __init__(self):
        super().__init__()   # Llama al constructor de Persona
        self.registro = []   # Lista para almacenar los estudiantes registrados

    def agregar_estudiante(self):
        print('--------------------------------------')

        # Solicita cuántos registros se desean ingresar
        while True:
            try:
                n = int(input("¿Cuántos registros deseas ingresar? "))
                if n <= 0:
                    print(" Debes ingresar al menos un registro.")
                else:
                    break
            except ValueError:
                print(" Por favor ingrese un número válido.")

        # Ingreso de los datos de cada estudiante
        for i in range(n):
            print(f"\nRegistro {i+1}:")
            datos = self.solicitar_datos_persona()  # Usa método heredado
            self.registro.append(datos)

        # Muestra los estudiantes registrados en pantalla
        print("\nESTUDIANTES REGISTRADOS:")
        for e in self.registro:
            print(f"ID: {e[0]} | Nombre: {e[1]} | Edad: {e[2]} | Email: {e[4]}")

        # Guarda los datos en un archivo CSV
        encabezados = ["Id", "Nombre", "Edad", "Direccion", "Email", "Fecha_nacimiento"]
        GestorCSV.añadir_datos_csv(
            nombre_archivo="estudiantes.csv", 
            encabezados=encabezados, 
            datos=self.registro
        )

    # Devuelve la lista actual de estudiantes registrados
    def obtener_estudiantes(self):
        return self.registro
    
    #buscar id de persona para sistema de biblioteca
    def buscar_estudiante(self,id_buscar):
        for estudiante in self.registro:
            if estudiante[0] == id_buscar:
                return estudiante
        return None
    


# ============================================================
# CLASE DOCENTE (hereda de Persona)
# Permite registrar y guardar docentes
# ============================================================

class Docente(Persona):
    def __init__(self):
        super().__init__()  # Inicializa los atributos de Persona
        self.registro = []  # Lista de docentes registrados

    def agregar_docente(self):
        print('--------------------------------------')
        # Solicita cuántos registros se van a ingresar
        while True:
            try:
                n = int(input("¿Cuántos registros deseas ingresar? "))
                if n <= 0:
                    print(" Debes ingresar al menos un registro.")
                else:
                    break
            except ValueError:
                print(" Por favor ingrese un número válido.")

        # Registro de cada docente
        for i in range(n):
            print(f"\nRegistro {i+1}:")
            datos = self.solicitar_datos_persona()  # Usa el método heredado
            self.registro.append(datos)

        # Muestra en pantalla los docentes agregados
        print("\n DOCENTES REGISTRADOS:")
        for d in self.registro:
            print(f"ID: {d[0]} | Nombre: {d[1]} | Edad: {d[2]} | Email: {d[4]}")

        # Guarda los docentes en archivo CSV
        encabezados = ["Id", "Nombre", "Edad", "Direccion", "Email", "Fecha_nacimiento"]
        GestorCSV.añadir_datos_csv(
            nombre_archivo="docentes.csv",
            encabezados=encabezados,
            datos=self.registro
        )

    # Devuelve la lista actual de docentes
    def obtener_docentes(self):
        return self.registro


# ============================================================
# CLASE MATERIA
# Gestiona la asignación de materias a docentes
# ============================================================

class Materia:
    def __init__(self):
        self.lista_docentes = []        # Lista recibida desde la clase Docente
        self.lista_estudiantes = []     # Lista recibida desde la clase Estudiante
        self.materias_asignadas = []    # Guarda relaciones docente-materia
        self.materias_estudiantes = []  # Guarda relaciones estudiante-materia

    # Recibir listas desde otras clases
    def recibir_docentes(self, lista_docentes):
        self.lista_docentes = lista_docentes

    def recibir_estudiantes(self, lista_estudiantes):
        self.lista_estudiantes = lista_estudiantes

    # Asignar materia a un docente
    def inscribir_materia_docente(self):
        if not self.lista_docentes:
            print("\n No hay docentes registrados aún. Agrega docentes antes de inscribir materias.\n")
            return

        print("\n Lista de docentes disponibles:\n")
        for docente in self.lista_docentes:
            print(f"ID: {docente[0]} - Nombre: {docente[1]} - Email: {docente[4]}")

        print("--------------------------------------")
        id_docente = input("Digite el id del docente al que le quiere inscribir materias: ")

        docente_encontrado = None

        for docente in self.lista_docentes:
            if docente[0] == id_docente:
                docente_encontrado = docente
                break

        if not docente_encontrado:
            print(f"No se encontró el docente con el id: {id_docente}")
            return

        nombre_materia = input("Digite el nombre de la materia: ")

        inscripcion_materias = [docente_encontrado[0], docente_encontrado[1], nombre_materia]
        self.materias_asignadas.append(inscripcion_materias)

        print(f"\nLa materia '{nombre_materia}' ha sido asignada correctamente al docente: {docente_encontrado[1]} (ID: {docente_encontrado[0]}).\n")

        print("Listado de materias asignadas a docentes:\n")
        for m in self.materias_asignadas:
            print(f"Docente: {m[1]} - Materia: {m[2]}")

        # Guarda los datos en un archivo CSV
        encabezados = ["Id", "Nombre", "Materia"]
        GestorCSV.añadir_datos_csv(
            nombre_archivo="inscribir_materia_docente.csv", 
            encabezados=encabezados, 
            datos=self.materias_asignadas
        )

    # Inscribir estudiante en una materia
    def inscribir_estudiante_materia(self):
        if not self.lista_estudiantes:
            print("\n No hay estudiantes registrados aún. Agrega estudiantes antes de inscribirlos en materias.\n")
            return

        if not self.materias_asignadas:
            print("\n No hay materias disponibles aún. Asigna materias a docentes antes de inscribir estudiantes.\n")
            return

        print("\n Lista de estudiantes disponibles:\n")
        for estudiante in self.lista_estudiantes:
            print(f"ID: {estudiante[0]} - Nombre: {estudiante[1]} - Email: {estudiante[4]}")

        id_estudiante = input("\nDigite el id del estudiante que desea inscribir: ")
        estudiante_encontrado = None

        for estudiante in self.lista_estudiantes:
            if estudiante[0] == id_estudiante:
                estudiante_encontrado = estudiante
                break

        if not estudiante_encontrado:
            print(f"No se encontró el estudiante con el id: {id_estudiante}")
            return

        print("\n Materias disponibles:\n")
        for m in self.materias_asignadas:
            print(f"{m[2]} - Docente: {m[1]} (ID: {m[0]})")

        nombre_materia = input("\nDigite el nombre de la materia a la que desea inscribir al estudiante: ")

        materia_encontrada = None
        for m in self.materias_asignadas:
            if m[2].lower() == nombre_materia.lower():
                materia_encontrada = m
                break

        if not materia_encontrada:
            print(f"No se encontró la materia '{nombre_materia}'.")
            return

        inscripcion_estudiante = [estudiante_encontrado[0], estudiante_encontrado[1], materia_encontrada[2]]
        self.materias_estudiantes.append(inscripcion_estudiante)

        print(f"\nEl estudiante '{estudiante_encontrado[1]}' ha sido inscrito correctamente en la materia '{materia_encontrada[2]}'.\n")

        print("Listado de inscripciones de estudiantes:\n")
        for ins in self.materias_estudiantes:
            print(f"Estudiante: {ins[1]} - Materia: {ins[2]}")
        # Guarda los datos en un archivo CSV
        encabezados = ["Id", "Nombre", "Materia"]
        GestorCSV.añadir_datos_csv(
            nombre_archivo="inscribir_materia_estudiante.csv", 
            encabezados=encabezados, 
            datos=self.materias_estudiantes
        )
    def obtener_materia_estudiantes(self):
        return self.materias_estudiantes

# ============================================================
# CLASE ACTIVIDAD
# Permite registrar actividades asociadas a una persona (docente o estudiante)
# ============================================================

class Actividad:
    def __init__(self):
        self.actividades = []  # Lista donde se guardarán las actividades registradas

    def agregar_actividad(self):
        print("-------------------------------------")

        # Solicita los datos de la persona a la que se asocia la actividad
        print("\n--- Datos de la persona asociada ---")
        id_persona = input("ID de la persona: ").strip()
        while not id_persona:
            id_persona = input("El ID no puede estar vacío: ").strip()

        nombre_persona = input("Nombre de la persona: ").strip()
        while not nombre_persona:
            nombre_persona = input("El nombre no puede estar vacío: ").strip()

        email_persona = input("Email de la persona: ").strip()
        while not email_persona:
            email_persona = input("El email no puede estar vacío: ").strip()

        # Solicita cuántas actividades se desean registrar
        while True:
            try:
                n = int(input("\n¿Cuántas actividades deseas registrar? "))
                if n <= 0:
                    print(" Debes ingresar al menos una actividad.")
                else:
                    break
            except ValueError:
                print(" Por favor ingresa un número válido.")

        # Registro de cada actividad
        for i in range(n):
            print(f"\nRegistro de actividad {i+1}:")
            id_actividad = input("ID de la actividad: ").strip()
            while not id_actividad:
                id_actividad = input("El ID no puede estar vacío: ").strip()

            tipo_actividad = input("Tipo de actividad (Futbol,Lectura,Baile): ").strip()
            while not tipo_actividad:
                tipo_actividad = input("El tipo no puede estar vacío: ").strip()

            descripcion = input("Descripción (opcional): ").strip() or "Sin descripción"

            # Guarda la actividad asociada a la persona
            self.actividades.append([
                id_actividad,
                tipo_actividad,
                descripcion,
                id_persona,
                nombre_persona,
                email_persona
            ])

        # Muestra en pantalla todas las actividades registradas
        print("\nACTIVIDADES REGISTRADAS:")
        for act in self.actividades:
            print(f"Actividad: {act[1]} -- Tipo: {act[2]} -- Persona: {act[4]}")

        # Guarda las actividades en un archivo CSV
        encabezados = ["id_actividad", "tipo_actividad", "descripcion", "id_persona", "nombre_persona", "email_persona"]
        GestorCSV.añadir_datos_csv(
            nombre_archivo="actividades.csv", 
            encabezados=encabezados, 
            datos=self.actividades
        )

class Notas:
    def __init__(self):
        self.lista_estudiantes_materias = []  # Se recibe desde Materia

    def recibir_estudiantes(self, lista_estudiantes_materias):
        self.lista_estudiantes_materias = lista_estudiantes_materias

    def agregar_notas_estudiantes(self):
        if not self.lista_estudiantes_materias:
            print("\nNo hay estudiantes inscritos en materias.\n")
            return

        print("\nEstudiantes inscritos en materias disponibles:\n")
        for registro in self.lista_estudiantes_materias:
            print(f"ID: {registro[0]} - Nombre: {registro[1]} - Materia: {registro[2]}")

        id_est = input("\nDigite el ID del estudiante: ").strip()
        materia_nombre = input("Digite el nombre de la materia: ").strip()

        registro_encontrado = None
        for registro in self.lista_estudiantes_materias:
            if registro[0] == id_est and registro[2].lower() == materia_nombre.lower():
                registro_encontrado = registro
                break

        if not registro_encontrado:
            print("\nNo se encontró el estudiante en esa materia.")
            return

        # Pedimos cuántas notas se quieren ingresar
        while True:
            try:
                n = int(input("\n¿Cuántas notas desea agregar? "))
                if n <= 0:
                    print("Debe ingresar al menos una nota.")
                else:
                    break
            except ValueError:
                print("Ingrese un número entero válido.")

        datos_csv = []
        for i in range(n):
            while True:
                try:
                    valor = float(input(f"Ingrese la nota #{i+1} (0.0 - 5.0): "))
                    if 0.0 <= valor <= 5.0:
                        datos_csv.append([registro_encontrado[0], registro_encontrado[1], registro_encontrado[2], valor])
                        break
                    print("La nota debe estar entre 0.0 y 5.0.")
                except ValueError:
                    print("Ingrese un número decimal válido.")

        # Guardamos en CSV correctamente
        encabezados = ["ID Estudiante", "Nombre Estudiante", "Materia", "Nota"]
        GestorCSV.añadir_datos_csv(
            nombre_archivo="notas.csv",
            encabezados=encabezados,
            datos=datos_csv
        )

        print(f"\nSe agregaron {len(datos_csv)} notas para {registro_encontrado[1]} en {registro_encontrado[2]}.\n")

        return datos_csv

class Asistencia:
    def __init__(self):
        self.lista_estudiantes_materias = []  # Se rellena desde Materia

    def recibir_estudiantes(self, lista_estudiantes_materias):
        self.lista_estudiantes_materias = lista_estudiantes_materias

    def registrar_inasistencias(self):
        if not self.lista_estudiantes_materias:
            print("\nNo hay estudiantes inscritos en materias.\n")
            return

        print("\nEstudiantes inscritos y sus materias:\n")
        for registro in self.lista_estudiantes_materias:
            print(f"ID: {registro[0]} - Nombre: {registro[1]} - Materia: {registro[2]}")

        id_est = input("\nDigite el ID del estudiante: ").strip()
        materia_nombre = input("Digite el nombre de la materia: ").strip()

        registro_encontrado = None
        for registro in self.lista_estudiantes_materias:
            if registro[0] == id_est and registro[2].lower() == materia_nombre.lower():
                registro_encontrado = registro
                break

        if not registro_encontrado:
            print("\nNo se encontró el estudiante en esa materia.")
            return

        while True:
            try:
                cantidad = int(input("\n¿Cuántas inasistencias desea registrar? "))
                if cantidad <= 0:
                    print("Debe ingresar al menos una fecha.")
                else:
                    break
            except ValueError:
                print("Ingrese un número entero válido.\n")

        datos_csv = []
        for i in range(cantidad):
            while True:
                fecha = input(f"Ingrese la fecha #{i+1} (dd/mm/aaaa): ").strip()

                partes = fecha.split("/")
                if len(partes) == 3 and all(p.isdigit() for p in partes):
                    dia, mes, anio = map(int, partes)
                    if 1 <= dia <= 31 and 1 <= mes <= 12 and anio >= 2000:
                        datos_csv.append([
                            registro_encontrado[0],
                            registro_encontrado[1],
                            registro_encontrado[2],
                            fecha
                        ])
                        break

                print("Formato inválido. Intente de nuevo (dd/mm/aaaa).")

        encabezados = ["ID Estudiante", "Nombre Estudiante", "Materia", "Fecha Inasistencia"]

        GestorCSV.añadir_datos_csv(
            nombre_archivo="asistencias.csv",
            encabezados=encabezados,
            datos=datos_csv
        )

        print(f"\nSe registraron {len(datos_csv)} fechas de inasistencia para {registro_encontrado[1]} en {registro_encontrado[2]}.\n")

        return datos_csv
    
#Sistema de biblioteca
    
class biblioteca:

    def __init__(self):
        self.lista_libros = [["principito",True],
                             ["pinocho",True],
                             ["matilda",True],
                             ["momo",True],
                             ["programacion",True],
                             ["medicina",True],
                             ["historia",True],
                             ["ingles",True],
                             ["calculo",True],
                             ["videojuegos",True]
                             ]
        self.prestamos = []

    def mostrar_libros(self):
        print("")
        print("Libro"," Estado")
        for x in self.lista_libros:
            estado = "disponible" if x[1] else "Prestado"
            print("")
            print(f"{x[0]} {estado}")


    def prestar_libros(self,persona,nombre_libro):
        for x in self.lista_libros:
            if x[0] == nombre_libro:
                if x[1]:
                    x[1] = False
                    self.prestamos.append([persona[0],nombre_libro])
                    print(f"{x[0]} prestado a {persona[1]}")
                    return
                else:
                    print(f"el libro {x[0]} no esta disponible")
                    return
        print("\nLibro no encontrado")

    def mostrar_prestamos(self):
        print("\nLista de prestamos")
        for p in self.prestamos:
            print(f"Estudiante ID: {p[0]} libro {p[1]}")

    def devolver_libros(self,persona,nombre_libro):
        for x in self.prestamos:
            if x[0] == persona[0] and x[1] == nombre_libro:
                for i in self.lista_libros:
                    if i[0] == nombre_libro:
                        i[1] = True
                        break
                self.prestamos.remove(x)
                print(f"{nombre_libro} devuelto por {persona[1]}")
        print(f"No se encontró un prestamo activo del libro {nombre_libro} para {persona[1]}")


# ============================================================
# PROGRAMA PRINCIPAL
# Muestra el menú y controla la interacción con el usuario
# ============================================================

docente1 = Docente()
estudiante1 = Estudiante()
materia1 = Materia()
actividad1 = Actividad()
nota1 = Notas()
asistencia1 = Asistencia()
Libros1= biblioteca()

while True:
    print("\n--- MENÚ ---")
    print("1. Agregar estudiante")
    print("2. Agregar docente")
    print("3. Inscribir materia (docente)")
    print("4. Inscribir estudiante en materia")
    print("5. Agregar actividad")
    print("6. Agregar notas a estudiante en materia")
    print("7. Añadir asistencia a materia")
    print("8. Acceder a biblioteca")
    print("9. Salir")

    opcion = input("Seleccione una opción: ")

    # Validación: entrada vacía
    if opcion == "":
        print("\n Debes ingresar una opción.")
        continue

    # Validación: número entero
    try:
        opcion = int(opcion)
    except ValueError:
        print("\n Por favor ingrese un número válido.")
        continue

    # Validación: rango correcto
    if opcion < 1 or opcion > 8:
        print("\n Opción fuera de rango. Intente nuevamente.")
        continue

    # --- Ejecución de opciones ---
    if opcion == 1:
        estudiante1.agregar_estudiante()

    elif opcion == 2:
        docente1.agregar_docente()

    elif opcion == 3:
        # Verifica si hay docentes antes de asignar materias
        if not docente1.obtener_docentes():
            print("\n Primero debes agregar docentes antes de inscribir materias.\n")
        else:
            materia1.recibir_docentes(docente1.obtener_docentes())
            materia1.inscribir_materia_docente()

    elif opcion == 4:
        # Verifica si hay estudiantes y materias antes de inscribir
        if not estudiante1.obtener_estudiantes():
            print("\n Primero debes agregar estudiantes antes de inscribirlos en materias.\n")
        elif not materia1.materias_asignadas:
            print("\n No hay materias disponibles aún. Asigna materias a docentes primero.\n")
        else:
            materia1.recibir_estudiantes(estudiante1.obtener_estudiantes())
            materia1.inscribir_estudiante_materia()
    elif opcion == 5:
        actividad1.agregar_actividad()
    elif opcion == 6:
        if not materia1.obtener_materia_estudiantes():
            print("\n Primero debes agregar estudiantes y materias antes de agregar notas.\n")
        else:
            nota1.recibir_estudiantes(materia1.obtener_materia_estudiantes())
            nota1.agregar_notas_estudiantes()
    elif opcion ==7:
        if not materia1.obtener_materia_estudiantes():
            print("\n Primero debes agregar estudiantes y materias antes de agregar asistencia.\n")
        else:
            asistencia1.recibir_estudiantes(materia1.obtener_materia_estudiantes())
            asistencia1.registrar_inasistencias()

    elif opcion == 8:

        print("\nBienvenido al sistema de biblioteca")

        # Verifica si hay estudiantes o docentes
        if not estudiante1.obtener_estudiantes():
                print("\nPrimero debes agregar un estudiante.\n")
        
        
        else:
            accion = input("\n¿Que accion deseas hacer?, presiona\n1. Mostrar lista de libros\n2. Prestar libro\n3. Mostrar libros prestados\n4. Devolver un libro\nSelecciona una opcion: ")
            try:
                accion = int(accion)
            except ValueError:
                print("\nPor favor ingrese un número válido.")

            if accion == 1:

                Libros1.mostrar_libros()
            
            elif accion == 2:
                print("\nPrestamos")
                id_solicitado = input("\nIngrese su Id: ")
                nombre_libro = input("\nIngrese el nombre del libro que desea adquirir: ")

                tilin= estudiante1.buscar_estudiante(id_solicitado)
                
                if tilin:

                    Libros1.prestar_libros(tilin,nombre_libro)


                else:

                    print("\nNo se encontro estudiante con ese id")

            elif accion == 3:

                Libros1.mostrar_prestamos()

            elif accion == 4:

                print("\nDevolucion de libros")
                id_solicitado = input("\nIngrese su Id: ")
                nombre_libro = input("\nIngrese el nombre del libro que desea devolver: ")
                Libros1.devolver_libros(tilin,nombre_libro)
                
            
            else:
                print("Opcion no valida")
                



    elif opcion == 9:
        print("\n Saliendo del programa...")
        break
