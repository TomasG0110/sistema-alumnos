"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os

from flask import Flask, jsonify, request

## Instancia principal de la aplicación Flask.
app = Flask(__name__)

## Base de datos de alumnos en memoria (solo para fines de la actividad).
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

## Versión de la aplicación inyectada por el pipeline para trazabilidad.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Endpoint para saludar al usuario mediante parámetro de consulta.

    Lee el parámetro 'name' desde la cadena de consulta (query string) de la URL.

    @return Mensaje de saludo en texto plano.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """!
    @brief Verifica el estado de salud del servicio.

    @return Respuesta JSON con el estado operativo de la API.
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Entrega el nombre y la versión actual de la aplicación desplegada.

    @return Respuesta JSON con el nombre de la aplicación y su versión.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Lista todos los alumnos registrados en el sistema.

    @return Respuesta JSON con la lista completa de alumnos.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Busca y retorna un alumno específico según su identificador.

    @param alumno_id Identificador numérico único del alumno.
    @return Respuesta JSON con los datos del alumno, o error 404 si no existe.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Crea y registra un nuevo alumno a partir de un cuerpo JSON.

    Valida que el nombre no esté vacío y que el promedio esté entre 1.0 y 7.0.

    @return Respuesta JSON con el alumno creado (código 201) o mensaje de error (código 400).
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


def main():
    """!
    @brief Punto de entrada principal para iniciar el servidor web de desarrollo.
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()