
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:Mohamedaasif1@localhost:5432/student_management_fastapi"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from models.student_model import Student
    from models.fees_model import Fee
    from models.user_model import User

    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        # Add combined fee columns to the existing students table.
        connection.execute(text("""
            ALTER TABLE students
            ADD COLUMN IF NOT EXISTS fee_id INTEGER
        """))

        connection.execute(text("""
            ALTER TABLE students
            ADD COLUMN IF NOT EXISTS total_fees INTEGER
        """))

        connection.execute(text("""
            ALTER TABLE students
            ADD COLUMN IF NOT EXISTS paid_fees INTEGER
        """))

        connection.execute(text("""
            ALTER TABLE students
            ADD COLUMN IF NOT EXISTS pending_fees INTEGER
        """))

        # Copy active fee details into the students table.
        connection.execute(text("""
            UPDATE students AS s
            SET
                fee_id = f.id,
                total_fees = f.total_fees,
                paid_fees = f.paid_fees,
                pending_fees = f.pending_fees
            FROM fees AS f
            WHERE s.id = f.student_id
              AND s.is_deleted = FALSE
              AND f.is_deleted = FALSE
        """))

        # Clear fee details when a student has no active fee record.
        connection.execute(text("""
            UPDATE students AS s
            SET
                fee_id = NULL,
                total_fees = NULL,
                paid_fees = NULL,
                pending_fees = NULL
            WHERE NOT EXISTS (
                SELECT 1
                FROM fees AS f
                WHERE f.student_id = s.id
                  AND f.is_deleted = FALSE
            )
        """))

    inspector = inspect(engine)

    print("Database connected successfully!")
    print("Tables:", inspector.get_table_names())
    print("Views:", inspector.get_view_names())

    print("Student columns:", [
        column["name"]
        for column in inspector.get_columns("students")
    ])

    print("Fees columns:", [
        column["name"]
        for column in inspector.get_columns("fees")
    ])


if __name__ == "__main__":
    try:
        create_tables()

        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT
                        id,
                        name,
                        age,
                        course,
                        fee_id,
                        total_fees,
                        paid_fees,
                        pending_fees
                    FROM students
                    ORDER BY id
                """)
            )

            print("\nStudent + Fees Data:")
            for row in result:
                print(row._mapping)

    except Exception as error:
        print("Database operation failed:", error)
