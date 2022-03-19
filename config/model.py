import os

#========================== DIRECTORY =====================================
ROOT 					= os.path.normpath(os.path.dirname(__file__))

DIRECTORY_MODEL         = os.path.expanduser('~/.Halotec/Models')

DIRECTORY_LOGGER        = os.path.expanduser('~/.Halotec/Loggers')

#============================ MODELS ======================================
DETECTION_MODEL = {
	'seal_detection' : {
		'filename'  : 'seal_detection_gray.pt',
		'url'       : 'https://www.dropbox.com/s/wwa953l07tpflml/seal_detection_v1_1.pt?dl=1',
		'file_size' : 14753191
	}
}

#============================ CLASESS ======================================
CLASSES_DETECTION   = ['no_seal','seal']
CLASSES_FILTERED    = ['seal']