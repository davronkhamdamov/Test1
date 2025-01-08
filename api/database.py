from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = ("postgresql://online-diller_owner:Ed0VmKqJ8rzA@ep-billowing-sky-a7jgksno.ap-southeast-2.aws"
                           ".neon.tech/online-diller?sslmode=require")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()