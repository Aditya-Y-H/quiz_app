## test_connect.py
### test_index
Checks that the home route responds with HTTP 200 and renders a page titled "Quizzer".

### test_unknown_route_returns_404
Checks that requesting an undefined route returns HTTP 404.

## test_migrations.py
### test_migrations_build_current_schema
Runs the Alembic upgrade command and verifies it succeeds, creates the users, decks, questions, and alembic_version tables, adds the deck slug column, and makes deck user_id nullable.

## test_models.py
### test_deck_has_many_questions
Persists a user, a deck, and two questions, then reloads the deck and checks that both questions and the user relationship were stored correctly.

### test_user_has_many_decks
Persists a user with two decks, then reloads the user and checks that both deck relationships and their user_id values are correct.

### test_deck_slug_is_unique
Checks that inserting a second deck with a slug already in use fails with a database integrity error.

### test_question_deck_cascade_delete
Checks that deleting a deck through the ORM also deletes its associated questions.

### test_sqlite_foreign_keys_are_enabled
Checks that the test database uses SQLite and that SQLite foreign-key enforcement is enabled on its connection.

### test_question_requires_existing_deck
Checks that the database rejects a question whose deck_id refers to no existing deck.

### test_question_answer_must_be_a_valid_option
Checks that the database rejects a question whose answer is outside the allowed A-D options.

### test_question_required_fields_cannot_be_null
Runs once with answer set to null and once with deck_id set to null, checking that the database rejects each missing required value.

### test_deleting_user_deletes_decks_and_questions
Checks that deleting a user through the ORM deletes that user's decks and the questions belonging to those decks.

### test_removing_question_from_deck_deletes_it
Checks that removing one question from a deck's questions relationship deletes that question while leaving another question intact.
