from flask import Blueprint, session, request, render_template, redirect, flash, url_for
from models.db import db
from models.profesores import Profesores
from decorators import prof_required, login_required

routes_profesores = Blueprint("routes_profesores", __name__, url_prefix="/Profesores")

@routes_profesores.route("/CargarServicio", methods=["GET", "POST"])
@prof_required
@login_required
def cargar_servicio():
    profesor_id = session.get("user_id")

    # Si ya tiene servicio → que vaya a modificar
    servicio_existente = Profesores.query.get(profesor_id)
    if servicio_existente:
        return redirect(url_for("routes_profesores.modificar_servicio"))

    if request.method == "GET":
        return render_template("agregar_servicio.html")

    # POST
    nombre_profesor = request.form.get("nombre_profesor", "").strip()
    categoria = request.form.get("categoria", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    modalidad = request.form.get("modalidad", "").strip()
    direccion = request.form.get("direccion", "").strip()
    precio = request.form.get("precio_por_hora", "").strip()

    if not all([nombre_profesor, categoria, descripcion, modalidad, direccion, precio]):
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("routes_profesores.cargar_servicio"))

    try:
        precio = int(precio)
    except ValueError:
        flash("El precio debe ser un número.", "error")
        return redirect(url_for("routes_profesores.cargar_servicio"))

    nuevo_servicio = Profesores(
        id=profesor_id,
        nombre_profesor=nombre_profesor,
        categoria=categoria,
        descripcion=descripcion,
        modalidad=modalidad,
        direccion=direccion,
        precio_por_hora=precio,
    )

    db.session.add(nuevo_servicio)
    db.session.commit()

    flash("Servicio cargado correctamente.", "success")
    return redirect(url_for("routes_profesores.modificar_servicio"))


@routes_profesores.route("/ModificarServicio", methods=["GET", "POST"])
@prof_required
@login_required
def modificar_servicio():
    profesor_id = session.get("user_id")

    servicio = Profesores.query.get(profesor_id)
    if not servicio:
        # Si no tiene servicio → enviarlo a agregar
        return redirect(url_for("routes_profesores.cargar_servicio"))

    if request.method == "GET":
        return render_template("modificar_servicio.html", servicio=servicio)

    # POST → actualizar
    servicio.nombre_profesor = request.form.get("nombre_profesor", "").strip()
    servicio.categoria = request.form.get("categoria", "").strip()
    servicio.descripcion = request.form.get("descripcion", "").strip()
    servicio.modalidad = request.form.get("modalidad", "").strip()
    servicio.direccion = request.form.get("direccion", "").strip()

    precio = request.form.get("precio_por_hora", "").strip()
    try:
        servicio.precio_por_hora = int(precio)
    except:
        flash("El precio debe ser un número.", "error")
        return redirect(url_for("routes_profesores.modificar_servicio"))

    db.session.commit()
    flash("Servicio actualizado correctamente.", "success")

    return redirect(url_for("routes_profesores.modificar_servicio"))
