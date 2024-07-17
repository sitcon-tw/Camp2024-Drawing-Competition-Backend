from PIL import Image
from sentence_transformers import SentenceTransformer, util

class Clip:
    _instance= None

    def __init__(self) -> None:
        self.model = SentenceTransformer('clip-ViT-B-32')

    @staticmethod
    def get_instance():
        if Clip._instance is None:
            Clip._instance = Clip()
        return Clip._instance
    def linear_normalize(self,value, min_value, max_value):
        return (value - min_value) / (max_value - min_value)

    def calculate_clip_similarity(self, image1_path, image2_path):
        # Encode the images
        original_image = Image.open(image1_path)
        drawn_image = Image.open(image2_path)

        encoded_images = self.model.encode([original_image, drawn_image], batch_size=2, convert_to_tensor=True)

        # Compute cosine similarity
        similarity = util.cos_sim(encoded_images[0], encoded_images[1]).item()

        # Normalize similarity score to a range of 0 to 1
        similarity = self.linear_normalize(similarity, 0, 1)

        del encoded_images

        return similarity
    
if __name__ == "__main__":
    clip_instance=Clip.get_instance()
    similarity =clip_instance.calculate_clip_similarity("image1_path","image2_path")