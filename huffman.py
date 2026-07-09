import heapq
import sys

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

def build_heap(frequency):
    heap = []
    for char in frequency:
        node = Node(char, frequency[char])
        heapq.heappush(heap, node)
    return heap

def build_tree(heap):
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(root, current_code, codes):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
        return
    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)

def get_codes(root):
    codes = {}
    generate_codes(root, "", codes)
    return codes

def encode_text(text, codes):
    encoded = ""
    for char in text:
        encoded += codes[char]
    return encoded

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_text

def get_byte_array(padded_encoded_text):
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

def compress(path):
    with open(path, 'r') as file:
        text = file.read()
    
    frequency = build_frequency_table(text)
    heap = build_heap(frequency)
    root = build_tree(heap)
    codes = get_codes(root)
    encoded_text = encode_text(text, codes)
    padded_encoded_text = pad_encoded_text(encoded_text)
    b = get_byte_array(padded_encoded_text)
    
    output_path = path + ".bin"
    with open(output_path, 'wb') as output:
        output.write(bytes(b))
    
    return output_path

def get_bit_string(padded_encoded_text):
    bit_string = ""
    for byte in padded_encoded_text:
        bits = bin(byte)[2:].zfill(8)
        bit_string += bits
    return bit_string

def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    padded_encoded_text = padded_encoded_text[8:]
    if extra_padding == 0:
        encoded_text = padded_encoded_text
    else:
        encoded_text = padded_encoded_text[:-extra_padding]
    return encoded_text

def decode_text(encoded_text, root):
    decoded = ""
    current = root
    for bit in encoded_text:
        if bit == "0":
            current = current.left
        else:
            current = current.right
        if current.left is None and current.right is None:
            decoded += current.char
            current = root
    return decoded

def decompress(path):
    with open(path, 'rb') as file:
        bit_string = get_bit_string(file.read())
    
    encoded_text = remove_padding(bit_string)
    
    frequency = build_frequency_table(open(path.replace('.bin', ''), 'r').read())
    heap = build_heap(frequency)
    root = build_tree(heap)
    
    decoded_text = decode_text(encoded_text, root)
    
    output_path = path.replace('.bin', '_decompressed.txt')
    with open(output_path, 'w') as output:
        output.write(decoded_text)
    
    return output_path

if __name__ == "__main__":
    if sys.argv[1] == "compress":
        compress(sys.argv[2])
        print("File compressed successfully")
    elif sys.argv[1] == "decompress":
        decompress(sys.argv[2])
        print("File decompressed successfully")