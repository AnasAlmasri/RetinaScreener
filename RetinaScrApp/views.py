from django.shortcuts import render
from django.http import HttpResponse
from RetinaScrApp.framework_src.image_utils.RetinaImage import RetinaImage
from RetinaScrApp.framework_src.extractors.VesselExtractor import VesselExtractor
from RetinaScrApp.framework_src.extractors.OpticNerveExtractor import OpticNerveExtractor
from RetinaScrApp.framework_src.extractors.LesionExtractor import ExudateExtractor
import cv2
import matplotlib

# Create your views here.

def index(request):
    reset_processed_image()
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

        reset_processed_image()

        if not options[0] == False: # if Vessels was checked
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            vessels_extractor = VesselExtractor(retina)
            vessels = vessels_extractor.morph_extractor()
            retina.set_vessel_features(vessels)
            # save processed image
            cv2.imwrite('static/images/processed.jpg', retina.vessel_features)
        
        if not options[1] == False: # if Optic Nerve was checked
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            optic_nerve_extractor = OpticNerveExtractor(retina)
            optic_nerve = optic_nerve_extractor.morph_extractor()
            retina.set_optic_nerve_features(optic_nerve)
            # save processed image
            cv2.imwrite('static/images/processed.jpg', retina.optic_nerve_features)
        
        if not options[2] == False: # if fovea was checked
            pass
        
        if not options[3] == False: # if lesions was checked
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            lesion_extractor = ExudateExtractor(retina)
            lesions = lesion_extractor.clahe_extractor()
            retina.set_lesion_features(lesions)
            # save processed image
            cv2.imwrite('static/images/processed.jpg', retina.lesion_features)

    diagnosis_dict = {'vessel_src':'images/processed.jpg'}
    return render(request, 'RetinaScrApp/diagnosis.html', context=diagnosis_dict)

def reset_processed_image():
    processed_img = cv2.imread('static/images/processed.jpg')
    for i in range(processed_img.shape[0]):
        for j in range(processed_img.shape[1]):
            for k in range(processed_img.shape[2]):
                processed_img[i][j][k] = 255 # set value to white
    cv2.imwrite('static/images/processed.jpg', processed_img)