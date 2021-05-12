from TextExtractionRuleBased.rulebased import RuleBasedInformationExtractor

class TextModule:
    # TODO: config_path should be not default param
    def __init__(self, config_path='configurations/config.xml', weight_NER='auto', weight_RB='auto'):
        # TODO: check the sum of weights to be 1
        self.set_weights(weight_NER, weight_RB)
        self.__config_path = config_path




    def calc_similarity(self, text1, text2):
        """
        use Jaccard similarity - represents the size of the intersection divided by the size of the union of the sets
        """
        #TODO: implement

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

        intersect_cnt = 0

        for entity in entities1:
            if entity in entities2:
                intersect_cnt += 1

        union_cnt = len(entities1) + len(entities2) - intersect_cnt
        
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
