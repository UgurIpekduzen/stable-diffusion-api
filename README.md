# stable-diffusion-api

This project aims to generate a new image in a similar style using the Stable Diffusion algorithm with a given stock photo and a prompt. Additionally, it creates a simple dynamic ad template using the generated image.

![stable-diffusion-api](api_ui.jpg)

## Problem Solving

Traditional methods of creating advertisements can be time-consuming and costly. This project allows users to create unique ad visuals with a stock photo and a set of text inputs. The Stable Diffusion(Img2Img) algorithm stands out with its ability to produce realistic and creative images.

## Technologies Used

- Python
- Flask: Used to build the web application.
- PyTorch and Stable Diffusion(Img2Img): Utilized for image generation processes.
- HTML and CSS: Employed for creating web page templates.
- Google Cloud Platform (GCP): Deployed on GCP for scalable and reliable cloud hosting.

## How to Use

1. Clone the project to your computer:
    `git clone https://github.com/user/stable-diffusion-api.git`
2. Navigate to the project directory:
    `cd stable-diffusion-api`
3. Create a virtual environment and install the libraries:
    `python -m venv venv`
    `source venv/bin/activate`
    `pip install -r requirements.txt`
4. Run the app:
    `gunicorn wsgi:app -b 0.0.0.0:5000`
5. Open your browser and go to http://localhost:5000.
6. Fill out the form on the web page to generate the ad.
