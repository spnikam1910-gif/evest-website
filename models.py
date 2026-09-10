from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Lead(db.Model):
    """A contact / 'Book a Consultation' submission.

    Kept intentionally simple for v1 (SQLite + SQLAlchemy). Swap the
    DATABASE_URL in .env for Postgres/MySQL in production — no code
    changes required. See app.notify_new_lead() for wiring this up to
    email, a CRM, or WhatsApp later.
    """

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(150), nullable=True)
    service_interested = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="new")  # new | contacted | closed

    def __repr__(self):
        return f"<Lead {self.id} {self.full_name} ({self.email})>"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "company_name": self.company_name,
            "service_interested": self.service_interested,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
        }


class NewsletterSubscriber(db.Model):
    """Optional lightweight capture for footer newsletter signups."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
