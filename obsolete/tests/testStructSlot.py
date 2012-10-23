import numpy
from lazyflow import graph
from lazyflow import stype




class GraphType(stype.Struct):
    nodes = graph.Slot(stype = stype.ArrayLike, value = numpy.zeros((10,20)))
    edges = graph.Slot(stype = stype.ArrayLike, value = numpy.ones((10,20)))


class A(graph.Operator):

    tgraph = graph.OutputSlot(stype=GraphType)

    def setupOutputs(self):
        self.tgraph.nodes.meta.shape = (10,20)
        self.tgraph.nodes.meta.dtype = numpy.uint8
        self.tgraph.edges.meta.shape = (10,20)
        self.tgraph.edges.meta.dtype = numpy.uint8


    def execute(self, slot, subindex, roi, result):
        if slot == self.tgraph.nodes:
            result[:] = 0
        elif slot == self.tgraph.edges:
            result[:] = 1



class B(graph.Operator):

    tgraph = graph.InputSlot(stype=GraphType)

    output = graph.OutputSlot(stype=stype.ArrayLike)

    def setupOutputs(self):
        self.output.meta.shape = (1,)

    def execute(self,slot,roi,destination):
        nodes = self.tgraph.nodes[:].allocate().wait()
        assert (nodes==0).all()
        edges = self.tgraph.edges[:].allocate().wait()
        assert (edges==1).all()





g = graph.Graph()
a = A(graph=g)
b = B(graph=g)

b.tgraph.connect(a.tgraph)

b.output[:].allocate().wait()
