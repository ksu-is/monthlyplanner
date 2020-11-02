from . import db, ma

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(120))

    def __repr__(self):
        return "Todo('{}')".format(self.title)

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('titles')