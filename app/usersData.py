"""This module will serve the api request."""

from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
from importlib.machinery import SourceFileLoader


# Yardımcı modüller import edildi
helper_module = SourceFileLoader('*', './app/helpers.py').load_module()

# Veritabanı Seçildi
db = client.restfulapi
# Tablo Seçildi
collection = db.users

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Ekran çıktısı
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Mesajın ekranda görünmesi sağlandı
    resp = jsonify(message)
    return resp


@app.route("/api/v1/users", methods=['POST'])
def create_user():
    try:
        # Yeni bir kullanıcı oluşturuldu
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "", 400
        record_created = collection.insert(body)
        # Yanıt hazırlandı
        if isinstance(record_created, list):
            return jsonify([str(v) for v in record_created]), 201
        else:
            return jsonify(str(record_created)), 201
    except:
        return "", 500

@app.route("/api/v1/users", methods=['GET'])
def fetch_users():
    try:
        query_params = helper_module.parse_query_params(request.query_string)
        if query_params:
            # Değeri int'e dönüştürme
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}
            # Tüm kayıtları getir
            records_fetched = collection.find(query)
            # Kayıtların bulunup bulunmadığını kontrol edin
            if records_fetched.count() > 0:
                return dumps(records_fetched)
            else:
                # Kayıt bulunamadı
                return "", 404
        # Kayıt boşsa
        else:
            # Sorgu dizesi parametreleri kullanılamadığından tüm kayıtları döndür
            if collection.find().count() > 0:
                # Kullanıcılar bulunursa yanıtı hazırlayın
                return dumps(collection.find())
            else:
                # Kullanıcı bulunmazsa boş diziyi döndür
                return jsonify([])
    except:
        # Kaynağı getirmeye çalışırken hata
        # Hata ayıklama amacıyla mesaj ekleyin
        return "", 500


@app.route("/api/v1/users/<user_id>", methods=['POST'])
def update_user(user_id):
    try:
        # Güncellenmesi gereken değeri girin
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # İstek gövdesi mevcut olmadığından hatalı istek
            # Hata ayıklama amacıyla mesaj ekleyin
            return "", 400

        # Kullanıcı güncelle
        records_updated = collection.update_one({"id": int(user_id)}, body)

        # Kaynağın güncellenip güncellenmediğini kontrol edin
        if records_updated.modified_count > 0:
            # Kaynak başarıyla güncellendiğinde yanıtı hazırlayın
            return "", 200
        else:
            # Kaynak güncellenemediğinden hatalı istek
            # Hata ayıklama amacıyla mesaj ekleyin
            return "", 404
    except:
        return "", 500


@app.route("/api/v1/users/<user_id>", methods=['DELETE'])
def remove_user(user_id):
    try:
        # Kullanıcı silme
        delete_user = collection.delete_one({"id": int(user_id)})

        if delete_user.deleted_count > 0 :
            # Yanıtı hazırlayın
            return "", 204
        else:
            # Kaynak Bulunamadı
            return "", 404
    except:
        # İstek gövdesi mevcut olmadığından hatalı istek
        # Hata ayıklama amacıyla mesaj ekleyin
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """NotFound 404 durumundaki kullanıcıya mesaj gönder."""
    # Kullanıcıya mesaj
    message = {
        "err":
            {
                "msg": "Bu rota şu anda desteklenmiyor. Lütfen API belgelerine bakın."
            }
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
