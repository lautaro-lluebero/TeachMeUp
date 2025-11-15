from flask import Blueprint, session, request, render_template, redirect, flash, url_for
from models.db import db
from models.profesores import Profesores
from decorators import prof_required, login_required

routes_profesores = Blueprint("routes_profesores", __name__, url_prefix="/Profesores")

ZONAS_MENDOZA = [
    "Capital", "Godoy Cruz", "Guaymallén", "Las Heras", "Luján de Cuyo",
    "Maipú", "San Martín", "Rivadavia", "Junín", "Tunuyán", "Tupungato",
    "San Rafael", "Malargüe"
]

CATEGORIAS = [
    "Matemática", "Lengua", "Inglés", "Naturales", "Sociales", "Física",
    "Química", "Historia", "Programación", "Biología", "Geografía", "Filosofía",
    "Arte", "Tecnología", "Contabilidad", "Economía", "Administración", "Electrónica",
]

NIVELES = [
    "Inicial", "Primario", "Secundario", "Inicial-Primario",
    "Primario-Secundario", "Secundario-Universitario", "Universitario"
]

# ================== CARGAR SERVICIO (UNO POR PROFESOR) ==================

@routes_profesores.route("/CargarServicio", methods=["GET", "POST"])
@prof_required
@login_required
def cargar_servicio():
    profesor_id = session.get("user_id")

    # Si ya tiene servicio → que vaya a ver/modificar
    servicio_existente = Profesores.query.get(profesor_id)
    if servicio_existente:
        flash("Ya tienes un servicio existente.", "info")
        return redirect(url_for("routes_profesores.ver_servicio"))

    if request.method == "GET":
        return render_template(
            "agregar_servicio.html",
            categorias=CATEGORIAS,
            niveles=NIVELES,
            zonas=ZONAS_MENDOZA
        )

    # POST
    nombre_profesor = request.form.get("nombre_profesor", "").strip()
    categoria       = request.form.get("categoria", "").strip()
    nivel           = request.form.get("nivel", "").strip()
    descripcion     = request.form.get("descripcion", "").strip()
    modalidad       = request.form.get("modalidad", "").strip()
    direccion       = request.form.get("direccion", "").strip()
    celular         = request.form.get("celular", "").strip()
    precio          = request.form.get("precio_por_hora", "").strip()

    if not all([nombre_profesor, categoria, nivel, descripcion, modalidad, celular, direccion, precio]):
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("routes_profesores.cargar_servicio"))

    try:
        precio = int(precio)
    except ValueError:
        flash("El precio debe ser un número.", "error")
        return redirect(url_for("routes_profesores.cargar_servicio"))

    nuevo_servicio = Profesores(
        id=profesor_id,  # 1 servicio por usuario: PK = FK user_id
        nombre_profesor=nombre_profesor,
        categoria=categoria,
        nivel=nivel,
        descripcion=descripcion,
        modalidad=modalidad,
        direccion=direccion,
        celular=celular,
        precio_por_hora=precio,
    )

    db.session.add(nuevo_servicio)
    db.session.commit()

    flash("Servicio cargado correctamente.", "success")
    return redirect(url_for("routes_profesores.ver_servicio"))


# ================== VER SERVICIO ==================

@routes_profesores.route("/VerServicio")
@prof_required
@login_required
def ver_servicio():
    profesor_id = session.get("user_id")

    servicio = Profesores.query.get(profesor_id)

    if not servicio:
        flash("Debes cargar tu servicio primero.", "info")
        return redirect(url_for("routes_profesores.cargar_servicio"))

    return render_template(
        "ver_servicio.html",
        servicio=servicio,
        avatar_url=url_for('static', filename='img/user_default.jpeg')
    )


# ================== BORRAR SERVICIO ==================

@routes_profesores.route("/BorrarServicio", methods=["POST"])
@prof_required
@login_required
def borrar_servicio():
    profesor_id = session.get("user_id")

    servicio = Profesores.query.get(profesor_id)

    if not servicio:
        flash("No se encontró ningún servicio para borrar.", "error")
        return redirect(url_for("routes_profesores.ver_servicio"))

    db.session.delete(servicio)
    db.session.commit()

    flash("Tu servicio ha sido eliminado correctamente. Puedes cargar uno nuevo cuando quieras.", "success")
    return redirect(url_for("routes_main.index"))


# ================== MODIFICAR SERVICIO ==================

@routes_profesores.route("/ModificarServicio", methods=["GET", "POST"])
@prof_required
@login_required
def modificar_servicio():
    profesor_id = session.get("user_id")

    servicio = Profesores.query.get(profesor_id)
    if not servicio:
        flash("Debes cargar tu servicio primero.", "info")
        return redirect(url_for("routes_profesores.cargar_servicio"))

    if request.method == "GET":
        return render_template(
            "modificar_servicio.html",
            servicio=servicio,
            categorias=CATEGORIAS,
            niveles=NIVELES,
            zonas=ZONAS_MENDOZA
        )

    # POST → actualizar
    servicio.nombre_profesor = request.form.get("nombre_profesor", "").strip()
    servicio.categoria       = request.form.get("categoria", "").strip()
    servicio.nivel           = request.form.get("nivel", "").strip()
    servicio.descripcion     = request.form.get("descripcion", "").strip()
    servicio.modalidad       = request.form.get("modalidad", "").strip()
    servicio.direccion       = request.form.get("direccion", "").strip()
    servicio.celular         = request.form.get("celular", "").strip()
    precio                   = request.form.get("precio_por_hora", "").strip()

    try:
        servicio.precio_por_hora = int(precio)
    except ValueError:
        flash("El precio debe ser un número.", "error")
        return redirect(url_for("routes_profesores.modificar_servicio"))

    db.session.commit()
    flash("Servicio actualizado correctamente.", "success")

    return redirect(url_for("routes_profesores.ver_servicio"))


# ================== LISTAR PROFESORES (PÚBLICO + FILTROS) ==================

@routes_profesores.route("/", methods=["GET"])
def listar_profesores():
    """
    Lista de servicios de profesores con filtros por:
    - categoría (materia)
    - zona (usamos direccion como zona)
    - modalidad
    """
    categorias_sel = request.args.getlist("categorias")
    zonas_sel      = request.args.getlist("zonas")
    modalidad_sel  = request.args.get("modalidad", "").strip()

    query = Profesores.query

    if categorias_sel:
        query = query.filter(Profesores.categoria.in_(categorias_sel))

    if zonas_sel:
        query = query.filter(Profesores.direccion.in_(zonas_sel))

    if modalidad_sel:
        query = query.filter(Profesores.modalidad == modalidad_sel)

    profesores = query.all()

    return render_template(
        "profesores.html",
        profesores=profesores,
        categorias=CATEGORIAS,
        zonas=ZONAS_MENDOZA,
        niveles=NIVELES,
        categorias_sel=categorias_sel,
        zonas_sel=zonas_sel,
        modalidad_sel=modalidad_sel,
    )

@routes_profesores.route("/Detalle/<int:profesor_id>")
def detalle_profesor(profesor_id):
    servicio = Profesores.query.get_or_404(profesor_id)
    return render_template("detalle_profesor.html", servicio=servicio)
# routes_profesores.py
from flask import Blueprint, render_template

routes_profesores = Blueprint('routes_profesores', __name__)

@routes_profesores.route("/mapa")
def mapa():
    return render_template("mapaProf.html")

