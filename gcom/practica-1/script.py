"""
``Practica 1: Codigos de Huffman`` module
"""
from collections import Counter #Counter
from functools import total_ordering, reduce
from queue import PriorityQueue
from math import log2

@total_ordering
class HTbase:
    """
    Class used to represent common properties of Huffman nodes
    and leaves.

    ...

    Attributes
    ----------
    - frequency: frequency of the associated node
    """
    def __init__(self, frequency):
        """
        base init
        """
        self.frequency = frequency

    def get_freq(self):
        """
        Getter method for the frequency attribute.
        """
        return self.frequency

    def is_leaf(self):
        """
        Returns wether or not the Huffman node is a leaf.
        """
        raise NotImplementedError("is_leaf() is not defined for base")

    def todict(self):
        """
        Returns a dictionary whose keys are the Huffman Tree
        leaves characters and whose values are the associated
        Huffman code for said character.
        """
        def recursive_helper(node, code):
            if node.is_leaf():
                yield (node.get_char(), code)
            else:
                yield from recursive_helper(node.leftchild, code + '0')
                yield from recursive_helper(node.rightchild, code + '1')

        return dict(recursive_helper(self, ''))

    def __eq__(self, other):
        """
        Overloaded comparison to refer to the frequency attribute.
        """
        return self.frequency == other.frequency

    def __lt__(self, other):
        """
        Overloaded comparison to refer to the frequency attribute.
        """
        return self.frequency < other.frequency

class HTleaf(HTbase):
    """
    Class used to represent a Huffman Tree Leaf

    ...

    Attributes
    ----------
    
    - character: Leaf's associated character.
    - frequency: Frequency of the leaf's associated character.
    """
    def __init__(self, char, freq):
        """
        Parameters
        ----------
        
        - character: Leaf's associated character.
        - frequency: Frequency of the leaf's associated character.
        """
        super().__init__(freq)
        self.character = char

    def get_char(self):
        """
        Getter method for the character attribute.
        """
        return self.character

    def is_leaf(self):
        return True

    def __add__(self, other):
        """
        Overloaded addition to return Huffman's parent node of addends.
        """
        return HuffmanTree(self, other)

class HuffmanTree(HTbase):
    """
    Class used to represent a Huffman Tree

    ...

    
    Attributes
    ----------
    
    - frequency = returns the value of a given leaf or the sum of
    the values for its children for a node.
    - children= returns the node's childrens in a list.
    """
    def __init__(self, lnode, rnode):
        """
        Initializes a node whose frequency is the one of it's children
        added up.

        ...

        Parameters
        ----------
        lnode: Node's left children.
        rnode: NOde's right children.
        """
        super().__init__(lnode.get_freq() + rnode.get_freq())
        self.leftchild = lnode
        self.rightchild = rnode

    @classmethod
    def fromdict(cls, dictionary):
        """
        Uses a priority queue to transform a dictionary of
        {character: frequency} elements to a Huffman Tree.

        example input: d = {'c': 12, 'd': 56}
        example output: HT(HT('c', 12), HT('d', 56))
    
        """
        pq = PriorityQueue()
        
        for character, frequency in dictionary.items():
            pq.put(HTleaf(character, frequency))

        while pq.qsize() >= 2:
            elem1 = pq.get()
            elem2 = pq.get()
            pq.put(cls(elem1, elem2))
            
        return pq.get()

    def __add__(self, other):
        """
        Overloaded addition for creating tree whose children
        are the two addends.
        """
        return self.__init__(self, other)

    def __iter__(self):
        """
        Preorder leaf iterator.
        """
        yield from self.leftchild
        yield from self.rightchild
                 
    def is_leaf(self):
          return False

    def decode(self, bitstring):
        """
        Decode a binary string.

        ...

        Decodes a string compounded by 1's and 0's using a traversal
        algoritm on the Huffman Tree, while its not on a leaf it
        recursively traverses down the tree going left if given a '0'
        or right if given a '1'. Once a leaf is reached it appends the
        associated character to the output string and continues the
        algoritm on the tree's root.

        Input
        -----
        bitstring : string
            A string compounded by 1's and 0's

        Output
        ------
        decoded_string : string
            A string containing the characters associated to the
        decodification of ``bitstring``.
        """
        decoded_string = ''
        current_node = self
        for bit in bitstring:
            if bit == '0':
                current_node = current_node.leftchild
            else:
                current_node = current_node.rightchild
            if current_node.is_leaf():
                decoded_string += current_node.character
                current_node = self
        return decoded_string

