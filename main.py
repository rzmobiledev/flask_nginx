
import os
from dotenv import load_dotenv
from configuration.route import router
from configuration.base import app, db

load_dotenv()

with app.app_context():
    db.create_all()

app.register_blueprint(router)
    
if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG'), host="0.0.0.0", port=os.environ.get("FLASK_PORT"))
