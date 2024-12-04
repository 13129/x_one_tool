[alembic]
alembic init 
alembic revision -m "add db_test"
alembic upgrade head
alembic revision --autogenerate -m "update db_test224"
alembic upgrade head

[poetry]
poetry init
poetry add package
poetry show tree
poetry update package
