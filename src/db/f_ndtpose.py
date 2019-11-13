
import os

from sqlalchemy import create_engine
from setup import Base, Files, NdtPose
from setup import load_spatialite
from sqlalchemy.event import listen
from geoalchemy2 import WKTElement
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker



class FNdtPose:
    def __init__(self):
        __bagspath = os.environ['BAGSPATH']
        __dbname = 'sqlite:///' + __bagspath + '/index.db'        
        __engine = create_engine(__dbname)
        listen(__engine, 'connect', load_spatialite)
        Base.metadata.bind=__engine
        __Session = sessionmaker(bind=__engine)
        self.__session = __Session() 

    def __get_files(self,query):
        return set([ self.__session.query(Files).filter_by(id=data.file_id).first().name for data in query ])

    # available in filter
    def st_contains(self,x,y):
        query = self.__session.query(NdtPose).filter(func.ST_Contains(NdtPose.geom, WKTElement('POINT(%f %f)' %(x,y))))
        return self.__get_files(query)
