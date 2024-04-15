# Documentación del Proyecto de la Droguería

## Descripción General

El proyecto de la Droguería es un sistema de gestión que permite manejar inventarios de medicamentos, gestionar clientes y médicos, y crear y almacenar facturas.
> Permite realizar diversas operaciones a través de un menú de consola.

## Estructura del Proyecto

### Módulos Principales

* `cliente.py`: Define las clases CustomABC, Usuario, Cliente, y Medico.
* `inventario.py`: Contiene las clases relacionadas con el manejo del inventario de medicamentos, incluyendo la lectura y escritura de datos en diferentes formatos (CSV, JSON, TXT).
* `drogueria.py`: Es el módulo central que integra las funcionalidades de los clientes, médicos, inventario y facturas. Define la clase Drogueria que contiene métodos para agregar clientes, médicos, manejar el inventario y crear facturas.
* `main.py`: Proporciona la interfaz de usuario a través de la consola, permitiendo interactuar con el sistema mediante un menú de opciones.

### Funcionalidades Clave

* `Gestión de Inventario`: Cargar y guardar inventario en diferentes formatos, crear inventario ficticio, y mostrar el inventario actual.
* `Gestión de Personas`: Crear personas ficticias (clientes y médicos) y mostrar la lista de personas.
* `Gestión de Facturas`: Crear facturas ficticias y mostrar todas las facturas generadas.

### Menú Interactivo

> `python main.py`

* `Cargar inventario desde archivo`: Permite al usuario cargar el inventario desde un archivo en formatos CSV, JSON o TXT.
* `Crear inventario ficticio`: Genera un conjunto de medicamentos ficticios para poblar el inventario.
* `Mostrar inventario actual`
* `Guardar inventario actual`: Guarda el inventario actual en el formato especificado por el usuario (CSV, JSON, TXT).
* `Crear personas ficticias (Clientes y Médicos)`: Genera un conjunto de clientes y médicos ficticios.
* `Mostrar personas`: Muestra las listas de clientes y médicos registrados en el sistema.
* `Crear factura ficticia y guardarla en .txt`: Crea una factura ficticia utilizando los clientes y medicamentos disponibles y la guarda en formato TXT.
* `Mostrar facturas`: Muestra todas las facturas creadas en el sistema.
* `Crear todo`: **Ejecuta una secuencia de acciones para demostrar la funcionalidad del sistema haciendo lo pedido por el ejercicio, incluyendo la creación de personas, inventario y facturas.**
* `Salir`: Termina la ejecución del programa.
