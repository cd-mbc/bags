

import os
from collections import namedtuple

from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from geoalchemy2 import Geometry
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker


import ops

Base = declarative_base()


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

class Files(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        nt_Files = namedtuple('nt_Files',['name'])
        return nt_Files(name=self.name)


class NdtPose(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    geom = Column(Geometry(geometry_type='POLYGON', management=True))

    @property
    def serialize(self):
        nt_NdtPose = namedtuple('nt_NdtPose',['file_name'])       
        print ops.Ops().st_contains(0,1)
        return nt_NdtPose(
            file_name=ops.Ops().get_filename_by_id(self.file_id),
        )


def initizlize():
    conn = engine.connect()
    conn.execute(select([func.InitSpatialMetaData()]))
    conn.close()

    Files.__table__.create(engine)
    NdtPose.__table__.create(engine)    


bagspath = os.environ['BAGSPATH']
dbname = 'sqlite:///' + bagspath + '/index.db'
engine = create_engine(dbname)
listen(engine, 'connect', load_spatialite)

if not os.path.exists(bagspath + '/index.db'):
    initizlize()