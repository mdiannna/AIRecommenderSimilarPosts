from os import replace
from TextExtractionRuleBased.rulebased import RuleBasedInformationExtractor
import pandas as pd
from nltk.stem import SnowballStemmer
import nltk

class TextModule:
    # TODO: config_path should be not default param
    def __init__(self, config_path='configurations/config.xml', weight_NER='auto', weight_RB='auto'):
        # TODO: check the sum of weights to be 1
        self.set_weights(weight_NER, weight_RB)
        self.__config_path = config_path
        self.__stemmer = SnowballStemmer("romanian")
        

    def stem_text(self, text, verbose=False):
        """ apply Romanian stemmer to get the root of words & return new text with only word roots
        """
        resulted_text = ""
        tokens = nltk.word_tokenize(text)
        
        for idx, token in enumerate(tokens):
            stem = self.__stemmer.stem(token)
            if idx>0:
                resulted_text+=" "
            resulted_text += stem

            if verbose:
                print(token, "=>", stem)
        return resulted_text
    

    def stem_fields(self, fields, verbose=False):
        """ apply Romanian stemmer to get the root of fields & return stemmed fields """

        resulted_fields = []
        
        for field in fields:
            field_name, field_text = list(field.keys())[0], list(field.values())[0]
            stem = self.__stemmer.stem(field_text)
            resulted_fields.append({field_name:stem})
            if verbose:
                print(field_text, "=>", stem)

        return resulted_fields
        

    def remove_ro_diacritics(self, text):
        """ Remove romanian diacritics from text 
        Parameters:
        -----------
            text(str) - the text from which to remove diacritics
        Returns:
        -----------
            new_text(str) - the text with replaced diacritics
        """
        diacritics_map = {
            'ş': 's',
            'ţ': 't',
            'ă': 'a',
            'î': 'i',
            'â': 'a',
        }
        new_text = text

        for char_to_replace, replacement in diacritics_map.items():
            new_text = new_text.replace(char_to_replace, replacement)

        return new_text

    def remove_ro_diacritics_fields(self, fields):
        """ remove romanian diacritics from extracted fields """
        diacritics_map = {
            'ş': 's',
            'ţ': 't',
            'ă': 'a',
            'î': 'i',
            'â': 'a',
        }

        resulted_fields = []
        
        for field in fields:
            field_name, field_text = list(field.keys())[0], list(field.values())[0] 
            new_field_text = field_text

            for char_to_replace, replacement in diacritics_map.items():
                new_field_text = new_field_text.replace(char_to_replace, replacement)
            resulted_fields.append({field_name:new_field_text})

        return resulted_fields


    def preprocess_text(self, text):
        """ 
        Preprocess text before applyong similarity metric.
        Stem then remove diacritics for fields (having texts in Romanian) 
        """
        resulted_text = self.stem_text(text)
        resulted_text = self.remove_ro_diacritics(resulted_text)

        return resulted_text


    def preprocess_fields(self, fields, verbose=False):
        """ Stem then remove diacritics for fields (having texts in Romanian) """
        resulted_fields = []

        diacritics_map = {
            'ş': 's',
            'ţ': 't',
            'ă': 'a',
            'î': 'i',
            'â': 'a',
        }
        
        for field in fields:
            field_name, field_text = list(field.keys())[0], list(field.values())[0]
            new_field_text = field_text

            for char_to_replace, replacement in diacritics_map.items():
                new_field_text = new_field_text.replace(char_to_replace, replacement)

            stem = self.__stemmer.stem(new_field_text)
                
            resulted_fields.append({field_name:stem})

            if verbose:
                print(field_text, "=>", new_field_text)

        return resulted_fields
    


    def calc_similarity(self, text1, text2):
        """
        use Jaccard similarity - represents the size of the intersection divided by the size of the union of the sets
        """

        extracted_fields1 = self.extract_fields(text1, return_standardized=True)
        extracted_fields2 = self.extract_fields(text2, return_standardized=True)

        print("extracted fields1:", extracted_fields1)
        print("extracted fields2:", extracted_fields2)

        status1 = extracted_fields1[1]
        status2 = extracted_fields2[1]


        if status1!="success" or status2!="success":
            return -1

        #else, if success

        entities1 = extracted_fields1[0]
        entities2 = extracted_fields2[0]

        entities1_processed = self.preprocess_fields(entities1, verbose=True)
        entities2_processed = self.preprocess_fields(entities2, verbose=True)

        intersect_cnt = 0

        for entity in entities1_processed:
            if entity in entities2_processed:
                intersect_cnt += 1

        union_cnt = len(entities1_processed) + len(entities2_processed) - intersect_cnt
        
        if union_cnt>0:
            jaccard_score = intersect_cnt / union_cnt
            return jaccard_score    
        else:
            return 0


    def calc_similarity_fields(self, fields1, fields2):
        """
        calcualte similarity between already extracted fields from texts
        use Jaccard similarity - represents the size of the intersection divided by the size of the union of the sets
        """    
        intersect_cnt = 0

        fields1_processed = self.preprocess_fields(fields1, verbose=True)
        fields2_processed = self.preprocess_fields(fields2, verbose=True)

        for entity in fields1_processed:
            if entity in fields2_processed:
                intersect_cnt += 1

        union_cnt = len(fields1_processed) + len(fields2_processed) - intersect_cnt
        
        if union_cnt>0:
            jaccard_score = intersect_cnt / union_cnt
            return jaccard_score    
        else:
            return 0
    

    def extract_fields(self, text, return_standardized=False):
        #TODO: impement combination of rule-based and NER with specified weights

        extractor = RuleBasedInformationExtractor()
        result =  extractor.extract_fidels_from_config(text, self.config_path, verbose=True, return_standardized=return_standardized)


        #TODO: impement combination of rule-based and NER with specified weights next

        return result


    def get_most_similar_by_fields(self, base_fields, all_fields, all_fields_ids, max_similar=3, return_df_similarity=False):
        """ all fields ids - id of the texts/posts from where all_fields are extracted (not including the base_fields id) """
        similarities = []

        # all_fields.append(base_fields)
        # all_fields_ids.append("*base_txt_fields")

        print("base fields:", base_fields)


        for compare_fields in all_fields:
            print("fields;", compare_fields)
            # for compare_fields2 in all_fields:
            sim = self.calc_similarity_fields(base_fields, compare_fields)
            print("similarity:", sim)
            similarities.append(sim)

        # df_similarities = pd.DataFrame(similarities, columns=all_fields_ids, index=all_fields_ids)
        df_similarities = pd.DataFrame(similarities, columns=["similarity_score"], index=all_fields_ids)

        if return_df_similarity:
            return df_similarities

        print("df text similarity:")
        print(df_similarities.head())

        df1 = df_similarities.sort_values('similarity_score',ascending = False).head(max_similar)
        
        # df2 = df1[['*base_txt_fields']]
        dict_similarities = df1.to_dict()


        # if "*base_txt_fields" in dict_similarities:
        if len(dict_similarities)>0:
            return dict_similarities

        # #TODO: try catch return errors???
        return {}



    

    
    def set_weights(self, weight_NER='auto', weight_RB='auto'):
        """ 
        set the weights for the NER module and Rule-Based modules
        ----------
        parameters:
            - weight_NER (float or 'auto') - the importance of the NER module in the final result
            - weight_RB (float or 'auto') - the importance of the rule-based module in the final result
        """
        # TODO: check the sum of weights to be 1
        if weight_NER=='auto':
            self.__weight_NER = 0.5
        else:
            self.__weight_NER = weight_NER

        if weight_RB=='auto':
            self.__weight_RB = 0.5
        else:
            self.__weight_RB = weight_RB

    
    def get_weights(self):
        return self.__weight_NER, self.__weight_RB

    @property
    def config_path(self):
        return self.__config_path
    

    @config_path.setter
    def config_path(self, config_path):
        self.__config_path = config_path
    



        
