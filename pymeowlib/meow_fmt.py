from __future__ import annotations

import json, abc, ast
if not __package__:
    import sys
    from pathlib import Path
    ptop = Path(__file__).parent
    __package__= ptop.name
    # make sure package can be found by search in sys.path
    # so add parent of package root
    # so that <parent>/<name> is the package
    sys.path.append(str(ptop.parent))

# from .extract_sb2 import open_proj_file

# def write_data(proj_p, raw):
#     with open_proj_file('w') as f:  
#         json.dump(proj_p, f)

def is_iterable(v):
    try:
        iter(v)
    except (TypeError, NotImplemented, ValueError):
        return False
    return True


class NodeClassMap:
    def __init__(self):
        self.meow_to_ast = {}
        self._ast_to_cls = None

    def __getitem__(self, item):
        return self.tree_to_cls[item]

    def invalidate(self):
        self._ast_to_cls = None

    def get_cls_for(self, tree_t):
        v = self.tree_to_cls.get(tree_t)
        if v is None:
            raise RuntimeError(f"No Node type for {tree_t.__name__}")

    @property
    def tree_to_cls(self):
        if self._ast_to_cls is not None:
            return self._ast_to_cls
        self._ast_to_cls = {}
        for cls, trees in self.meow_to_ast.items():
            if not is_iterable(trees):
                trees = [trees]
            expanded_trees = []
            for tree in trees:
                expanded_trees.append(tree)
                expanded_trees.extend(tree.__subclasses__())
            self._ast_to_cls.update(dict.fromkeys(expanded_trees, cls))
        return self._ast_to_cls


NODE_CLASSES = NodeClassMap()


def node_class(*for_cls):
    if len(for_cls) == 1 and not issubclass(for_cls[0], ast.AST):
        raise TypeError("@node_class should be use with arguments: "
                        "@nodeclass(cls, ...)")
    def decor(cls):
        NODE_CLASSES.invalidate()
        NODE_CLASSES.meow_to_ast[cls] = for_cls
        return cls
    return decor


class MeowNode(abc.ABC):
    def __init__(self, writer, tree, parent):
        self.writer = writer
        self.ast = tree
        self.parent = parent

    def make_subnode(self, of: type[MeowNode], tree):
        return of(self.writer, tree, self)

    def make_subtree(self, tree):
        return self.make_subnode(NODE_CLASSES.get_cls_for(type(tree)), tree)
    
    @abc.abstractmethod
    def write_data(self):
        pass

    def append_data(self, data):
        pass


@node_class(ast.Module)
class ModuleNode(MeowNode):
    def write_data(self):
        for smt in self.ast.body:
            smt.write_data() ## todo
        
    
class MeowScriptsWriter:
    def __init__(self):
        self.scripts_root = []
        self.current = self.scripts_root

    @property
    def nscripts(self):
        return len(self.scripts_root)

    def add_global_script(self, s):
        self.scripts_root.append(s)

    def write_node(self, node):
        ncls = NODE_CLASSES[type(node)]
        n: MeowNode = ncls(self)
        data = n.get_data()
        
