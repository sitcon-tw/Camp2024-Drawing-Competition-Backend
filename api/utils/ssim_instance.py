import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim   

class SSIM:
    _instance = None
    
    def __init__(self)->None:
        print("[SSIM-Instance] SSIM Instance inited")

    @staticmethod
    def get_instance():
        if SSIM._instance is None:
            SSIM._instance = SSIM()
        return SSIM._instance
    
    def linear_normalize(self,value, min_value, max_value):
        return (value - min_value) / (max_value - min_value)
    def calculate_similarity(self,image1_path:str,image2_path:str):

        # Open the two images
        image1 = Image.open(image1_path).convert('L') # convert('L') converts an image to grayscale
        image2 = Image.open(image2_path).convert('L')
        
        # Resize images to the same size for comparison
        image1 = image1.resize((500, 500))
        image2 = image2.resize((500, 500))

        # Compare the two images
        # This will return a floating point number representing the similarity
        # 0 means the images are completely different
        # 1 means the images are identical

        # similarity = Image.cmp(image1, image2)

        # Use the SSIM (Structural Similarity Index) to compare the two images
        image1_np = np.array(image1)
        image2_np = np.array(image2)
        similarity, _ = ssim(image1_np, image2_np, full=True) # range of SSIM is -1 to 1
        similarity = self.linear_normalize(similarity, -1, 1)  # Normalize to a range of 0 to 1
        print(f"[SSIM-Instance] Similarity score: {similarity}")
        return similarity