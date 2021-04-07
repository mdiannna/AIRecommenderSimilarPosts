from imagesimilarity import ImageSimilarity

# imgSim = ImageSimilarity(imgs_path="images")
imgSim = ImageSimilarity(imgs_path="ImageSimilarityModule/images")


# imgSim.compute_similarity("img1", "img2")
# TODO: finish
# imgSim.get_most_similar("ImageSimilarityModule/images/cat9_siamese.jpg")


img_folder = 'ImageSimilarityModule/images/'
similarity_score1 = imgSim.compute_similarity(img_folder + "abysinian1.jpg", img_folder + "abysinian4.jpeg")
print("similarity score 1:", similarity_score1)