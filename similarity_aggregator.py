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


    def aggregate_similarities(self, text_similarity, img_similarity):
        aggregated_similarity = self.__weight_image*img_similarity + self.__weight_text*text_similarity
        return aggregated_similarity
        


    # #TODO; should include also existing fields!!!
    # def get_similar_posts_by_features(img_features, text, max_similar_posts, all_img_features,fields=None):

        
    
    # imag_path & text params because post is not yet in the system
    # def get_similar_posts(self, image_path, text, max_similar_posts):
    # def get_similar_posts(self, post_id, other_posts_df, max_similar_posts):
    def get_similar_posts(self, post_df, other_posts_df, max_similar_posts=3, 
                        top_similar_texts=1000, top_similar_imgs=1000, return_df_similarity=False, use_post_id_external=False):
        # TODO


        other_posts_df[['fields']] = other_posts_df[['fields']].fillna("").apply(list)
        post_df[['fields']] = post_df[['fields']].fillna("").apply(list)


        df_other_post_ids_external = other_posts_df[['post_id_external']]


        print(colored("----Similarity Aggregator-----", "yellow"))
        
        post_id = post_df['id'].to_numpy().flatten()[0]
        print(colored("Post id received:" + str(post_df), "blue"))
        print(colored("Post id received:" + str(post_id), "blue"))
        print("other posts:")
        print(other_posts_df.head())
        print("columns:", other_posts_df.columns)

        print("post df cols: ", post_df.columns )
        base_fields = post_df['fields'].to_numpy().flatten()[0]
        print(" *base fields:", base_fields)
        print("**")
        print(post_df['fields'])

        # base_img_features = post_df['img_features'].to_numpy().flatten()[0]
        base_img_features = post_df['img_features'].to_list()[0]

        # all_txt_fields = other_posts_df['fields'].to_numpy().flatten()
        all_txt_fields = other_posts_df['fields'].to_list()
        # all_imgs_features = other_posts_df['img_features'].to_list()
        # all_imgs_features = other_posts_df[['id','img_features']].set_index('id').T.to_dict('list')
        all_imgs_features = dict(other_posts_df[['id','img_features']].values)

        # print("all imgs features", all_imgs_features)
        all_posts_ids = other_posts_df.index


        df_similar_texts = self.text_module.get_most_similar_by_fields(base_fields, all_txt_fields, all_posts_ids, 
                                        max_similar=top_similar_texts, return_df_similarity=True)

        # rename similarity_score column to text similarity
        df_similar_texts.rename(columns={"similarity_score":"text_similarity"}, inplace=True)
        print("df similar texts type:", df_similar_texts)

        # # #TODO: mai intai most similarl texts, pe urma most similar images care se includ in texte, add post ids!!!!!!!!
        df_similar_images = self.img_module.get_similar_img_by_features(base_img_features, 
                all_imgs_features, max_similar_imgs=top_similar_imgs, return_df_similarity=True, verbose=False)

        df_similar_images = df_similar_images[['*base_img']]

        # rename *base_img column to image similarity
        df_similar_images.rename(columns={"*base_img":"image_similarity"}, inplace=True)
        df_similar_images.drop("*base_img")
        print("*df similar imgs:")
        print(df_similar_images)
        print("type:", type(df_similar_images))
            

        df_similar_merged = df_similar_images.merge(df_similar_texts, left_index=True, right_index=True)
        # print("--- merged df:")
        # print(df_similar_merged.head(10))

        print("--- merged df with aggregated:")
        df_similar_merged['aggregated_similarity'] = df_similar_merged.apply(
                            lambda x: self.aggregate_similarities(x['text_similarity'], x['image_similarity']), axis=1)
        print(df_similar_merged.head(10))

        df_result = df_similar_merged.sort_values('aggregated_similarity',ascending = False).head(max_similar_posts+1).iloc[1:]

        print("df_Result:")
        print(df_result)


        if use_post_id_external:
            df_result = df_result.merge(df_other_post_ids_external, left_index=True, right_index=True)
            df_result = df_result.set_index("post_id_external")

            print("df_Result:")
            print(df_result)


        if return_df_similarity:
            return df_result
        
        
        # return df_result[['aggregated_similarity']].to_dict()

        return df_result[['aggregated_similarity']].to_dict()



        raise NotImplementedError
        return {"result": "not yet implemented!"}

    
    #TODO: add fields extracted from text???
    # def get_similar_posts_by_features(img_features, text, max_similar_posts):
    # get_similar_img_by_features(self, base_img_features, all_imgs_features, max_similar_imgs=3)

    # def get_similar_posts_by_features(self, img_features, txt_fields, all_imgs_features, all_txt_fields, max_similar_posts=3, top_similar_imgs=100, top_similar_texts=100):
    def get_similar_posts_by_features(self, img_features, txt_fields, all_imgs_features, all_txt_fields, max_similar_posts=3, top_similar_imgs=100, top_similar_texts=100):
        # TODO
        print(colored("----Similarity Aggregator-----", "yellow"))
        
        print(colored("Img features:" + str(img_features), "blue"))
        
        print(colored("Text received:" + str(txt_fields), "blue"))


        #TODO; add getMostSimilarTexts, sau texte care match cumva la anumite fielduri, sau doar delta most similar ca la imagini???
        df_similar_texts = self.text_module.get_most_similar_by_fields(txt_fields, all_txt_fields, max_similar=top_similar_texts)

        #TODO: mai intai most similarl texts, pe urma most similar images care se includ in texte, add post ids!!!!!!!!
        df_similar_images = self.img_module.get_similar_img_by_features(img_features, 
                all_imgs_features, max_similar_imgs=top_similar_imgs, return_df_similarity=True)
        
        #lista de posts ids
        df_indexes_img = df_similar_images.index
        df_indexes_texts = df_similar_texts.index

        # print("df indexes img:", df_indexes_img)
        # print("df indexes texts:", df_indexes_texts)
        #TODO: combine all in a single df, and add aggregated_score column, return top max_similar
        # TODO:  put zero when missing a text or image index

        

        # df1 = df_similarity.sort_values('*base_img',ascending = False).head(max_similar_imgs+1).iloc[1:]
        # df2 = df1[['*base_img']]
        # dict_similarities = df2.to_dict()

        

        #TODO: finish


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

