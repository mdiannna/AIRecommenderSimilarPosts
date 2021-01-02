from termcolor import colored
import os
from nltk.tokenize import word_tokenize
import string

# TODO: check if output maybe needs to be the same as for NER???
class RuleBasedInformationExtractor():
    """ Class for extracting fields specified in fields_to_extract list from text """

    __allowed_fields = {"breed"}

    def __init__(self, fields_to_extract=[], language="ro"):
        """ 
        Init class

            Parameters:
            ----------
                fields_to_extract (list): a list of strings
                language (str): specifies what language will be used, default Romanian
        """
        self.__fields_to_extract = fields_to_extract
        self.__language = language


    def extract_fields(self, text):
        """
        Extract fields specified in fields_to_extract list from the text and returns results in a list of dictionaries

            Parameters:
            ----------
                fields_to_extract (list): a list of strings

            Returns: 
                result: list of dictionaries  in the form {word:field}
            ----------
        """
        # result = [{"word":"field"}]
        result = []
        

        return result
    
    def extract_field_from_options(self, text, options_filename, options_folder="options/", verbose=False):
        extracted = []
        
        #TODO: make this code better!
        if options_folder=='options/':
            script_dir = os.path.dirname(__file__) 
            rel_path = "options/"
            abs_file_path = os.path.join(script_dir, rel_path)

        f = open(abs_file_path + options_filename)
        options = f.readlines()

        options = [x.lower().replace('\n', '').strip() for x in options]

        # TODO: test if ok options_extended
        options_extended = options
        for option in options:
            if ' ' in option:
                options_extended.append(option.split(' ')[0])

        for word in word_tokenize(text):
            print(colored(word, "green"))

            # TODO: use smth like fuzzy_matching
            if word.lower().strip().translate(str.maketrans('', '', string.punctuation)) in options_extended:
                extracted.append(word)

        # TODO: add logging
        if verbose:
            print(colored("---options:", "blue"), options_extended)
            print(colored("---options_extended:", "blue"), options_extended)

        return extracted

    def extract_breed(self, text, field_name="breed", options_filename="rase_caini.txt", options_folder="options/", verbose=False):
        """ 
        Extract breed field from text (name of field depends on language) 
            Parameters:
            -----------
                text(str) - the text to be analyzed
            Returns:
            -----------
                result: list of dictionaries  in the form {word:field} 
        """
        result = []

        if self.language=="ro":
            field_name = "rasa"
        
        extracted = self.extract_field_from_options(text, options_filename, options_folder, verbose)
        
        for item in extracted:
            result.append({item:field_name})

        return result


    @property
    def fields_to_extract(self):
        return self.__fields_to_extract
    
    @fields_to_extract.setter
    def fields_to_extract(self, fields):
        self.__fields_to_extract = fields

    @property
    def language(self):
        return self.__language
    
    @language.setter
    def language(self, lang):
        self.__language = lang