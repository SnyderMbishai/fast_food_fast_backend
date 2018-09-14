"""Welcome resource."""
# from flask_restful import Resource
from flask import render_template

@app.route('/')
def docs():
    """Display template."""

    return render_template("documentation.html")
