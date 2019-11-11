

from ast import *



class PreprocCmdMkindex(NodeTransformer):
    
    def __init__(self, aa):
        super(PreprocCmdMkindex, self).__init__()
        self.d = aa.d

    def visit_Name(self, node):
        if node.id == 'TARGET_DIRECTORY':

            self.d.lineno = node.lineno
            self.d.col_offset = node.col_offset
            return self.d
        else:
            return node