"""WSGI entry point for Vercel serverless deployment"""
from app import app

if __name__ == '__main__':
    app.run()
