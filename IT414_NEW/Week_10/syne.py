import os
import shutil
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import zipfile
from urllib.parse import urljoin

# Constants
BASE_URL = 'https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week10/WI20-Assignment/employees/index.php?ModPagespeed=off'
IMAGES_FOLDER = 'images'
OUTPUT_FOLDER = os.path.join(IMAGES_FOLDER, 'output_images')
FONT_PATH = '/mnt/data/Syne-Regular.ttf'  # Path to the uploaded font file

# Clear the images folder
if os.path.exists(IMAGES_FOLDER):
    shutil.rmtree(IMAGES_FOLDER)
os.makedirs(IMAGES_FOLDER)
os.makedirs(OUTPUT_FOLDER)

# Scrape the webpage
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Get company logo
logo_img_tag = soup.find('img')
logo_url = urljoin(BASE_URL, logo_img_tag['src'])
logo_response = requests.get(logo_url)
company_logo = Image.open(BytesIO(logo_response.content))

# Scrape employee data
employees = soup.find_all('div', class_='employee')
employee_data = []
for employee in employees:
    name = employee.find('h2').text
    title = employee.find('h3').text
    image_url = urljoin(BASE_URL, employee.find('img')['src'])
    employee_data.append((name, title, image_url))

# Download images and process them
for name, title, image_url in employee_data:
    try:
        # Download image
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))

        # Overlay text and logo
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, size=20)

        # Determine position for text and logo to avoid covering the face
        text_position = (10, img.height - 50)
        logo_position = (img.width - company_logo.width - 10, 10)

        # Add text
        draw.text(text_position, f'{name}\n{title}', font=font, fill='white')

        # Add logo
        img.paste(company_logo, logo_position, company_logo)

        # Save the modified image
        img_output_path = os.path.join(OUTPUT_FOLDER, f'{name.replace(" ", "_")}.png')
        img.save(img_output_path)
        print(f'Successfully processed and saved image for {name}')

    except Exception as e:
        print(f'Error processing image for {name}: {e}')

# ZIP the modified images
try:
    zip_path = os.path.join(IMAGES_FOLDER, 'output_images.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(OUTPUT_FOLDER):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), OUTPUT_FOLDER))
    print(f'Successfully created ZIP file at {zip_path}')
except Exception as e:
    print(f'Error creating ZIP file: {e}')
