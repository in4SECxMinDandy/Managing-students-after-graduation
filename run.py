"""
Flask Application Entry Point
Chạy: python run.py
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("QLSVSDH API Server")
    print("=" * 50)
    print("Starting Flask server...")
    print("API Endpoints: http://localhost:5000/api/")
    print("Health Check:  http://localhost:5000/api/health")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
