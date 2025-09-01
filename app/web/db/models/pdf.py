import uuid
from app.web.db import db
from .base import BaseModel


class Pdf(BaseModel):
    id: str = db.Column(
        db.String(), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: str = db.Column(db.String(80), nullable=False)
    user_id: str = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("User", back_populates="pdfs")

    conversations = db.relationship(
        "Conversation",
        back_populates="pdf",
        order_by="desc(Conversation.created_on)",
    )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "created_on": self.created_on.isoformat() if self.created_on else None,
        }