def satisfies_shannons_first_theorem(h, l, output=True, sig_figs=4):
    if h - 1 <= l and l <= h + 1:
        if output:
            print((f"\\({round(h - 1, sig_figs)} \\le"
                   f"{round(l, sig_figs)} \\le "
                   f"{round(h + 1, sig_figs)}\\)\n"))
            print("Se cumple el primer teorema de Shannon\n")
            return True
        else:
            return False

def encode(string, code):
    """
    Encode the given string using code as the dictionary.
    """
    return reduce(lambda x, y: x + code[y], string, '')

FILENAME_ES = 'GCOM2023_pract1_auxiliar_esp.txt'
SIG_FIGS = 3

with open(FILENAME_ES, 'r', encoding = "utf8") as ifile:
    es = ifile.read()

tab_es = Counter(es)
ht_es = HuffmanTree.fromdict(tab_es)
d_es = ht_es.todict()
l_es_i = [len(code) * tab_es[letter] for letter, code in d_es.items()]
l_es = (sum(l_es_i), len(es))
h_es_i = [freq / len(es) * log2(freq / len(es)) for freq in tab_es.values()]
h_es = -1 * sum(h_es_i)

FILENAME_EN = 'GCOM2023_pract1_auxiliar_eng.txt'
with open(FILENAME_EN, 'r', encoding = "utf8") as ifile:
    en = ifile.read()

tab_en = Counter(en)
ht_en = HuffmanTree.fromdict(tab_en)
d_en = ht_en.todict()
l_en_i = [len(code) * tab_en[letter] for letter, code in d_en.items()]
l_en = (sum(Len_i), len(en))
h_en_i = [freq / len(en) * log2(freq / len(en)) for freq in tab_en.values()]
h_en = -1 * sum(h_en_i)

print((f"- La longitud media L_esp es \\(\\frac{{{l_es[0]}}}{{{l_es[1]}}}"
       f"\\approx {round(l_es[0] / l_es[1], SIG_FIGS)} \\)\n"))
print(f"- La entropia H_esp es {h_es}]\n")
assert satisfies_shannons_first_theorem(h_es, l_es[0]/l_en[1], SIG_FIGS)
print((f"- La longitud media L_en es \\(\\frac{{{l_en[0]}}}{{{l_en[1]}}}"
       f"\\approx {round(l_en[0] / l_en[1], SIG_FIGS)} \\)\n"))
print(f"- La entropia H_eng es {h_en}\n")
assert satisfies_shannons_first_theorem(h_en, l_en[0]/l_en[1], SIG_FIGS)

x_es = ''
x_en = ''
PALABRA = 'dimension'
for letter in PALABRA:
    x_es += d_en[letter]
    x_en += d_es[letter]

percent_es = int(len(PALABRA*8)/len(x_es)*100)
print(f"\'{palabra}\' compreso con S_Esp es \'{X_es}\'\n")
print(f"sin comprimir es {percent_es}% mas largo")

percent_en = int(len(PALABRA*8)/len(x_en)*100)
print(f"\'{PALABRA}\' compreso con S_Eng es \'{x_en}\'\n")
print(f"sin comprimir es {percent_en}% mas largo")

ENCODED = "0101010001100111001101111000101111110101010001110"
decoded = HT_en.decode(encoded)

print(f"{ENCODED} es \n{decoded}\n"\
      f"Los arboles de Huffman NO son únicos "\
      f"y este apartado está mal planteado.")
