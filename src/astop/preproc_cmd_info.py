
from ast import *


class PreprocCmdInfo(NodeTransformer):
    
    def __init__(self, aa):
        super(PreprocCmdInfo, self).__init__()
        self.p = aa.p
        self.topic = aa.topic

    def visit_Name(self, node):
        if node.id == 'TARGET_DIRECTORY':

            self.p.lineno = node.lineno
            self.p.col_offset = node.col_offset
            return self.p

        if node.id == 'TOPIC':

            self.topic.lineno = node.lineno
            self.topic.col_offset = node.col_offset
            return self.topic

        else:
            return node