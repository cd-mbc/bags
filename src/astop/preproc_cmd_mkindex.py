

from ast import *



class PreprocCmdMkindex(NodeTransformer):
    
    def __init__(self, aa):
        super(PreprocCmdMkindex, self).__init__()
        self.p = aa.p

    def visit_Name(self, node):
        if node.id == 'TARGET_DIRECTORY':

            self.p.lineno = node.lineno
            self.p.col_offset = node.col_offset
            return self.p
        else:
            return node