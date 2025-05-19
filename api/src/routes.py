from flask import Blueprint, request, jsonify

# Own Modules
from business_logic import (
    bl_create_user,
    bl_get_user,
    bl_get_all_users,
    bl_update_user,
    bl_delete_user,
    bl_search_user
)

api = Blueprint('api', __name__)

@api.route('/healthcheck')
def health_check():
    return jsonify({'status': 'running'})

@api.route('/user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    try:
        user_id = bl_create_user(data)
        return jsonify({'message': f'Nutzer mit ID {user_id} erfolgreich erstellt'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        return jsonify({'error': f'Feld {e} fehlt'}), 400

@api.route('/user/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    user = bl_get_user(user_id)
    if user:
        user_data = {
            'id': user.id,
            'vorname': user.vorname,
            'nachname': user.nachname,
            'geburtsdatum': user.geburtsdatum.isoformat() if user.geburtsdatum else None,
            'kontakt': {'email': user.kontakt.email, 'telefonnummer': user.kontakt.telefonnummer} if user.kontakt else None,
            'adresse': {'strasse': user.adresse.strasse, 'hausnummer': user.adresse.hausnummer, 'plz': user.adresse.plz, 'ort': user.adresse.ort, 'land': user.adresse.land} if user.adresse else None
        }
        return jsonify(user_data)
    return jsonify({'message': 'Nutzer nicht gefunden'}), 404

@api.route('/users', methods=['GET'])
def get_all_user_route():
    users = bl_get_all_users()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'vorname': user.vorname,
            'nachname': user.nachname,
            'geburtsdatum': user.geburtsdatum.isoformat() if user.geburtsdatum else None,
            'kontakt': {'email': user.kontakt.email, 'telefonnummer': user.kontakt.telefonnummer} if user.kontakt else None,
            'adresse': {'strasse': user.adresse.strasse, 'hausnummer': user.adresse.hausnummer, 'plz': user.adresse.plz, 'ort': user.adresse.ort, 'land': user.adresse.land} if user.adresse else None
        })
    return jsonify(user_list)

@api.route('/user/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.get_json()
    updated_user = bl_update_user(user_id, data)
    if updated_user:
        return jsonify({'message': f'Nutzer mit ID {user_id} erfolgreich aktualisiert'})
    return jsonify({'message': 'Nutzer nicht gefunden'}), 404

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    if bl_delete_user(user_id):
        return jsonify({'message': f'Nutzer mit ID {user_id} erfolgreich gelöscht'})
    return jsonify({'message': 'Nutzer nicht gefunden'}), 404

@api.route('/user/search/<query>', methods=['GET'])
def get_all_user_route(query):
    
    try:
        result = bl_search_user(query)
        return jsonify(result)
    except:
       return jsonify({'error': 'Not found.'}), 400 
