from post import Post
from termcolor import colored

class SimilarityAggregator():
    def get_similar_posts(self, post, n):
        # TODO
        print(colored("----Similarity Aggregator-----", "yellow"))
        
        print(colored("Image received:" + str(post.image), "blue"))
        print(colored("Text received:" + str(post.text), "blue"))

        return {"result": "not yet implemented!"}