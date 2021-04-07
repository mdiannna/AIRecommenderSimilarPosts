from PIL import Image
from keras.applications import vgg16
from keras.preprocessing.image import load_img,img_to_array
from keras.models import Model
from keras.applications.imagenet_utils import preprocess_input

from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from img_custom_errors import ModelNotFoundError



class ImageSimilarity:    
    def __init__(self, imgs_path, model_path=None, imgs_model_width = 224, imgs_model_height = 224, nr_similar_imgs=5):
        """ 
        Init class

            Parameters:
            ----------
                imgs_path(str) - the path to folder where images are stored
                model_path (str) [optional] - the path for Image recognition/feature extraction model
                imgs_model_width(int) - the width of images for model
                imgs_model_height(int) - the heights of images for model
                nr_similar_imgs(int) - number of most similar images to retrieve
        """
        self.__model_path = model_path
        # parameters setup

        # imgs_path = "../input/style/"
        if imgs_path[-1]!="/":
            imgs_path += "/"
        self.__imgs_path = imgs_path
        self.__imgs_model_width = imgs_model_width
        self.__imgs_model_height = imgs_model_height

        self.__nr_similar_imgs = nr_similar_imgs


        self.model = self.load_model(model_name='vgg16', from_keras=True)

        print(self.model.summary())
    
    
    # TODO: parametru metric sa poata fi setat!
    def compute_similarity(self, img_path1, img_path2):
        """ 
        Compute similarity score between 2 images
            Parameters:
            ----------
                img_path1 (str) - path where first image is stored
                img_path2 (str) - path were second image is stored
                nr_similar_imgs(int) - nr of similar images to return

            Returns:
            ----------
                score (float) - the similarity score (TODO: decide unit - percentages or other)
        
        TODO: img_paths sau image ca obiect in PIL de decis
        TODO: decis algoritm (cosine similarity sau jaccard similarity sau Jensen-Shannon distance sau Earth Mover distance etc)
        """

        score = 0

        #TODO: check if it is in db, if not, extract features
        img1_features = self.extract_features(self.model, img_path1)
        img2_features = self.extract_features(self.model, img_path2)

        print("img1 features:", img1_features, "shape: ", img1_features.shape)
        print("img2 features:", img2_features, "shape: ", img2_features.shape)

        arr_features = np.array([img1_features, img2_features])
        arr_features = arr_features.reshape(2, arr_features.shape[2])
        print("arr features:", arr_features)
        
        print("arr features shape:", arr_features.shape)

        # TODO: try catch or return 0 if error
        cosSimilarities = cosine_similarity(arr_features)
        score = cosSimilarities[0][1]
       
        return score     
    
    
    #TODO: finish this function!!!
    def compute_similarity_batch(self, imgs_features):
        # compute cosine similarities between images

        cosSimilarities = cosine_similarity(imgs_features)

        # store the results into a pandas dataframe

        cos_similarities_df = pd.DataFrame(cosSimilarities, columns=files, index=files)
        cos_similarities_df.head()

        #TODO: finish this function!!!


    def get_most_similar(self, img_path, nr_similar_imgs=3):
        """ 
        Get the most similar images to the image specified in img_path
            Parameters:
            ----------
                img_path (str) - path where the image is stored
                nr_similar_imgs (int) - how many top similar images to return (by default 3) TODO: parametru la functie sau la clasa!!! decis!
            Returns:
            ----------
                results (list of dictionaries) - a list of similar images with their similarity score, in the form
                    [{"similar_image": "path"(str), "score": float},  .... ]        
        TODO: img_paths sau image ca obiect in PIL de decis
        """
        
        if nr_similar_imgs!=None:
            self.__nr_similar_imgs = nr_similar_imgs

        score = 0

       
        #TODO: later, additionally to img_path add a list of potential images, not to search through all of them!!
        imgs_to_compare = [self.imgs_path + x for x in os.listdir(self.imgs_path) if ("png" in x) or ("jpg" in x)or ("jpeg" in x)]
        print("imgs_to_compare[0]:", imgs_to_compare[0])
        print("number of images:",len(imgs_to_compare))

        # features = self.extract_features(self.model, imgs_to_compare[0])
        base_img_features = self.extract_features(self.model, img_path)
        print("base_img features:", base_img_features)
        

        # TODO: next implement

        #TODO: implement
        raise NotImplementedError


    def load_model(self, model_name='vgg16', from_keras=True):
        """ 
        Load model for image similarity
            Parameters:
            ----------
                model_name(str) - the name of the model to load
                from_keras(bool) - specifies if the model loads from keras or not
        """
        if from_keras==True and model_name.lower() =='vgg16':
            # load the model
            vgg_model = vgg16.VGG16(weights='imagenet')

            # remove the last layers in order to get features instead of predictions
            feat_extractor = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc2").output)
        
            return feat_extractor
        #else
        # TODO: implement loading from custom model_path!!
        # self.model_path(str) [optional] - specifies the model_path if from_keras is false TODO: implement

        raise ModelNotFoundError

    # TODO: set model as internal class parameter???
    def extract_features(self, model, img_path):
        """ Extract features using model from one image path"""

        # load an image in PIL format
        original = load_img(img_path, target_size=(self.imgs_model_width, self.imgs_model_height))
        
        # show img
        # plt.imshow(original)
        # plt.show()
        print("image loaded successfully!")

        # convert the PIL image to a numpy array
        numpy_image = img_to_array(original)

        # convert the image / images into batch format
        # expand_dims will add an extra dimension to the data at a particular axis
        # we want the input matrix to the network to be of the form (batchsize, height, width, channels)
        # thus we add the extra dimension to the axis 0.
        image_batch = np.expand_dims(numpy_image, axis=0)
        print('image batch size', image_batch.shape)

        # prepare the image for the VGG model
        img_processed = preprocess_input(image_batch.copy())


        # get the extracted features
        img_features = model.predict(img_processed)

        print("features successfully extracted!")
        print("number of image features:",img_features.size)
        return img_features


    # TODO: acest proces se face doar la inceput, sau pentru fiecare imagine individual si se salveaza/updateaza in db,
    # in asa mod nu va fi complexitate mare si timp mare
    #TODO: se poate de facut functie import_images cu mai multe imagini, dar nush daca trebuie
    #TODO!!! fiecare user trebuie sa aiba separat folderul de fisiere/ bd 
    def extract_features_list_imgs(self, model, imgs_paths_lst):
        """ Extract features for all the image paths from a list """
        # load all the images and prepare them for feeding into the CNN

        imported_images = []

        for img_path in imgs_paths_lst:
            original = load_img(img_path, target_size=(self.imgs_model_width, self.imgs_model_height))
            np_image = img_to_array(original)
            image_batch = np.expand_dims(np_image, axis=0)
            
            imported_images.append(image_batch)
            
        imgs = np.vstack(imported_images)

        processed_imgs = preprocess_input(imgs.copy())

        # extract the images features

        imgs_features = model.predict(processed_imgs)

        print("features successfully extracted!")
        imgs_features.shape

        return imgs_features

    @property
    def model_path(self):
        return self.__model_path
    
    @property
    def imgs_path(self):
        return self.__imgs_path

    @property
    def model_path(self):
        return self.__model_path

    @property
    def imgs_model_width(self):
        return self.__imgs_model_width 
    
    @property
    def imgs_model_height(self):
        return self.__imgs_model_height
    
    @property
    def nr_similar_imgs(self):
        return self.__nr_similar_imgs
    

    @model_path.setter
    def model_path(self, model_path):
        self.__model_path = model_path
    

    #TODO:add setters as needed!
