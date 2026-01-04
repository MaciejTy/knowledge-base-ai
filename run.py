from app import create_app, db
from app.models import Document

app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in flask shell"""
    return {'db': db, 'Document': Document}

if __name__ == '__main__':
    app.run()