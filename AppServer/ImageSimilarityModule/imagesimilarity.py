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
        self.__imgs_path = imgs_path
        self.__imgs_model_width = imgs_model_width
        self.__imgs_model_height = imgs_model_height

        self.__nr_similar_imgs = nr_similar_imgs
    
    
    def compute_similarity(self, img_path1, img_path2, nr_similar_imgs=None):
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

        if nr_similar_imgs!=None:
            self.nr_similar_imgs = nr_similar_imgs

        score = 0

        model = self.load_model(model_name='vgg16', from_keras=True)

        print(model.summary())

        # TODO: next implement

        raise NotImplementedError

        # TODO:Implement
        return score     
        


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

        model = self.load_model(model_name='vgg16', from_keras=True)

        print(model.summary())

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
