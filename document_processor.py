
import os
import sys
from config import Config

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
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
        
    def get_text_content(self):
        """Get text content.

        If query parameter exists, return query directly; otherwise read file content.

        Returns:
            str: Text content
        Raises:
            FileNotFoundError: If file does not exist
            IOError: If error occurs while reading file
        """
        if self.query:
            self.text = self.query
            return self.query
        
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(Config.ERROR_MESSAGES["path_not_exist"].format(self.path))
                
            with open(self.path, 'r', encoding='utf-8') as file:
                self.text = file.read()
                return self.text
        except IOError as e:
            raise IOError(f"Error reading file {self.path}: {str(e)}")
            
    def split_text_into_chunks(self):
        """
        Split the text content into chunks using configured chunk size and overlap.

        Returns:
            list: A list of text chunks.
        Raises:
            ValueError: If text content is empty
        """
        try:
            text = self.get_text_content()
            if not text.strip():
                raise ValueError("Empty text content")
                
            chunks = []
            remaining_text = text
            
            while len(remaining_text) > self.chunk_size:
                chunk = remaining_text[:self.chunk_size]
                chunks.append(chunk)
                remaining_text = remaining_text[self.chunk_size - self.chunk_overlap:]
                
            if remaining_text:
                chunks.append(remaining_text)
                
            return chunks
        except Exception as e:
            raise Exception(f"Error splitting text into chunks: {str(e)}")

#*************  ✨ Codeium Cocodeium configcodeium configmmand ⭐  *************/
if __name__ == '__main__':
    
    folder_path = os.path.join(os.path.dirname(__file__), "database/rawFile/差旅费管理/上海交通大学差旅费管理暂行办法.txt")
    
    data = ReadFile(folder_path)
    
    chunks = data.split_text_into_chunks()
    
    for chunk in chunks:
        print(chunk[:], len(chunk))
        print('---')
        
    print(len(chunks))
