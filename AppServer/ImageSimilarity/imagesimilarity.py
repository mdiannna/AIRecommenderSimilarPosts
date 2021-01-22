class ImageSimilarity:    
    def init(self, model_path):
        """ 
        Init class

            Parameters:
            ----------
                model_path (str): specifies the path for Image recognition/feature extraction model
        """
        self.__model_path = model_path
    
    def compute_similarity(self, image_path1, imag_path2):
        """ 
        Compute similarity score between 2 images
            Parameters:
            ----------
                image_path1 (str) - path where first image is stored
                image_path2 (str) - pathe were second image is stored

            Returns:
            ----------
                score (float) - the similarity score (TODO: decide unit - percentages or other)
        
        TODO: image_paths sau image ca obiect in PIL de decis
        TODO: decis algoritm (cosine similarity sau jaccard similarity sau Jensen-Shannon distance sau Earth Mover distance etc)
        """
        score = 0
        raise NotImplementedError

        # TODO:Implement
        return score
        
    
    def get_most_similar(self, image_path, limit=3):
        """ 
        Get the most similar images to the image specified in image_path
            Parameters:
            ---------7-
                image_path (str) - path where the image is stored
                limit (int) - how many top similar images to return (by default 3)
            Returns:
            ----------
                results (list of dictionaries) - a list of similar images with their similarity score, in the form
                    [{"similar_image": "path"(str), "score": float},  .... ]        
        TODO: image_paths sau image ca obiect in PIL de decis
        """
        
        #TODO: implement
        raise NotImplementedError


    @property
    def model_path(self):
        return self.__model_path
    
    @model_path.setter
    def model_path(self, model_path):
        self.__model_path = model_path
    