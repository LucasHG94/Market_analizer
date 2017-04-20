from distutils.core import setup

setup(
    name='market_analizer',
    version='0.1.0',
    packages=['configEx', 'modelsEx'],
    url='',
    license='',
    author='Lucas Hurtado',
    author_email='',
    description='Market analizer',
    install_requires=[
        'Flask==0.11.1',
        'SQLAlchemy==1.1.4',
        'Flask-SQLAlchemy==2.1',
        'SQLAlchemy-Utils==0.32.9',
        'Flask-Principal==0.4.0',
        'Flask-SocketIO==2.7.2',
        'request==2.13.0',
        'lxml==3.7.1'
    ],
    include_package_data=True,
)