#include <filename>
#include "filename"
import re
import os
from graphviz import Digraph

class FileNode():
    def __init__(self, name, parent=[], children=[]):
        self.name = name
        self.parent =[]
        self.parent+=parent
        self.children=[]
        self.children+=children

    def get_child_nodes(self):
        return self.children

    def get_parent_nodes(self):
        return self.parent

    def insert_children(self,child):
        self.children.append(child)
        return self.children

    def insert_parent(self,parent):
        self.parent.extend(parent)
        return self.parent

    def __str__(self):
        return '{"FileNode":{"name":'+ self.name +'} }\n'

class FileReader():
    @staticmethod
    def regex_search_file(file_name, r_string):
         return [re.findall(r_string,line) for line in open(file_name)]

class CppFileReader():
    @staticmethod
    def get_dependency_info(file_name):
        if file_name.endswith('.cpp') or file_name.endswith('.h'):
            CppIncludes = FileReader.regex_search_file(file_name,r'#include \"(.*)\"') + FileReader.regex_search_file(file_name,r'#include <(.*)>')
            return CppIncludes
        else:
            return []
    
class FileTraveser():
    @staticmethod
    def create_graph(your_dir,file_reader_function):
        print(your_dir)
        graph = []
        for dirpath, dirnames, filenames in os.walk(your_dir):
            for file in filenames:
                print("\nnode:")
                file_node = FileNode(file)
                print(file_node.name)
                file_name = os.path.join(dirpath, file)
                file_dependencies = file_reader_function(file_name)
                for file_dependency in file_dependencies:
                    file_node.insert_parent(file_dependency)
                print("\nparents:")
                print(file_node.get_parent_nodes())
                graph.append(file_node)
                print("\n\n\n")
        return graph
                    
graph1 = FileTraveser.create_graph(os.getcwd(),CppFileReader.get_dependency_info)
dot = Digraph(comment='cpp dependency', filename='cpp.gv',
            node_attr={'color': 'lightblue2', 'style': 'filled'})
dot.attr(size='6,6')
for i in range(len(graph1)):
    parents = graph1[i].get_parent_nodes()
    for j in range(len(parents)):
        dot.edge(graph1[i].name ,parents[j])

dot.view()
