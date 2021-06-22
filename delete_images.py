from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np 
import cv2, os

examples = 'examples/'
image = []

for img in os.listdir(examples):
	temp_name = img
	image = cv2.imread(os.path.join(examples, img))
	orig = image.copy()
	
	# Preprocessing the image & Prediction
	image = cv2.resize(image, (28, 28))
	image = image.astype('float')/255.0	
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	model = load_model('model.h5')
	(not_notes, notes) = model.predict(image)[0]
	label = 'notes' if notes > not_notes else "not_notes"
	proba = notes if notes > not_notes else not_notes
	# label = "{}: {:.2f}%".format(label,proba*100)
	
	# Sorting in Respective folders
	if(label == "not_notes"):
		if not os.path.exists('Not_Notes'):
			os.makedirs('Not_Notes')

		path = 'Not_Notes/'+temp_name
	else:
		if not os.path.exists('Notes'):
    			os.makedirs('Notes')

		path = 'Notes/'+temp_name
  
	cv2.imwrite(path, orig)
