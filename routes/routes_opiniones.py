from decorators import login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import db
from models.opiniones import Opinion
from models.users import Users
from models.profesores import Profesores
from datetime import datetime

routes_opiniones = Blueprint('routes_opiniones', __name__, url_prefix='/opiniones')


# LISTAR + FORM abajo (usa templates/opiniones.html)
@routes_opiniones.route('/', methods=['GET'])
def index():

    rows = (
        db.session.query(Opinion, Users, Profesores)
        .join(Users, Opinion.user_id == Users.id)
        .outerjoin(Profesores, Profesores.id == Users.id)
        .order_by(Opinion.created_at.desc())
        .all()
    )

    opiniones = []
    for opinion, user, profesor in rows:
        opiniones.append({
            "id": opinion.id,
            "contenido": opinion.contenido,
            "created_at": opinion.created_at,
            "username": user.nombre,
            "rol": user.rol,
            "categoria": profesor.categoria if profesor else None
        })

    return render_template('opiniones.html', opiniones=opiniones)


# CREAR (solo profesores logueados)
@routes_opiniones.route('/crear', methods=['POST'])
@login_required
def crear():
    contenido = (request.form.get('contenido') or '').strip()

    user_id = session.get('user_id')
    user = Users.query.get(user_id)

    if user.rol != "profesor":
        flash("Solo los profesores pueden publicar en este foro.", "danger")
        return redirect(url_for('routes_opiniones.index'))

    # 🌟 Nueva verificación
    profesor = Profesores.query.get(user_id)
    if profesor is None:
        flash("Debes cargar tu servicio antes de comentar en el foro.", "warning")
        return redirect(url_for('routes_profesores.cargar_servicio'))

    if not contenido:
        flash('Escribí tu opinión antes de enviar.', 'warning')
        return redirect(url_for('routes_opiniones.index'))

    nueva_opinion = Opinion(
        user_id=user_id,
        contenido=contenido,
        created_at=datetime.utcnow()
    )

    db.session.add(nueva_opinion)
    db.session.commit()

    flash('Mensaje publicado.', 'success')
    return redirect(url_for('routes_opiniones.index'))



# (Opcional) compatibilidad si alguna vez llamaste a .nueva
@routes_opiniones.route('/nueva', methods=['GET'])
def nueva():
    return redirect(url_for('routes_opiniones.index'))
