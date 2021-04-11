from post import Post
from termcolor import colored

class SimilarityAggregator():
    def __init__(self, weight_text='auto', weight_image='auto'):
        self.__weight_text = weight_text
        self.__weight_image = weight_image
        
    
    def similarity_score(self, post1, post2):
        """ Calculate similarity score between 2 posts """
        #TODO: implement
        raise NotImplementedError

    # imag_path & text params because post is not yet in the system
    def get_similar_posts(image_path, text, max_similar_posts):
        # TODO
        print(colored("----Similarity Aggregator-----", "yellow"))
        
        print(colored("Image received:" + str(image_path), "blue"))
        print(colored("Text received:" + str(text), "blue"))

        return {"result": "not yet implemented!"}