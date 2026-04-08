"""
App routes package
Register all blueprints here
"""


def register_blueprints(app):
    """Register all Flask blueprints"""
    from app.routes.auth_routes import auth_bp
    from app.routes.khoa_routes import khoa_bp
    from app.routes.mon_hoc_routes import mon_hoc_bp
    from app.routes.nganh_routes import nganh_bp
    from app.routes.lop_routes import lop_bp
    from app.routes.tuyen_sinh_routes import tuyen_sinh_bp
    from app.routes.hoc_tap_routes import hoc_tap_bp
    from app.routes.tot_nghiep_routes import tot_nghiep_bp
    from app.routes.thong_bao_routes import thong_bao_bp
    from app.routes.sinh_vien_routes import sinh_vien_bp

    # Auth routes
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # CRUD routes
    app.register_blueprint(khoa_bp, url_prefix="/api/khoa")
    app.register_blueprint(mon_hoc_bp, url_prefix="/api/mon-hoc")
    app.register_blueprint(nganh_bp, url_prefix="/api/nganh")
    app.register_blueprint(lop_bp, url_prefix="/api/lop")
    app.register_blueprint(sinh_vien_bp, url_prefix="/api/sinh-vien")

    # Business routes
    app.register_blueprint(tuyen_sinh_bp, url_prefix="/api/tuyen-sinh")
    app.register_blueprint(hoc_tap_bp, url_prefix="/api/hoc-tap")
    app.register_blueprint(tot_nghiep_bp, url_prefix="/api/tot-nghiep")
    app.register_blueprint(thong_bao_bp, url_prefix="/api/thong-bao")
