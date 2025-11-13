from flask import Blueprint, session, request, render_template, redirect, flash, url_for
from models.db import db
from models.profesores import Profesores
from decorators import prof_required, login_required

routes_profesores= Blueprint("routes_profesores", __name__, url_prefix="/Profesores")

@routes_profesores.route("/CargarServicio",methods=["GET", "POST"])
@prof_required
@login_required
def cargar_servicio():
    nombre_profesor = categoria = descripcion = modalidad = direccion = precio = None
    profesor_id = session.get("user_id")
    profesor_nombre = session.get("username")

    if request.method == "GET":
        profesor_id = session.get("user_id")
        print(f"ID en sesión: {profesor_id}")
        servicio_existente = Profesores.query.get(profesor_id)
        print(f"Servicio encontrado: {servicio_existente}")
        return render_template("cargar_servicio.html", servicio=servicio_existente)

    if request.method == "POST":
        nombre_profesor = request.form.get("nombre_profesor", "").strip()
        categoria = request.form.get("categoria", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        modalidad = request.form.get("modalidad", "").strip()
        direccion = request.form.get("direccion", "").strip()
        precio = request.form.get("precio_por_hora", "").strip()

    # Validar campos obligatorios
    if not all([nombre_profesor, categoria, descripcion, modalidad, direccion, precio]):
        return render_template(
            "cargar_servicio.html",
            error="Todos los campos son obligatorios."
        )

    # Validar que el precio sea número
    try:
        precio = int(precio)
    except ValueError:
        return render_template(
            "cargar_servicio.html",
            error="El precio debe ser un número entero."
        )

    # Buscar si ya tiene servicio cargado
    servicio = Profesores.query.filter_by(id=profesor_id).first()

    if servicio:
        # 🔁 Actualizar servicio existente
        servicio.nombre_profesor = nombre_profesor
        servicio.categoria = categoria
        servicio.descripcion = descripcion
        servicio.modalidad = modalidad
        servicio.direccion = direccion
        servicio.precio_por_hora = precio
        db.session.commit()
        flash("Servicio actualizado correctamente", "success")
    else:
        # 🆕 Crear nuevo servicio
        nuevo_servicio = Profesores(
            id=profesor_id,
            nombre_profesor=nombre_profesor,
            categoria=categoria,
            descripcion=descripcion,
            modalidad=modalidad,
            direccion=direccion,
            precio_por_hora=precio
        )
        db.session.add(nuevo_servicio)
        db.session.commit()
        flash("Servicio cargado correctamente", "success")

    # 🔄 Redirigir para recargar el formulario con los datos actualizados
    return redirect(url_for("routes_profesores.cargar_servicio"))

