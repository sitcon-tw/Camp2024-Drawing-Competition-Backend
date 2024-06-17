import platform
import subprocess
import os
from PIL import Image
import time
from skimage.metrics import structural_similarity as ssim
import numpy as np

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

def judge_logic(image_url, result_path, word_count, execution_time):

    # Open the two images
    image1 = Image.open(image_url).convert('L') # convert('L') converts an image to grayscale
    image2 = Image.open(result_path).convert('L')

    # Resize images to the same size for comparison
    image1 = image1.resize((500, 500))
    image2 = image2.resize((500, 500))

    # Compare the two images
    # This will return a floating point number representing the similarity
    # 0 means the images are completely different
    # 1 means the images are identical

    # Use the SSIM (Structural Similarity Index) to compare the two images
    image1_np = np.array(image1)
    image2_np = np.array(image2)
    similarity, _ = ssim(image1_np, image2_np, full=True) # range of SSIM is -1 to 1
    similarity = linear_normalize(similarity, -1, 1)  # Normalize to a range of 0 to 1
    # Normalized scores for word count and execution time
    min_word_count = 100  # Example value, should be adjusted
    max_word_count = 600  # Example value, should be adjusted
    min_execution_time = 0  # Example value, should be adjusted
    max_execution_time = 6.0  # Example value, should be adjusted

    # Normalize word count to a score out of 20
    word_count_score = 20 * (1 - linear_normalize(word_count, min_word_count, max_word_count))
    word_count_score = max(0, min(20, word_count_score))

    # Normalize execution time to a score out of 20
    execution_time_score = 20 * (1 - linear_normalize(execution_time, min_execution_time, max_execution_time))
    execution_time_score = max(0, min(20, execution_time_score))

    # Calculate total score
    similarity_score = 60 * similarity  # 60% weight for similarity
    total_score = similarity_score + word_count_score + execution_time_score
    print(f"Similarity score: {similarity_score}, Word Count score: {word_count_score}, Execution Time score: {execution_time_score}\n\n")
    # Return the similarity score
    return total_score, similarity*100

def run_code(code_path, image_url, result_path):

    result_dir = os.path.dirname(result_path)
    ps_file = f"{result_dir}/temp.ps"
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
        print(f"Error: {e}")
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
