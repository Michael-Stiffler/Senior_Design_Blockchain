import hashlib
from typing import List
from typing import Tuple
import math


class Node:
    def __init__(self, left, right, value) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()


class MerkleTree:
    def __init__(self, data: List[str]) -> None:
        retData = self.formatData(data)  # will include extra spaces
        self.buildTree(retData)
        self.assembleData(retData)  # assemble fin out without extra spaces

    # combine data with sensID and sentType, correct for non-power 2
    def formatData(self, data: List[str]) -> List[str]:
        twopower = math.ceil(math.log2(len(data)))
        retData = [''] * 2**twopower  # forcing power 2 size
        for x in range(0, len(data)):
            retData[x] += data[x]
        return retData

    # creates leaves, calls recursive node assembly
    def buildTree(self, data: List[str]) -> None:
        leaves: List[Node] = [Node(None, None, Node.hash(e)) for e in data]
        self.root: Node = self.assembleNodes(leaves)

    def assembleNodes(self, nodes: List[Node]) -> Node:
        # recursive tree node assembly
        mid: int = len(nodes) // 2
        if len(nodes) == 1:
            return nodes[0]
        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value))

        left: Node = self.assembleNodes(nodes[:mid])
        right: Node = self.assembleNodes(nodes[mid:])
        value: str = Node.hash(left.value+right.value)

        return Node(left, right, value)

    def printTree(self) -> None:
        self.printTreeRecursion(self.root)

    def printTreeRecursion(self, node) -> None:
        if node != None:
            print(node.value)
            self.printTreeRecursion(node.left)
            self.printTreeRecursion(node.right)

    # store given data as a single string
    def assembleData(self, data: List[str]) -> None:
        assembly = ""
        for x in data:
            if (x != ''):
                assembly += x + "||"
        assembly += self.root.value
        self.assembledData = assembly

    def getRootHash(self) -> str:
        return self.root.value

    def getAssembledData(self) -> str:
        return self.assembledData


# functions to simplify the process of pushing to blockchain and validating.
# data is expected to be an array of strings in the form "timestamp|signature|data"

    # only functionality added for this method of input - we want only one sensor per merkle tree.
def computeMerkleRoot(data: List[str]) -> Tuple[str, str, Node]:
    merk = MerkleTree(data)
    return [merk.getRootHash(), merk.getAssembledData(), merk.root]

    # validate with same data inputs, as well as the originally computed root.


def validateMerkleRoot(sensorID: str, sensorType: str, data: List[str], roothash: str) -> bool:
    merk = MerkleTree(data)
    return (roothash == merk.getRootHash())


def test():
    list = ["Hello", "mister", "Merkle"]
    roothash, ret, node = computeMerkleRoot(list)
    print(roothash)
    print(ret)

    list2 = ["Hello", "mister", "Merkle", "test", "test2"]
    roothash2, ret2, node2 = computeMerkleRoot(list2)
    print(roothash2)
    print(ret2)

    list3 = ["Hello", "mister", "Merkle"]
    roothash3, ret3, node3 = computeMerkleRoot(list3)
    print(roothash3)
    print(ret3)

    print(validateMerkleRoot("ID1", "TestSensor", list, roothash))
    print(validateMerkleRoot("ID1", "TestSensor", list, roothash2))
    print(validateMerkleRoot("ID1", "TestSensor", list, roothash3))


if __name__ == "__main__":
    test()
