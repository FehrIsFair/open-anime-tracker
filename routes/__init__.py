from main import app
from routes.anime import AnimeView
from routes.list import ListView
from routes.user import UserView

AnimeView.register(app)
ListView.register(app)
UserView.register(app)