#TODO use a testing module, library, something
# from text_module import TextModule
if __name__=="__main__":
        
    tm = TextModule()

    # TODO: species like "caine, cainele" should be defined as equivalences!!! (maybe separate file etc)
    text1 = """S-a perdut in com.Tohatin, caine de rasa ,,BEAGLE,,, mascul pe nume ,,KAY,,"""
    # text2 = "cainele de rasa beagle s-a pierdut"
    text2 = "caine de rasa beagle s-a pierdut"


    text_similarity = tm.calc_similarity(text1, text2)
    print("text similarity (jaccard):", text_similarity)


    # print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

    print("-----------get most similar texts:")

    text1 = "caine de rasa beagle s-a pierdut"
    # text2 = """S-a perdut in com.Tohatin, caine de rasa ,,beagle,,, mascul pe nume ,,KAY,, """
    text2 = """S-a perdut in com.Tohatin, caine de rasa ,, beagle ,,,  pe nume ,,KAY,, """
    # text2 = "cainele de rasa beagle s-a pierdut"
    text3 = "caine de rasa siameza s-a pierdut"
    text4 = "câine de rasa buldog s-a pierdut"

    fields1 = tm.extract_fields(text1)[0]
    fields2 = tm.extract_fields(text2)[0]
    fields3 = tm.extract_fields(text3)[0]
    fields4 = tm.extract_fields(text4)[0]

    print("fields1:", fields1)
    print("fields2:", fields2)
    print("fields3:", fields3)
    print("fields4:", fields4)

    ds = tm.get_most_similar_by_fields(fields1, [fields2,fields3,fields4], ["text2", "text3", "text4"])
    # ds = tm.get_most_similar_by_fields(fields1, [fields2,fields3,fields4], ["id_post1", "id_post2", "id_post3"])
    print("dict sim:", ds)

    

    ############# Test text preprocessing:
    
    text7 = "S-a perdut în com.Tohatin, câine de rasă ,, beagle ,,,  pe nume ,,KAY,,"
    fields7 = tm.extract_fields(text7)[0]
    print("fields7:", fields7)

    print("Remove diacritics in text:", tm.remove_ro_diacritics(text7))
    print("Stem text:", tm.stem_text(text7))
    print("Full preprocess text:", tm.preprocess_text(text7))

    print()

    print("Stem fields:", tm.stem_fields(fields7))
    print("Remove diaicritics fields:", tm.remove_ro_diacritics_fields(fields7))
    print("Preprocess text from fields:", tm.preprocess_fields(fields7))
    print("fields7 changed?", fields7)
    