from . import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='project',
                             lazy=True, cascade="all, delete-orphan")


class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id'), nullable=False)

    external_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=True)

    notes = db.Column(db.Text, nullable=True)
    visited = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('project_id', 'external_id',
                            name='unique_project_place'),
    )
