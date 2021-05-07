#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver: 
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        edges = []
        totalLength = 0
        n = destIndex
        while n != self.source:
            try:
                edges.append( (self.prev[n].src.loc, self.prev[n].dest.loc, '{:.0f}'.format(self.prev[n].length)) )
                totalLength += self.prev[n].length
                n = self.prev[n].src.node_id
            except KeyError:
                return {'cost':float('inf'), 'path':[]}
        return {'cost':totalLength, 'path':edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        if use_heap:
            self.heap_Dijkstras()
        else:
            self.array_Dijkstras()
        t2 = time.time()
        return (t2-t1)


    def heap_Dijkstras( self ):
        minHeap = []
        map = {}
        self.makeHeap( minHeap, map, self.network.nodes, self.source )
        self.prev = {}
        #prev[self.network.nodes[self.source].node_id] = None
        while len(minHeap) > 0:
            #print(len(minHeap))
            u = self.deleteMin_h(minHeap, map)
            vertex = self.network.nodes[u[0]]
            for edge in vertex.neighbors:
                distance = u[1] + edge.length
                if self.decreaseKeyMinHeap(minHeap, map, edge.dest.node_id, distance):
                    self.prev[edge.dest.node_id] = edge

    def array_Dijkstras( self ):
        array = []
        self.makeArray(array)
        self.prev = {}
        while len(array) > 0:
            u = self.deleteMin_a(array)
            vertex = self.network.nodes[u[0]]
            for edge in vertex.neighbors:
                distance = u[1] + edge.length
                if self.decreaseKeyArray(array, edge.dest.node_id, distance):
                    self.prev[edge.dest.node_id] = edge



    def minHeapInsert( self, array, dictionary, vertex, distance ):
        array.append([vertex, distance])
        i = len(array)-1
        dictionary[vertex] = i
        while i > 0 and array[(i-1)//2][1] > distance:
            dictionary[vertex] = (i-1)//2
            dictionary[array[(i-1)//2][0]] = i
            array[i], array[(i-1)//2] = array[(i-1)//2], array[i]
            i = (i-1)//2


    def deleteMin_h( self, array, dictionary ):
        dictionary.pop(array[0][0])
        min = array[0]
        array[0], array[len(array)-1] = array[len(array)-1], array[0]
        array.pop()
        i = 0
        indexes = len(array)-1
        print("looping")
        while (2*i)+2 <= indexes:
            print(i)
            if array[(2*i)+1][1] <= array[(2*i)+2][1]:
                dictionary[array[i][0]] = (2*i)+1
                dictionary[array[(2*i)+1][0]] = i
                array[i], array[(2*i)+1] = array[(2*i)+1], array[i]
                i = (2*i)+1
            elif array[(2*i)+2][1] < array[(2*i)+1][1]:
                dictionary[array[i][0]] = (2*i)+2
                dictionary[array[(2*i)+2][0]] = i
                array[i], array[(2*i)+2] = array[(2*i)+2], array[i]
                i = (2*i)+2

        if indexes == (2*i)+1:
            dictionary[array[i][0]] = (2*i)+1
            dictionary[array[(2*i)+1][0]] = i
            array[i], array[(2*i)+1] = array[(2*i)+1], array[i]
            i = (2*i)+1
        return min


    def decreaseKeyMinHeap( self, array, dictionary, vertex, distance ):
        if (dictionary.get(vertex) is not None) and distance < array[dictionary[vertex]][1]:
            i = dictionary[vertex]
            array[i][1] = distance
            while i > 0 and array[(i-1)//2][1] > distance:
                dictionary[vertex] = (i-1)//2
                dictionary[array[(i-1)//2][0]] = i
                array[i], array[(i-1)//2] = array[(i-1)//2], array[i]
                i = (i-1)//2
            return True
        return False

    def makeHeap( self, array, dictionary, nodes, source ):
        for node in nodes:
            self.minHeapInsert(array, dictionary, node.node_id, float('inf'))
        self.decreaseKeyMinHeap(array, dictionary, source, 0)
        print("returned from makeHeap")



    def makeArray(self, array):
        for node in self.network.nodes:
            if node.node_id == self.source:
                array.append([node.node_id, 0])
            else:
                array.append([node.node_id, float('inf')])

    def deleteMin_a(self, array): #Returns an id/distance pair
        minIndex = 0
        for i in range(len(array)):
            if array[i][1] < array[minIndex][1]:
                minIndex = i
        min = array[minIndex]
        array.pop(minIndex)
        return min

    def decreaseKeyArray(self, array, index, distance): #Currently O(n). Fix this if there's time
        for node in array:
            if node[0] == index:
                if distance < node[1]:
                    node[1] = distance
                    return True
        return False