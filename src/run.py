import sys

sys.path.append(".")
from src.app import app
# from src.config import PORT

__author__ = 'ishween'

PORT = 8000

app.run(debug=app.config['DEBUG'], port=PORT, host='0.0.0.0')