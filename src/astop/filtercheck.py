
from ast import *
import sys

class FilterChecker(NodeVisitor):

    def generic_visit(self,node):
        super(FilterChecker, self).generic_visit(node)

    def visit_Name(self,node):
        selfdef_ids = ['start','end','comp','count','count','size','ver','path','types','topics','msg']
        selfdef_for_index = ['ndt_pose']
        predef_ids = ['True','False','type','int','str','float','double']

        available_ids = selfdef_ids + predef_ids + selfdef_for_index
        if node.id not in available_ids:
            print 'id %s is not available' %(node.id)
            sys.exit()


def check(f):
    a = parse(f)
    
    if len(a.body) != 1:
        print("Error: only one statement is allowed")
        sys.exit()
    
    if a.body[0].__class__ != Expr:
        print("Error: only Expr statement is allowed")
        sys.exit()

    fc = FilterChecker().visit(a)

    return True