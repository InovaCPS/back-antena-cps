from webapp import db
from models.table_parceiros import Parceiros
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(Parceiros.id_geral))
    user = db.relationship(Parceiros)