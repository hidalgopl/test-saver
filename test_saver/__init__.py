import databases
import os

database = databases.Database(os.getenv("DATABASE_URL"))
