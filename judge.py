import subprocess
import os
from PIL import Image
import time
import platform
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import imagehash

def get_word_count(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        words = content.split()
        return len(words)

def linear_normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

def convert_ps_to_png(ps_file, png_file):
    # Ensure the output directory exists
    # Open the PostScript file and convert it to a PNG file
    img = Image.open(ps_file)
    img.save(png_file)

def extract_object(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])

    object_img = image[y:y+h, x:x+w]
    return object_img

def calculate_pixel_difference_similarity(image1_path, image2_path):
    # Extract objects from the images
    img1 = extract_object(image1_path)
    img2 = extract_object(image2_path)
    
    # Convert images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY).astype(np.int16)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY).astype(np.int16)

    # Ensure the images have the same size for comparison
    img1 = cv2.resize(img1, (500, 500))
    img2 = cv2.resize(img2, (500, 500))

    # Create a mask to ignore white pixels (value 255)
    mask = (img2 != 255).astype(np.uint8)  # create mask with 0 where img2 is 255, and 1 otherwise

    valid_pixel = 0
    similar_pixel = 0
    THRESHOLD = 20

    for i in range(500):
        for j in range(500):
            if mask[i][j] == 0:  # if mask is 0, ignore this pixel
                continue
            valid_pixel += 1
            if abs(img1[i][j] - img2[i][j]) <= THRESHOLD:
                similar_pixel += 1
    print('similar_pixel: ', similar_pixel)
    pixel_similarity = similar_pixel / 500**2
    return pixel_similarity

def calculate_clip_similarity(model, image1_path, image2_path):
    # Encode the images
    original_image = Image.open(image1_path)
    drawn_image = Image.open(image2_path)

    encoded_images = model.encode([original_image, drawn_image], batch_size=2, convert_to_tensor=True)

    # Compute cosine similarity
    similarity = util.cos_sim(encoded_images[0], encoded_images[1]).item()

    # Normalize similarity score to a range of 0 to 1
    similarity = linear_normalize(similarity, 0, 1)

    return similarity
def judge_logic(image_url, result_path, word_count, execution_time):

    pixel_similarity = calculate_pixel_difference_similarity(image_url, result_path)
    print('origin pixel_similarity: ', pixel_similarity)
    pixel_similarity = min(1, linear_normalize(pixel_similarity, 0, 0.025))
    print('Loading CLIP Model...')
    model = SentenceTransformer('clip-ViT-B-32')
    # Calculate CLIP similarity
    clip_similarity = calculate_clip_similarity(model, image_url, result_path)
    print('origin clip_similarity: ', clip_similarity)
    clip_similarity = max(0, linear_normalize(clip_similarity, 0.7, 1))
    # Normalize percentage difference to a similarity score (0 to 1)
    # Combine the similarity scores with equal weight

    combined_similarity = 0.7 * pixel_similarity + 0.3 * clip_similarity
    print('pixel_similarity: ', pixel_similarity)
    print('clip_similarity: ', clip_similarity)
    print('combined_similarity: ', combined_similarity)
    min_word_count = 100
    max_word_count = 600

    word_count_score = 30 * (1 - linear_normalize(word_count, min_word_count, max_word_count))
    word_count_score = max(0, min(30, word_count_score))

    similarity_score = 70 * combined_similarity
    total_score = similarity_score + word_count_score

    # print(f"Percentage Difference: {percentage_diff}%")
    print(f"Similarity score: {combined_similarity}, Word Count score: {word_count_score}\n\n")
    return total_score, combined_similarity

# def judge_logic(image_url, result_path, word_count, execution_time):
#     # Open the images
#     # image1 = cv2.imread(image_url)
#     # image2 = cv2.imread(result_path)

#     # # Ensure the images have the same size for comparison
#     # image1 = cv2.resize(image1, (500, 500))
#     # image2 = cv2.resize(image2, (500, 500))
#     original_object = extract_object(image_url)
#     drawn_object = extract_object(result_path)
#     image1 = cv2.resize(original_object, (500, 500))
#     image2 = cv2.resize(drawn_object, (500, 500))
#     # Compare histograms for RGB channels
#     print('image1: ', image1.shape)
#     print('image2: ', image2.shape)
#     hist_similarity = compare_histograms(image1, image2)

#     # Convert images to grayscale for structural similarity comparison
#     gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#     gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

#     # Compute SSIM
#     ssim_index, _ = ssim(gray_image1, gray_image2, full=True)
#     ssim_index = linear_normalize(ssim_index, -1, 1)

#     # Combine the similarity scores
#     combined_similarity = 0.5 * hist_similarity + 0.5 * ssim_index

#     # Normalize similarity score to a range of 0 to 1
#     combined_similarity = linear_normalize(combined_similarity, 0, 1)

#     min_word_count = 100
#     max_word_count = 600

#     word_count_score = 30 * (1 - linear_normalize(word_count, min_word_count, max_word_count))
#     word_count_score = max(0, min(30, word_count_score))

#     similarity_score = 70 * combined_similarity
#     total_score = similarity_score + word_count_score

#     print(f"Histogram Similarity: {hist_similarity}, SSIM: {ssim_index}")
#     print(f"Similarity score: {similarity_score}, Word Count score: {word_count_score}\n\n")
#     return total_score, combined_similarity

def run_code(code_path, image_url, result_path):

    result_dir = os.path.dirname(result_path)
    ps_file = f"{result_dir}/temp.ps"
    if os.path.isfile(ps_file):
        # Remove the file
        os.remove(ps_file)
    # png_file = f"{result_dir}/{output_filename}.png"
    # Ensure the result directory exists
    os.makedirs(result_dir, exist_ok=True)

    word_count = get_word_count(code_path)
    # Run the provided Python script to generate the PostScript file
    # Use check to raise an exception if the script fails
    start_time = time.time()
    try:
        # Detect Run Time OS
        if platform.system() == "Windows":
            subprocess.run(["python", code_path, ps_file], check=True)
        else:
            subprocess.run(["python3", code_path, ps_file], check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess
        print(f"Subprocess CalledProcessError: {e}")
        return None
    end_time = time.time()
    execution_time = end_time - start_time

    # check if the PostScript file was created
    if not os.path.exists(ps_file):
        return 0, 0, word_count, execution_time

    convert_ps_to_png(ps_file, result_path)
    score, similarity = judge_logic(image_url, result_path, word_count, execution_time)
    # Return the path to the generated PNG file
    return score, similarity, word_count, execution_time

def judge_submission(code_path, image_url, result_path):

    image_url = f".{image_url}"
    print(f"image_url: {image_url}\n\n")
    score, similarity, word_count, execution_time = run_code(code_path, image_url, result_path)

    # Here you would implement the logic to judge the PNG file and assign a score.
    # For demonstration, let's assume the score is always 100.

    return score, similarity, word_count, execution_time
