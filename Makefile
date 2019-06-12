test:
	poetry run python -m pytest --color=yes --cov=fafnir

lint:
	poetry run pylint fafnir

install:
	poetry install

init-screen:
	Xvfb :1 -screen 0 1024x268x16 &

publish:
	poetry build
	poetry publish --username $(PYPI_USERNAME) --password $(PYPI_PASSWORD)

ci: init-screen install lint test
