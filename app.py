from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que la página web se comunique con este servidor

# Base de datos simulada en memoria para los cursos
courses = [
    {
        "id": 1,
        "title": "Introducción a la Inteligencia Artificial",
        "description": "Aprende los conceptos básicos y herramientas de IA.",
        "duration": "4 semanas",
    },
    {
        "id": 2,
        "title": "Gestión de Proyectos de Software",
        "description": "Metodologías ágiles y control de proyectos.",
        "duration": "6 semanas",
    },
]


# 1. GET: Obtener todos los cursos
@app.route("/api/courses", methods=["GET"])
def get_courses():
  return jsonify(courses)


# 2. POST: Crear un nuevo curso
@app.route("/api/courses", methods=["POST"])
def create_course():
  data = request.get_json()
  new_id = courses[-1]["id"] + 1 if courses else 1
  new_course = {
      "id": new_id,
      "title": data.get("title", ""),
      "description": data.get("description", ""),
      "duration": data.get("duration", ""),
  }
  courses.append(new_course)
  return jsonify(new_course), 201


# 3. GET: Obtener un curso por su ID
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
  course = next((c for c in courses if c["id"] == course_id), None)
  if not course:
    return jsonify({"error": "Curso no encontrado"}), 404
  return jsonify(course)


# 4. PUT: Actualizar un curso
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
  course = next((c for c in courses if c["id"] == course_id), None)
  if not course:
    return jsonify({"error": "Curso no encontrado"}), 404
  data = request.get_json()
  course["title"] = data.get("title", course["title"])
  course["description"] = data.get("description", course["description"])
  course["duration"] = data.get("duration", course["duration"])
  return jsonify(course)


# 5. DELETE: Eliminar un curso
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
  global courses
  course = next((c for c in courses if c["id"] == course_id), None)
  if not course:
    return jsonify({"error": "Curso no encontrado"}), 404
  courses = [c for c in courses if c["id"] != course_id]
  return jsonify({"message": "Curso eliminado con éxito"})


if __name__ == "__main__":
  app.run(port=5000, debug=True)