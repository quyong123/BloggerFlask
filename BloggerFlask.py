# coding=utf-8
import os
import sys
from app import create_app,db
from app.models import Role
app = create_app(os.environ.get('FLASK_CONFIG') or 'development')

if __name__ == '__main__':
    app.run(host='192.168.1.107')