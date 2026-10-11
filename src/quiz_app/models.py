from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db

from typing import Literal


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    decks: Mapped[list["Deck"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Question(db.Model):
    __tablename__ = "questions"

    __table_args__ = (
        CheckConstraint(
            "answer IN ('A', 'B', 'C', 'D')", name="ck_questions_valid_answer"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(nullable=False)
    option_a: Mapped[str] = mapped_column(nullable=False)
    option_b: Mapped[str] = mapped_column(nullable=False)
    option_c: Mapped[str] = mapped_column(nullable=False)
    option_d: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[Literal["A", "B", "C", "D"]] = mapped_column(nullable=False)
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=False)
    deck: Mapped["Deck"] = relationship(back_populates="questions")


class Deck(db.Model):
    __tablename__ = "decks"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    questions: Mapped[list[Question]] = relationship(
        back_populates="deck", cascade="all, delete-orphan"
    )
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped[User] = relationship(back_populates="decks")
