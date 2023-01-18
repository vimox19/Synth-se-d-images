from flask import Flask, make_response, render_template, request, redirect,jsonify
from lib.searcher import Search
from PIL import Image
import numpy as np
import cv2
import os
import shutil
from lib.models import read_obj,calc_features
from paste.translogger import TransLogger
from waitress import serve

app = Flask(__name__)

UPLOAD_FOLDER = 'static/te'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def clear_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

			
@app.route('/')
def cekawal():
	if os.path.exists('static/temp') == True :
		shutil.rmtree('static/temp')
		shutil.rmtree('static/tmp')
		return redirect('/home')
	else :
		return redirect('/home')

@app.route('/home')
def home():

	datasets = os.listdir('static/models-images')
	if os.path.exists('static/temp') == True :
		image_names = os.listdir('static/temp')
		nearest = sorted(os.listdir('static/temp'))[0]
		target = os.listdir('static/tmp')
		return render_template("index.html", image_names=sorted(image_names),\
		target=(target), page_status=1,  nearest=(nearest),count=len(datasets))
	else :
		return render_template("index.html", page_status=2,count=len(datasets))


@app.route('/search', methods=['POST'])
def search():
	file = request.files['obj_file']
	filename = file.filename
	name=filename[0:11]
	file.save(os.path.join("static/te",filename))

	image=cv2.imread("C:/Users/vimox/Desktop/Flask/static/models-images/"+name+".jpg")
	#print(image)
	

	readFile = read_obj(str(UPLOAD_FOLDER + '/' + filename))
	vertex = calc_features(readFile)
	#print(readFile)
	#print(vertex)

	searcher = Search('conf/models.csv')
	results = searcher.search(vertex)

	#print(results)

	os.makedirs('static/temp')
	os.makedirs('static/tmp')

	saveimg = cv2.imwrite("C:/Users/vimox/Desktop/Flask/static/tmp/"+ name + ".jpg" ,image )
	i = 0
	for (score, imagePath) in results:
		if imagePath == 'static/models-images/' +name:
			continue
		i += 1
		scoore= str(score)
		result = cv2.imread("C:/Users/vimox/Desktop/Flask/"+imagePath+".jpg")
		#print(result)
		saveimg = cv2.imwrite("C:\\Users\\vimox\\Desktop\\Flask\\static\\temp\\" +str(i)+"-" +scoore[0:10]+ ".jpg",result )

	return redirect('/home')

@app.route('/<page_name>')
def other_page(page_name):
	return render_template("404.html"), 404

if __name__ == '__main__':
	clear_folder('static/te')
	serve(TransLogger(app, setup_console_handler=False), host="0.0.0.0", port=5000)

