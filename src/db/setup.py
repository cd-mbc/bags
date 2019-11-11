

import os
from collections import namedtuple

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

import ops

Base = declarative_base()


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
    position_max_x = Column(Float)
    position_max_y = Column(Float)
    position_min_x = Column(Float)
    position_min_y = Column(Float)

    @property
    def serialize(self):
        nt_NdtPose = namedtuple('nt_NdtPose',['file_name','position_max_x', 'position_max_y', 'position_min_x', 'position_min_y'])       
        return nt_NdtPose(
            file_name=ops.Ops().get_filename_by_id(self.file_id),
            position_max_x=self.position_max_x,
            position_max_y=self.position_max_y,
            position_min_x=self.position_min_x,
            position_min_y=self.position_min_y,
        )




bagspath = os.environ['BAGSPATH']
dbname = 'sqlite:///' + bagspath + '/index.db'
engine = create_engine(dbname)
Base.metadata.create_all(engine)

