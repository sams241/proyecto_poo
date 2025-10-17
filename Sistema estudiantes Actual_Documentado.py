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
        self.lista_docentes = []       # Lista recibida desde la clase Docente
        self.materias_asignadas = []   # Guarda las relaciones docente-materia

    # Recibe la lista de docentes desde otra clase
    def recibir_docentes(self, lista):
        self.lista_docentes = lista

    # Permite asignar una materia a un docente ya registrado
    def inscribir_materia_docente(self):
        if not self.lista_docentes:
            print("\n No hay docentes registrados aún. Agrega docentes antes de inscribir materias.\n")
            return

        # Muestra la lista de docentes disponibles
        print("\n Lista de docentes disponibles:\n")
        for docente in self.lista_docentes:
            print(f"ID: {docente[0]} - Nombre: {docente[1]} - Email: {docente[4]}")

        print("--------------------------------------")
        id_docente = input("Digite el id del docente al que le quiere inscribir materias: ")

        docente_encontrado = None

        # Busca al docente por su ID
        for docente in self.lista_docentes:
            if docente[0] == id_docente:
                docente_encontrado = docente
                break

        # Si no se encuentra, se detiene el proceso
        if not docente_encontrado:
            print(f"No se encontró el docente con el id: {id_docente}")
            return

        # Pide el nombre de la materia a asignar
        nombre_materia = input("Digite el nombre de la materia: ")

        # Crea el registro de inscripción
        inscripcion_materias = [docente_encontrado[0], docente_encontrado[1], nombre_materia]
        self.materias_asignadas.append(inscripcion_materias)

        print(f"\nLa materia '{nombre_materia}' ha sido asignada correctamente al docente con id: {docente_encontrado[1]}.\n")

        # Muestra todas las materias asignadas
        print("Listado de materias asignadas:\n")
        for m in self.materias_asignadas:
            print(f"Docente: {m[1]} - Materia: {m[2]}")


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

            nombre_actividad = input("Nombre de la actividad: ").strip()
            while not nombre_actividad:
                nombre_actividad = input("El nombre no puede estar vacío: ").strip()

            tipo_actividad = input("Tipo de actividad (Tarea, Examen, Taller, Proyecto): ").strip()
            while not tipo_actividad:
                tipo_actividad = input("El tipo no puede estar vacío: ").strip()

            descripcion = input("Descripción (opcional): ").strip() or "Sin descripción"

            # Permite ingresar la fecha con o sin /
            fecha_entrega = input("Fecha de entrega (ddmmaaaa o dd/mm/aaaa): ").strip()
            if '/' not in fecha_entrega and len(fecha_entrega) == 8:
                fecha_entrega = f"{fecha_entrega[:2]}/{fecha_entrega[2:4]}/{fecha_entrega[4:]}"

            while not fecha_entrega:
                fecha_entrega = input("La fecha no puede estar vacía: ").strip()

            # Guarda la actividad asociada a la persona
            self.actividades.append([
                id_actividad,
                nombre_actividad,
                tipo_actividad,
                descripcion,
                fecha_entrega,
                id_persona,
                nombre_persona,
                email_persona
            ])

        # Muestra en pantalla todas las actividades registradas
        print("\nACTIVIDADES REGISTRADAS:")
        for act in self.actividades:
            print(f"Actividad: {act[1]} -- Tipo: {act[2]} -- Persona: {act[6]}")

        # Guarda las actividades en un archivo CSV
        encabezados = [
            "id_actividad", "Nombre_actividad", "Tipo", "Descripcion",
            "Fecha_entrega", "id_persona", "Nombre_persona", "Email_persona"
        ]
        GestorCSV.añadir_datos_csv("actividades.csv", encabezados, self.actividades)


# ============================================================
# PROGRAMA PRINCIPAL
# Muestra el menú y controla la interacción con el usuario
# ============================================================

docente1 = Docente()
estudiante1 = Estudiante()
materia1 = Materia()
actividad1 = Actividad()

while True:
    print("\n--- MENÚ ---")
    print("1. Agregar estudiante")
    print("2. Agregar Docente")
    print("3. Inscribir Materia")
    print("4. Agregar Actividad")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    # Valida que se ingrese algo
    if opcion == "":
        print("\n Debes ingresar una opción.")
        continue

    # Valida que sea un número entero
    try:
        opcion = int(opcion)
    except ValueError:
        print("\n Por favor ingrese un número válido.")
        continue

    # Valida que esté dentro del rango del menú
    if opcion < 1 or opcion > 5:
        print("\n Opción fuera de rango. Intente nuevamente.")
        continue

    # Ejecuta la opción seleccionada
    if opcion == 1:
        estudiante1.agregar_estudiante()

    elif opcion == 2:
        docente1.agregar_docente()

    elif opcion == 3:
        # Verifica si hay docentes registrados antes de asignar materia
        if not docente1.obtener_docentes():
            print("\n Primero debes agregar docentes antes de inscribir materias.\n")
        else:
            materia1.recibir_docentes(docente1.obtener_docentes())
            materia1.inscribir_materia_docente()

    elif opcion == 4:
        actividad1.agregar_actividad()

    elif opcion == 5:
        print("\n Saliendo del programa...")
        break
