import cv2

class RetinaImage:
	# class constructor
	def __init__(self, image):
		# original image matrix
		self.fundus = image
		
		# image.resolution = (height, width)
		self.resolution = (self.fundus.shape[0], self.fundus.shape[1])
		# image.shape = (height, width, channels)
		self.shape = (self.fundus.shape[0], self.fundus.shape[1], self.fundus.shape[2])

		# image extraction status
		# image.status = 'RAW' when untouched
		# image.status = 'PROCESSED' when features extracted
		self.status = 'RAW' # default value

		# extraction status
		# image.vessels = 'NONE' when vessel features not extracted
		# image.vessels = 'DONE' when vessel features extracted
		self.vessels = 'NONE' # default value
		self.vessel_features = None

		# image.optic_nerve = 'NONE' when optic_nerve features not extracted
		# image.optic_nerve = 'DONE' when optic_nerve features extracted
		self.optic_nerve = 'NONE' # default value
		self.optic_nerve_features = None

		# image.fovea = 'NONE' when fovea features not extracted
		# image.fovea = 'DONE' when fovea features extracted
		self.fovea = 'NONE' # default value
		self.fovea_features = None

		# image.lesions = 'NONE' when lesion features not processed
		# image.lesions = 'DONE' when lesion features processed
		self.lesions = 'NONE' # default value
		self.lesion_features = None

	# end of constructor

	def resize(self, height=640, width=480):
		self.fundus = cv2.resize(self.fundus, (height, width)) 

# -------------------- SETTERS AND GETTERS ---------------------

	def set_status(self, status):
		self.status = status

	def set_vessel_features(self, features):
		self.vessel_features = features
		self.vessels = 'DONE'
		self.update_status()

	def set_optic_nerve_features(self, features):
		self.optic_nerve_features = features
		self.optic_nerve = 'DONE'
		self.update_status()

	def set_fovea_features(self, features):
		self.fovea_features = features
		self.fovea = 'DONE'
		self.update_status()

	def set_lesion_features(self, features):
		self.lesion_features = features
		self.lesions = 'DONE'
		self.update_status()

	def get_vessel_features(self):
		pass

	def get_optic_nerve_features(self):
		pass

	def get_fovea_features(self):
		pass

	def get_lesion_features(self):
		pass

	def update_status(self):
		if self.vessels == 'DONE' and self.optic_nerve == 'DONE':
			if self.fovea == 'DONE' and self.lesions == 'DONE':
				self.set_status = 'PROCESSED'