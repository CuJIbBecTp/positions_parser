import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker


class Datahouse:
    def __init__(self, base, db_uri):
        self.base = base
        self.engine = sqla.create_engine(db_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.connection = self.engine.connect()

    def create(self):
        self.base.metadata.create_all(self.engine)

    def drop(self):
        self.base.metadata.drop_all(self.engine)

    def get_or_create(self, model, **kwargs):
        """avoid duplicates in db"""
        instance = self.get_instance(**kwargs)
        if instance is None:
            print(f"The new position of {kwargs['title']} will be added to the database")
            self.create_instance(model, **kwargs)
        else:
            print(f'The position of {instance[0]} already exists in a database')
            return

    def create_instance(self, model, **kwargs):
        """create instance and add it to db"""
        instance = model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return True

    def get_instance(self, **kwargs):
        """return first instance found"""
        query = sqla.text(f"SELECT title FROM positions WHERE title='{kwargs['title']}' AND department='{kwargs['department']}'")
        result_proxy = self.connection.execute(query)
        result_set = result_proxy.fetchall()
        if result_set:
            return result_set
        else:
            return

    def get_content(self, model, columns=['id', 'title', 'department']):
        sql_query = sqla.text(f"SELECT {', '.join(columns)} FROM {model.__tablename__}")
        result_proxy = self.connection.execute(sql_query)
        result_set = result_proxy.fetchall()
        return result_set