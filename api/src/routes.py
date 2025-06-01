from datetime import datetime

# Third-party modules
from flask import Blueprint, request, jsonify, make_response

# Own Modules
from business_logic import (
    bl_create_user,
    bl_get_user,
    bl_get_all_users,
    bl_update_user,
    bl_delete_user,
    bl_search_user
)
from create_pdf import generate_statistics_pdf

api = Blueprint("api", __name__)

@api.route("/healthcheck")
def health_check():
    return jsonify({"status": "running"})

@api.route("/user", methods=["POST"])
def create_user_route():
    data = request.get_json()
    try:
        user_id = bl_create_user(data)
        return jsonify({"message": f"User with ID {user_id} successfully created"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Field {e} missing"}), 400

@api.route("/user/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    user = bl_get_user(user_id)
    if user:
        user_data = {
            "id": user.id,
            "vorname": user.vorname,
            "nachname": user.nachname,
            "geburtsdatum": user.geburtsdatum.isoformat() if user.geburtsdatum else None,
            "kontakt": {"email": user.kontakt.email, "telefonnummer": user.kontakt.telefonnummer} if user.kontakt else None,
            "adresse": {"strasse": user.adresse.strasse, "hausnummer": user.adresse.hausnummer, "plz": user.adresse.plz, "ort": user.adresse.ort, "land": user.adresse.land} if user.adresse else None
        }
        return jsonify(user_data)
    return jsonify({"error": "User not found"}), 404

@api.route("/users", methods=["GET"])
def get_all_user_route():
    users = bl_get_all_users()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "vorname": user.vorname,
            "nachname": user.nachname,
            "geburtsdatum": user.geburtsdatum.isoformat() if user.geburtsdatum else None,
            "kontakt": {"email": user.kontakt.email, "telefonnummer": user.kontakt.telefonnummer} if user.kontakt else None,
            "adresse": {"strasse": user.adresse.strasse, "hausnummer": user.adresse.hausnummer, "plz": user.adresse.plz, "ort": user.adresse.ort, "land": user.adresse.land} if user.adresse else None
        })
    return jsonify(user_list)

@api.route("/user/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    updated_user = bl_update_user(user_id, data)
    if updated_user:
        return jsonify({"message": f"User with ID {user_id} successfully updated"})
    return jsonify({"error": "User not found"}), 404

@api.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    if bl_delete_user(user_id):
        return jsonify({"message": f"User with ID {user_id} successfully deleted"})
    return jsonify({"error": "User not found"}), 404

@api.route("/search", methods=["GET"])
def serarch_user():
    # Get Args
    args = request.args
    
    # Get Parameters from Args
    vorname = args.get("vorname", default=None, type=str)
    nachname = args.get("nachname", default=None, type=str)
    telefonnummer = args.get("telefonnummer", default=None, type=str)
    strasse = args.get("strasse", default=None, type=str)
    ort = args.get("ort", default=None, type=str)
    land = args.get("land", default=None, type=str)
    plz = args.get("plz", default=None, type=str)

    try:
        # Search in Business Logic
        users = bl_search_user(
            vorname=vorname,
            nachname=nachname,
            telefonnummer=telefonnummer,
            strasse=strasse,
            ort=ort,
            land=land,
            plz=plz
            )

        # Create json object
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "vorname": user.vorname,
                "nachname": user.nachname,
                "geburtsdatum": user.geburtsdatum.isoformat() if user.geburtsdatum else None,
                "kontakt": {"email": user.kontakt.email, "telefonnummer": user.kontakt.telefonnummer} if user.kontakt else None,
                "adresse": {"strasse": user.adresse.strasse, "hausnummer": user.adresse.hausnummer, "plz": user.adresse.plz, "ort": user.adresse.ort, "land": user.adresse.land} if user.adresse else None
            })

        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error": f"{e}"})

@api.route('/download-statistics-pdf')
def download_statistics_pdf():
    try:
        pdf_data = generate_statistics_pdf()
        
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=personenstatistiken_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        
        return response
        
    except Exception as e:
        return f"Error when generating the PDF: {str(e)}", 500

@api.route('/view-statistics-pdf')
def view_statistics_pdf():
    try:
        pdf_data = generate_statistics_pdf()
        
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=personenstatistiken.pdf'
        
        return response
        
    except Exception as e:
        return f"Error when generating the PDF: {str(e)}", 500