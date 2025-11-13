from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(f):
    """
    Requiere que el usuario esté logueado.
    Chequea session['logged_in'] (como usás en routes_main.index).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Debes iniciar sesión para acceder a esta página", "error")
            return redirect(url_for("routes_auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Requiere que el usuario sea administrador.
    Rol esperado: 'administrador'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rol = (session.get("rol") or "").lower()
        if rol != "administrador":
            flash("No tienes permisos para realizar esta acción", "error")
            # Lo mandamos al inicio o a donde prefieras
            return redirect(url_for("routes_main.index"))
        return f(*args, **kwargs)
    return decorated_function


def owner_or_admin(f):
    """
    Permite acceso solo si:
    - el usuario es administrador, o
    - el recurso pertenece al usuario (por ejemplo, /users/update/<id>
      donde id == session['user_id']).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rol = (session.get("rol") or "").lower()
        user_id_session = session.get("user_id")

        # Intentamos obtener el parámetro "id" de la ruta
        # (por ejemplo /users/update/<int:id>)
        resource_id = kwargs.get("id")
        if resource_id is None:
            # Como fallback, probamos con "user_id"
            resource_id = kwargs.get("user_id")

        # Admin siempre puede
        if rol == "administrador":
            return f(*args, **kwargs)

        # Si no es admin, tiene que ser dueño de ese recurso
        if user_id_session is not None and resource_id is not None and int(user_id_session) == int(resource_id):
            return f(*args, **kwargs)

        flash("No tienes permisos para acceder a este recurso", "error")
        return redirect(url_for("routes_main.index"))

    return decorated_function

def prof_required(f):
    """
    Requiere que el usuario sea profesor.
    Rol esperado: 'profesor'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rol = (session.get("rol") or "").lower()
        if rol != "profesor":
            flash("No tienes permisos para realizar esta acción", "error")
            return redirect(url_for("routes_main.index"))
        return f(*args, **kwargs)
    return decorated_function