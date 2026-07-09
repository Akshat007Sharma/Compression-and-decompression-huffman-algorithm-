# Huffman Compression Tool

built this as an assignment from my dad. it compresses and decompresses text files using the huffman coding algorithm. written from scratch in python, no libraries except heapq.

## how to run

compress:
python huffman.py compress yourfile.txt

decompress:
python huffman.py decompress yourfile.txt.bin

## what it does

basically it counts how many times each character appears in the text, builds a tree where rare characters are deeper and frequent ones are at the top, assigns binary codes based on that, and then encodes the whole text using those codes. the compressed file is way smaller than the original.

decompression just reverses the whole thing.

## what i learned

- huffman coding algorithm
- binary trees and how to build them
- heaps and priority queues
- file handling in python
- how compression actually works under the hood
