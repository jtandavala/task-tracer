from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from src.task.infrastructure.task_model import mapper_registry, start_mappers


class DatabaseConnection:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.session = None

    def setup(self, database):
        self.engine = create_engine(database)
        mapper_registry.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        start_mappers()

    def create_session(self):
        if not self.session:
            self.session = self.session_factory()
        return self.session

    def teardown(self):
        if self.session:
            self.session.close()
        clear_mappers()
        if self.engine:
            self.engine.dispose()
