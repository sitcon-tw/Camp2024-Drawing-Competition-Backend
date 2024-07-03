import platform
import subprocess
import os
from PIL import Image
import time
from skimage.metrics import structural_similarity as ssim

import cv2
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import imagehash
import numpy as np
import datetime

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
    min_word_count = 50
    max_word_count = 300

    word_count_score = 25 * (1 - max(0, linear_normalize(word_count, min_word_count, max_word_count)))
    word_count_score = max(0, min(25, word_count_score))

    similarity_score = 75 * combined_similarity
    if similarity_score > 30:
        total_score = similarity_score + word_count_score
    else:
        total_score = 0
    # print(f"Percentage Difference: {percentage_diff}%")
    print(f"Similarity score: {combined_similarity}, Word Count score: {word_count_score}\n\n")
    return total_score, combined_similarity

def copy_and_modify_template(judge_template_path, template_revise_path, 
                                        code_path):
    code_filename = os.path.basename(code_path)
    # Construct the import line
    import_line = f"from {code_filename .replace('.py', '')} import drawing\n"

    # Read the original template
    with open(judge_template_path, 'r') as template_file:
        template_content = template_file.read()

    # Create the new content with the import line at the beginning
    new_content = import_line + template_content
    # new_content = template_content
    # Write the new content to the destination path
    with open(template_revise_path, 'w') as new_template_file:
        new_template_file.write(new_content)

# At here, change the main_template code and drawing template code

def run_code(code_path, image_url, result_path, team_id, 
                drawing_template_path, main_drawing_path, 
                template_revise_path, submission_id):

    result_dir = os.path.dirname(result_path)
    ps_file = f"{result_dir}/{submission_id}.ps"
    if os.path.isfile(ps_file):
        # Remove the file
        os.remove(ps_file)
    # png_file = f"{result_dir}/{output_filename}.png"
    # Ensure the result directory exists
    os.makedirs(result_dir, exist_ok=True)
    
    copy_and_modify_template(drawing_template_path, template_revise_path, 
                                        code_path)
    print(f'template revise path: {template_revise_path}')
    # Run the provided Python script to generate the PostScript file
    # Use check to raise an exception if the script fails
    try:
        print("MAINDRAWING",main_drawing_path,ps_file,submission_id, code_path,template_revise_path,result_path,image_url,sep=" ")
        p=subprocess.Popen([
            "python3", 
            str(main_drawing_path), 
            str(ps_file), 
            str(submission_id), 
            str(code_path), 
            str(template_revise_path), 
            str(result_path), 
            str(image_url)
        ])
     
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return
    # try:
    #     process = subprocess.Popen([
    #         "python3", 
    #         main_drawing_path, 
    #         ps_file, 
    #         str(submission_id), 
    #         code_path, 
    #         template_revise_path, 
    #         result_path, 
    #         image_url
    #     ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    #     print("Main drawing started, continuing with other tasks...")
        
    #     # Optionally, you can check on the process or wait for it to complete later
    #     # For example, to wait for the process to complete and capture output:
    #     stdout, stderr = process.communicate(timeout=30)  # Adjust the timeout as needed

    #     if process.returncode == 0:
    #         print("Main drawing completed successfully")
    #         print(f"Output: {stdout}")
    #     else:
    #         print(f"Main drawing failed with return code {process.returncode}")
    #         print(f"Error: {stderr}")

    # except subprocess.TimeoutExpired:
    #     process.kill()
    #     stdout, stderr = process.communicate()
    #     print("Main drawing timed out and was killed")
    #     print(f"Output: {stdout}")
    #     print(f"Error: {stderr}")
    # except subprocess.CalledProcessError as e:
    #     print(f"Main drawing failed: {e}")
    

def judge_submission(code_path, image_url, result_path, team_id, 
                        drawing_template_path, main_drawing_path, 
                        template_revise_path, submission_id):

    image_url = f".{image_url}"
    print(f"image_url: {image_url}\n\n")
    
    run_code(code_path, image_url, result_path, team_id, 
                drawing_template_path, main_drawing_path, 
                template_revise_path, submission_id)

    # Here you would implement the logic to judge the PNG file and assign a score.
    # For demonstration, let's assume the score is always 100.

