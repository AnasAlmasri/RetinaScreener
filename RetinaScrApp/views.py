from django.shortcuts import render
from django.http import HttpResponse
from RetinaScrApp.framework_src.image_utils.RetinaImage import RetinaImage
from RetinaScrApp.framework_src.extractors.VesselExtractor import VesselExtractor
import cv2

# Create your views here.

def index(request):
    index_dict = {'insert_me': "Hello. I am from views.py"}
    return render(request, 'RetinaScrApp/index.html', context=index_dict)

def diagnosis(request):

    if request.method == 'POST':
        options = []
        options.append(request.POST.get('vessels', False)) 
        options.append(request.POST.get('opticnerve', False))
        options.append(request.POST.get('fovea', False))
        options.append(request.POST.get('lesions', False))
        options.append(request.POST.get('full', False))
        # example: [False, False, 'Fovea', 'Lesions', False]
        
        if not options[0] == False:
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            vessels_extractor = VesselExtractor(retina)
            vessels = vessels_extractor.morph_extractor()
            retina.set_vessel_features(vessels)
            if retina.vessels == 'DONE':
                cv2.imshow('Vessels', retina.vessel_features)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    diagnosis_dict = {'vessel_src':'images/vessels.jpg'}
    return render(request, 'RetinaScrApp/diagnosis.html', context=diagnosis_dict)