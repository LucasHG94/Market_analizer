
from core import init_app

# app = Flask(__name__)
# app.config.from_object(__name__)
#
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'database/market.db'),
#     SECRET_KEY='123',
#     USERNAME='admin',
#     PASSWORD='123'
# ))
# app.config.from_envvar('MARKET_SETTINGS', silent=True)
#
# engine = create_engine('sqlite:///' + app.config['DATABASE'])
# Base = declarative_base()


# @app.route('/')
# def hello_world(self):
#     return 'Hello, World!'
#
#
# def create_ed():
#     Base.metadata.create_all(engine, checkfirst=True)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     ed_user = Company(name='ed')
#     session.add(ed_user)
#     session.commit()
#
#
# def show_data():
#     connection = engine.connect()
#     result = connection.execute("select name from Company")
#     for row in result:
#         print("Nombre:", row['name'])
#     connection.close()

if __name__ == '__main__':
    init_app()
