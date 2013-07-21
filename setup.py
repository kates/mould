from setuptools import setup, find_packages

setup(
        name="mould",
        version="0.1",
        packages=find_packages(),
        package_data={
                "mould": ["*.tpl"],
                },
        install_requires=[
                "Flask",
                "Flask-Script",
                "Flask-Testing",
                "alembic",
                "gunicorn",
                "sqlalchemy"
                ],
        )

