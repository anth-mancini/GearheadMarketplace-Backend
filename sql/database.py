from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://ec2-34-206-8-52.compute-1.amazonaws.com:5432/d3v9akgqgdr0lf"
SQLALCHEMY_DATABASE_URL = "postgresql://usurmhsrkkzjrb:0a8d4ec36ff2abff343c0426bfe991209d24481d98535d5592cafc830a077d9c@ec2-34-206-8-52.compute-1.amazonaws.com:5432/d3v9akgqgdr0lf"


# include the connect args for sqllte only
# SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
except:
    raise "DB connection error"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()