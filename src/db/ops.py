
import os

from sqlalchemy import create_engine
from setup import Base, Files, NdtPose
from sqlalchemy.orm import sessionmaker


class Ops:

    def __init__(self):
        bagspath = os.environ['BAGSPATH']
        dbname = 'sqlite:///' + bagspath + '/index.db'        
        engine = create_engine(dbname)
        Base.metadata.bind=engine
        Session = sessionmaker(bind=engine)
        self.session = Session()    

    def exists_file(self, name):
        d = self.session.query(Files).filter_by(name=name).all()
        return len(d) != 0

    def get_file(self, name):
        d = self.session.query(Files).filter_by(name=name).all()
        return d[0]

    def get_file_all(self):
        d = self.session.query(Files).all()
        return d 

    def get_filename_by_id(self,fid):
        d = self.session.query(Files).filter_by(id=fid).all()
        return d[0].name

    def add_file(self,name):
        new_file = Files(name=name)
        self.session.add(new_file)
        self.session.commit()

    def add_ndt_pose(self,fname,max_x,max_y,min_x,min_y): 

        if not self.exists_file(fname):
            self.add_file(fname)

        new_ndt_pose = NdtPose(
            file_id=self.get_file(fname).id,
            position_max_x=max_x,
            position_max_y=max_y,
            position_min_x=min_x,
            position_min_y=min_y,
        )
        self.session.add(new_ndt_pose)
        self.session.commit()

    def get_ndt_pose(self,fname):
        file_id = self.get_file(fname).id
        d = self.session.query(NdtPose).filter_by(file_id=file_id).all()
        return d[0]

