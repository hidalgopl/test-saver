import databases
import os

__version__ = '0.1.0'
database = databases.Database(os.getenv("DATABASE_URL"))
