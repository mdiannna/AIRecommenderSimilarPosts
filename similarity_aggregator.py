from post import Post
from termcolor import colored
from text_module import TextModule
from ImageSimilarityModule.imagesimilarity import ImageSimilarity

class SimilarityAggregator():
    # TODO: add text config_path param to be used in text module when using this class
    def __init__(self, weight_text='auto', weight_image='auto', text_module_config_path='configurations/config.xml', image_module=None):
        
        if image_module==None:
            self.img_module = ImageSimilarity() 
        else:
            self.img_module = image_module
        self.text_module = TextModule(config_path=text_module_config_path)

        self.set_weights(weight_image, weight_text)        


    # TODO: test!
    def calc_similarity_posts(self, post1, post2, extended_result=False):
        """ 
        Calculate similarity score between 2 posts 
        --------
        parameters:
            - post1(Post) - the first post to compare
            - post2(Post) - the second post to compare
            - extended_result(bool) - if True will return a dictionary with more params, as img_score, text_score and weights
        --------
        returns:
            - result (fload or dict) - if extended_result is True then dict, else the calculated score as float
        """
        
        text1 = post1.text
        text2 = post2.text
        img1 = post1.image
        img2 = post2.image

        return self.calc_similarity(text1, img1, text2, img2)


    def calc_similarity(self, text1, img_path1, text2, img_path2, extended_result=False):
        """ 
        Calculate similarity score between 2 posts 
        --------
        parameters:
            - text1(str) - text of the first post to compare
            - text2(str) - text of the second post to compare
            - img_path1(str) - the path to the image of the first post to compare
            - img_path2(str) - the path to the image of the second post to compare
            - extended_result(bool) - if True will return a dictionary with more params, as img_score, text_score and weights
        --------
        returns:
            - result (fload or dict) - if extended_result is True then dict, else the calculated score as float
        """
        
        text_similarity = self.text_module.calc_similarity(text1, text2)
        print("text similarity (jaccard):", text_similarity)
        print(type( text_similarity))

        img_similarity = self.img_module.calc_similarity(img_path1, img_path2)
        print("image similarity score:", img_similarity)
        print(type(img_similarity))

        print(type(self.__weight_image))

        aggregated_similarity = self.__weight_image*img_similarity + self.__weight_text*text_similarity
        print("aggregated_similarity:", aggregated_similarity)

        if extended_result:
            return {"aggregated_similarity":aggregated_similarity, 
                    "text_similarity":text_similarity, 
                    "image_similarity":img_similarity, 
                    "weight_text":self.__weight_text,
                    "weight_image":self.__weight_image}
        # else
        return aggregated_similarity


    # #TODO; should include also existing fields!!!
    # def get_similar_posts_by_features(img_features, text, max_similar_posts, all_img_features,fields=None):

        
    
    # imag_path & text params because post is not yet in the system
    def get_similar_posts(image_path, text, max_similar_posts):
        # TODO
        print(colored("----Similarity Aggregator-----", "yellow"))
        
        print(colored("Image received:" + str(image_path), "blue"))
        print(colored("Text received:" + str(text), "blue"))

        raise NotImplementedError
        return {"result": "not yet implemented!"}


    def set_weights(self, weight_text="auto", weight_image="auto"):
        """ 
        set the weights for the NER module and Rule-Based modules
        ----------
        parameters:
            - weight_text (float or 'auto') - the importance of the NER module in the final result
            - weight_image (float or 'auto') - the importance of the rule-based module in the final result
        """
        # TODO: check the sum of weights to be 1
        if weight_text=='auto':
            self.__weight_text = 0.5
        else:
            self.__weight_text = weight_text

        if weight_image=='auto':
            self.__weight_image = 0.5
        else:
            self.__weight_image = weight_image


if __name__=="__main__":
    # sa = SimilarityAggregator()
    sa = SimilarityAggregator(text_module_config_path='configurations/config.xml')


    text1 = """S-a perdut in com.Tohatin, caine de rasa ,,BEAGLE,,, mascul pe nume ,,KAY,,"""
    # text2 = "cainele de rasa beagle s-a pierdut"
    text2 = "caine de rasa beagle s-a pierdut"

    img_folder = 'ImageSimilarityModule/images/'
    img_path1 = img_folder + "abysinian1.jpg"
    img_path2 = img_folder + "abysinian4.jpeg"

    print("---- final aggregated similarity:--")
    print(sa.calc_similarity(text1, img_path1, text2, img_path2))
    print(sa.calc_similarity(text1, img_path1, text2, img_path2, extended_result=True))
