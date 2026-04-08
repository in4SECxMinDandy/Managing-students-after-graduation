"""
QLSVSDH Flask Application Factory
Khởi tạo Flask app với cấu hình database và blueprints
"""
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config


def create_app(config_class=Config):
    """Flask app factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS cho GUI
    CORS(app, origins=["*"], supports_credentials=True)

    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    # Health check endpoint
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "QLSVSDH API"})

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad Request", "message": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "Unauthorized", "message": "Vui lòng đăng nhập"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Forbidden", "message": "Không có quyền truy cập"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not Found", "message": "Không tìm thấy tài nguyên"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal Server Error", "message": "Lỗi hệ thống"}), 500

    return app
