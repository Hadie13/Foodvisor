# -*- coding: utf-8 -*-
"""
Created on thu Sep  29 14:09:09 2020

@author: Hadiza_Mahaman
"""

class TreeNode:

    def __init__(self, ID):
        self.ID = ID
        self.children = []
        self.parent = None
        self.data = None

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = (spaces + '|__' if self.parent else '')
        print (prefix + self.ID + ' level ' + str(self.get_level()) + ' data ' + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class Database(object):

    def __init__(self, ID):
        self.root = TreeNode(ID)

    def add_nodes(self, tuples):
        for node in tuples:
            if self.root.ID == node[1]:
                self.root.add_child(TreeNode(node[0]))
            else:
                if self.root.children:
                    for child in self.root.children:
                        if child.ID == node[1]:
                            child.add_child(TreeNode(node[0]))
                        #self.add_nodes(child)

    def add_extract(self, dicts):
        for key in dicts:
            print(dicts[key])
            if self.root.ID in dicts[key]:
                print("coucou", self.root.ID)
                #self.root.data = key
                if self.root.data == None: self.root.data = key

        for child in self.root.children:
            self.fill_data(child, dicts)


    def fill_data(self, node, dicts):
        for key in dicts:
            if node.ID in dicts[key]:
                print("Ici node ID", node.ID)
                #node.data = key
                if node.data == None: node.data = key
            else:
                if node.children:
                    for child in node.children:
                        #print ("else", child.ID, node.ID)
                        if child.ID in dicts[key]:
                            #child.data = key
                            if child.data == None: child.data = key
                    self.fill_data(child, dicts)

        
    def get_extract_status(self):
 
        status = {}
        if(self.root.children):
            
            for child in self.root.children:
                if(child.data != None): status[child.data] = "granularity_staged"
                for child1 in child.children:
                    if(child1.data != None and len(child1.parent.children) > 1): status[child1.data] = "coverage_staged"
                    if(child1.data != None and len(child1.parent.children) == 1): status[child1.data] = "valid"

        return status


if __name__ == '__main__':

    # Initial graph
    build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]

    # Extract
    extract = {"img001": ["A", "B"], "img002": ["A", "C1"], "img003": ["B", "E"]}

    # Graph edits
    edits = [("A1", "A"), ("A2", "A"), ("C2", "C")]

    # Get status (this is only an example, test your code as you please as long as it works)
    status = {}
    if len(build) > 0:
       # Build graph
       db = Database(build[0][0])
       if len(build) > 1:
         	db.add_nodes(build[1:])
       # Add extract
       db.add_extract(extract)
       # Graph edits
       db.add_nodes(edits)
       print (db.root.print_tree())
       # Update status
       status = db.get_extract_status()
    print(status)    		


