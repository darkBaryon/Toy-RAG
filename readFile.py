
from genericpath import isdir
from math import e
import os
import sys

class ReadFile:
    
    '''
    A class to read and process text files in a folder.

    Parameters
    ----------
    folder_path : str
        The path of the folder containing the text files.

    Attributes
    ----------
    folder_path : str
        The path of the folder containing the text files.
    text_dict : dict
        A dictionary where keys are filenames and values are text contents.

    Methods
    -------
    get_text_content()
        Read and return the text_dict of all files in a folder.
    split_text_into_chunks()
        Split the text content of a dictionary into chunks of size not exceeding 128.
        The chunks have an overlap of 32 characters.
        
    '''
    def __init__(self, path = None, query = None):
        
        self.path = path
        self.query = query
        self.text = ''
        
    def get_text_content(self):

        if self.query:
            self.text = self.query
            return self.query
        with open(self.path, 'r', encoding='utf-8') as file:
            self.text = file.read()
            return file.read()
            
    def split_text_into_chunks(self, chunk_size = 128, overlap = 20):
        """
        Split the text content of a dictionary into chunks of size not exceeding 128.
        The chunks have an overlap of 32 characters.

        Args:
            text_dict (dict): A dictionary where keys are filenames and values are text contents.

        Returns:
            list: A list of chunks.
        """
        chunks = []
        self.get_text_content()
        
        while len(self.text) > chunk_size:
            chunk = self.text[:chunk_size]
            chunks.append(chunk)
            self.text = self.text[chunk_size - overlap:]
        if self.text:
            chunks.append(self.text)
        return chunks

#*************  ✨ Codeium Cocodeium configcodeium configmmand ⭐  *************/
if __name__ == '__main__':
    
    folder_path = os.path.join(os.path.dirname(__file__), "database/rawFile/差旅费管理/上海交通大学差旅费管理暂行办法.txt")
    
    data = ReadFile(folder_path)
    
    chunks = data.split_text_into_chunks()
    
    for chunk in chunks:
        print(chunk[:], len(chunk))
        print('---')
        
    print(len(chunks))
