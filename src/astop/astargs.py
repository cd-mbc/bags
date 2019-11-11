

import os
from ast import *
import filtercheck

class AstArgs:

    def __init__(self,args):
        self.args = args
        
        if 'BAGSLIMITED' in os.environ:
            bagslimited = os.environ['BAGSLIMITED']
        else:
            bagslimited = True

        if bool(bagslimited) and hasattr(args, 'f'):
            filtercheck.check(args.f)

    @property
    def src(self):
        bagspath = os.environ['BAGSPATH']
        with open(bagspath + self.args.cmd_path,'r') as f:
            src = f.read()

        return parse(src)

    @property
    def f(self):
        str_filter = self.args.f
        ast_filter = parse(str_filter)
        return ast_filter.body[0].value    

    @property
    def d(self):
        str_td = "'%s'"  %(self.args.d)
        ast_td = parse(str_td)
        return ast_td.body[0].value    

    @property
    def topic(self):
        str_topic = "'%s'"  %(self.args.topic)
        ast_topic = parse(str_topic)
        return ast_topic.body[0].value  