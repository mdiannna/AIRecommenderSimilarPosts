from imagesimilarity import ImageSimilarity

# imgSim = ImageSimilarity(imgs_path="images")
imgSim = ImageSimilarity(imgs_path="ImageSimilarityModule/images")


# imgSim.compute_similarity("img1", "img2")
# TODO: finish
imgSim.get_most_similar("ImageSimilarityModule/images/cat9_siamese.jpg")