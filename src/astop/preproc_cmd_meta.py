

from ast import *



class PreprocCmdMeta(NodeTransformer):
    
    def __init__(self, aa):
        super(PreprocCmdMeta, self).__init__()
        self.f = aa.f
        self.d = aa.d

    def visit_Name(self, node):
        if node.id == 'FILTER':

            # set same lineno,col_offset
            self.f.lineno = node.lineno
            self.f.col_offset = node.col_offset
            
            return self.f
        if node.id == 'TARGET_DIRECTORY':

            self.d.lineno = node.lineno
            self.d.col_offset = node.col_offset
            return self.d
        else:
            return node