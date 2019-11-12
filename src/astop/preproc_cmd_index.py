

from ast import *



class PreprocCmdIndex(NodeTransformer):
    
    def __init__(self, aa):
        super(PreprocCmdIndex, self).__init__()
        self.f = aa.f

    def visit_Name(self, node):
        if node.id == 'FILTER':

            # set same lineno,col_offset
            self.f.lineno = node.lineno
            self.f.col_offset = node.col_offset
            
            return self.f
        else:
            return node