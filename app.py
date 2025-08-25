from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos de prueba (puedes cambiar por base de datos en el futuro)
usuarios = {"admin": "1234"}
tareas = []
contador_id = 1


@app.route("/")
def home():
    return "Bienvenido al Sistema de Gestión de Tareas"


# ---- LOGIN ----
@app.route("/login", methods=["POST"])
def login():
    datos = request.json
    usuario = datos.get("usuario")
    password = datos.get("password")

    if usuario in usuarios and usuarios[usuario] == password:
        return jsonify({"mensaje": "Login exitoso"})
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401


# ---- CRUD DE TAREAS ----
@app.route("/tareas", methods=["GET"])
def listar_tareas():
    return jsonify(tareas)


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    global contador_id
    datos = request.json
    nueva_tarea = {
        "id": contador_id,
        "titulo": datos.get("titulo"),
        "descripcion": datos.get("descripcion"),
        "completada": False
    }
    tareas.append(nueva_tarea)
    contador_id += 1
    return jsonify(nueva_tarea), 201


@app.route("/tareas/<int:id_tarea>", methods=["PUT"])
def editar_tarea(id_tarea):
    for tarea in tareas:
        if tarea["id"] == id_tarea:
            tarea["titulo"] = request.json.get("titulo", tarea["titulo"])
            tarea["descripcion"] = request.json.get("descripcion", tarea["descripcion"])
            tarea["completada"] = request.json.get("completada", tarea["completada"])
            return jsonify(tarea)
    return jsonify({"mensaje": "Tarea no encontrada"}), 404


@app.route("/tareas/<int:id_tarea>", methods=["DELETE"])
def eliminar_tarea(id_tarea):
    global tareas
    tareas = [t for t in tareas if t["id"] != id_tarea]
    return jsonify({"mensaje": "Tarea eliminada"})


if __name__ == "__main__":
    app.run(debug=True)
