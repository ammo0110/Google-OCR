# Google OCR for Python 3

Uses [Google Cloud Vision](https://cloud.google.com/vision/) to perform Optical Character Recognition on jpg and png images.

## Usage
1. Clone this repo
> git clone https://github.com/ammo0110/Google-OCR
2. Install the requirements
> pip3 install -r requirements.txt
3. Enable the Cloud Vision API from Google Cloud Platform Console. Refer [this](https://cloud.google.com/vision/docs/before-you-begin)
4. Get an API key for yourself. Refer [this](https://cloud.google.com/docs/authentication/api-keys)
5. Once you have the API key, execute main.py file with following arguments
> python3 main.py `path_to_api_key_file` `path_to_input_image`

## Other features
1. `-o/ --output` flag for redirecting output to a file
2. Recursive mode for recognizing a complete directory of jpg/png images at once
3. Multithreaded processing in case of recursive mode

For help, use
> python3 main.py --help

## Afterthoughts
Google provides two kinds of APIs for it's GCP services: REST APIs and the other language specific APIs. I immediately found some issues with the Python specific APIs, which are:

1. They are written only for Python 2.
2. You have to install Google Libraries on your system
3. Unlike REST APIs, the authetication process for using these APIs is not decoupled from the API library itself. Although easier to use, I don't think that this kind of approach is practical
from a design point of view.

Anyways, I decided to give it a try and wrote a [program](https://github.com/ammo0110/Google-Speech-Example) for Speech Recognition using the Python specific APIs. Then I realized one more problem with it. 
In case of an internet connection failure, these APIs don't report any error.

So now I have concluded that for Python, using REST APIs is the only option since it solves all the aforementioned problems.
