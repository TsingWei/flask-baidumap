from sqlalchemy import Column,  create_engine, Integer, Float, DateTime,INT,desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

# 创建对象的基类:
Base = declarative_base()



class SQLConnection:

    # 定义LocationStamp对象:
    class LocationStamp(Base):
        __tablename__ = 'Locations'
        # 表的结构:
        id = Column(INT, primary_key=True)
        time =   Column(DateTime)
        lati =  Column(Float) 
        longi = Column(Float)

    def __init__(self):
        # 初始化数据库连接:
        engine = create_engine('mysql+mysqlconnector://moe:123456@localhost:3306/IOT')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def addStamp(self, lati, longi):
        # dateTime_p = datetime.datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
        new_user = self.LocationStamp( time=datetime.datetime.now(),lati=lati,longi=longi)
        self.session.add(new_user)
        self.session.commit()
    
    def getNStamp(self, n:int): 
        return self.session.query(self.LocationStamp).order_by(desc('time')).limit(n)

    def __del__(self):
        # 关闭session:
       self.session.close()



if __name__ == '__main__':

    s = SQLConnection()
    # s.addStamp(3.4444,55.34)
    for stamp in s.getNStamp(5):
        print(stamp.lati)
