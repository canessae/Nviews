# Nviews
A simple python tool to produce N views from single image and depth map

# Usage
python3 -m venv venv
source venv/bin/activate
  	pip install -r requirements.txt
deactivate

# Install
source venv/bin/activate
	python3 nviews.py -i img/000152.png -d depthmap/000152dp.png -nv 50		## -f 1/25 -ud 
deactivate

# Output
See directory example/ for input, output data:

![output-25-50](https://user-images.githubusercontent.com/84878752/209672713-07349566-4746-4daf-bb45-ff7106f1df5a.gif)
