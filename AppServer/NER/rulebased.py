from termcolor import colored
import os
from nltk.tokenize import word_tokenize
import string
import re


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
        """ 
        Extract field from text according to files containing list of options
            Parameters:
            -----------
            text(str) - text from which to extract fields
            options_filename(str) - the name of the file containing list of options
            options_folder(str) - the name of the folder containing options file
            verbose(bool) - True to show more output, False for less output

            Returns:
            -----------
            extracted(list of str) - list of extracted fields from text            
        """

        extracted = []
        
        #TODO: make this code better!
        if options_folder=='options/':
            script_dir = os.path.dirname(__file__) 
            rel_path = "options/"
            options_folder = os.path.join(script_dir, rel_path)

        f = open(options_folder + options_filename)
        options = f.readlines()

        options = [x.lower().replace('\n', '').strip() for x in options]

        # TODO: test if ok options_extended
        options_extended = options
        for option in options:
            if ' ' in option:
                options_extended.append(option.split(' ')[0])

        for word in word_tokenize(text):
            if verbose:
                print(colored(word, "green"))

            # TODO: use smth like fuzzy_matching
            if word.lower().strip().translate(str.maketrans('', '', string.punctuation)) in options_extended:
                extracted.append(word)

        # TODO: add logging
        if verbose:
            print(colored("---options:", "blue"), options_extended)
            print(colored("---options_extended:", "blue"), options_extended)

        return extracted
    
    def extract_field_from_regex(self, text, regex_filename, regex_folder='regex/', verbose=False):
        """ 
        Extract field from text according to files containing regular expressions
            Parameters:
            -----------
            text(str) - text from which to extract fields
            regex_filename(str) - the name of the file containing regex
            regex_folder(str) - the name of the folder containing regex file
            verbose(bool) - True to show more output, False for less output

            Returns:
            -----------
            extracted(list of str) - list of extracted fields from text            
        """

        extracted = []
        
        #TODO: make this code better!
        if regex_folder=='regex/':
            script_dir = os.path.dirname(__file__) 
            rel_path = "regex/"
            regex_folder = os.path.join(script_dir, rel_path)

        f = open(regex_folder + regex_filename)
        options_regex = f.readlines()

        if verbose:
            print(colored("options_regex:", "blue"), options_regex)

        for reg in options_regex:
            reg = reg.replace("\n", "").replace("\\\\", '\\')


            pattern = re.compile(reg)
            if verbose:
                print(colored("reg:", "blue"), reg)
                print(colored("compiled pattern:", "blue"), pattern)

            i = 0
            for line in text.split("\n"):
                if verbose:
                    print(colored("line:", "yellow"), line)
                
                for match in re.finditer(pattern, line):
                    if verbose:
                        print (colored('Found on line %s: %s' % (i+1, match.group()), "green"))
                    extracted.append(match.group())
                i+=1

        return extracted


    def extract_field(self, text, field_name, extraction_type, filename, folder="", verbose=False):
        """
        Extract field from text
            Parameters:
            -----------
                text(str) - the text to be analyzed
                field_name(str) - the name of field to return
                extraction_type(str) - can be either 'options' or 'regex'
                filename(str) - the name of the file containing option or regex
                folder(str) - the name of the folder containing file for option or regex
                verbose(bool) - True to show more output, False for less output
        """
        result = []

        if extraction_type=="options":
            if folder=="":
                options_folder = "options/"
            extracted = self.extract_field_from_options(text, filename, options_folder, verbose)
        
        elif extraction_type=="regex":
            if folder=="":
                regex_folder = "regex/"
            extracted = self.extract_field_from_regex(text, filename, regex_folder, verbose)
        
        else:
            print(colored("!Error! extraction_type should be either 'options' or 'regex'", 'red'))
            extracted = []
        
        for item in extracted:
            result.append({item:field_name})
        
        return result


    def extract_breed(self, text, field_name="breed", options_filename="rase_caini.txt", options_folder="options/", verbose=False):
        """ 
        Extract breed field from text (name of field depends on language) 
            Parameters:
            -----------
                text(str) - the text to be analyzed
            Returns:
            -----------
                result - list of dictionaries in the form {word:field} 
        """
        result = []

        if self.language=="ro":
            field_name = "rasa"
        
        extracted = self.extract_field_from_options(text, options_filename, options_folder, verbose)
        
        for item in extracted:
            result.append({item:field_name})

        return result
    
    def extract_animal_type(self, text, field_name="animal_type", options_filename="specie_animal.txt", options_folder="options/", verbose=False):
        """ 
        Extract animal type (species) field from text (name of field depends on language) 
            Parameters:
            -----------
                text(str) - the text to be analyzed
            Returns:
            -----------
                result - list of dictionaries in the form {word:field} 
        """
        result = []

        if self.language=="ro":
            field_name = "specie_animal"
        
        extracted = self.extract_field_from_options(text, options_filename, options_folder, verbose)
        
        for item in extracted:
            result.append({item:field_name})

        return result

    def extract_phone(self, text, field_name="phone", regex_filename="telefon.txt", regex_folder="regex/", verbose=False):
        """
        Extract phone field from text (name of field depends on language)
            Parameters:
            -----------
                text(str) - the text to be analyzed
            Returns:
            -----------
                result - list of dictionaries in the form {word:field}
        """
        result = []

        if self.language=="ro":
            field_name = "telefon"
        
        extracted = self.extract_field_from_regex(text, regex_filename, regex_folder, verbose)
        
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