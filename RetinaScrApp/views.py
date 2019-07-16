from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from RetinaScrApp.framework_src.diagnozer.RetinaDiagnozer import RetinaDiagnozer
from RetinaScrApp.framework_src.image_utils.RetinaImage import RetinaImage
from RetinaScrApp.framework_src.extractors.VesselExtractor import VesselExtractor
from RetinaScrApp.framework_src.extractors.OpticNerveExtractor import OpticNerveExtractor
from RetinaScrApp.framework_src.extractors.LesionExtractor import LesionExtractor
from RetinaScrApp.models import Doctor, Patient, Algorithm, Diagnosis
from RetinaScrApp.forms import RegistrationForm
from email.utils import parseaddr
import cv2
import base64
import matplotlib
import sys
import io
from difflib import SequenceMatcher 
import textwrap

diagnozer = RetinaDiagnozer()

def index(request):
    reset_processed_image()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm_password']
            validation_ret = validate_registration(f_name, l_name, email, password, confirm)
            if validation_ret == None: # if no errors were returned
                record = Doctor.objects.get_or_create(
                f_name=f_name,
                l_name=l_name,
                email=email,
                password=password,
                login_method='email')[0]
                record.save()
                return redirect('index')
            else:
                msg = validation_ret + " Please try again by re-filling the registration form with valid information."
                index_dict = {'form': form, 'errors': msg}
                return render(request, 'RetinaScrApp/index.html', context=index_dict)
    #doctor_list = Doctor.objects.all()
    index_dict = {'form': RegistrationForm(), 'password_confirmed': False}
    return render(request, 'RetinaScrApp/index.html', context=index_dict)

def diagnosis(request):
    reset_processed_image()
    
    if request.method == 'POST':
        options = []
        options.append(request.POST.get('vessels', False)) 
        options.append(request.POST.get('opticnerve', False))
        options.append(request.POST.get('fovea', False))
        options.append(request.POST.get('lesions', False))
        options.append(request.POST.get('full', False))
        # example: [False, False, 'Fovea', 'Lesions', False]

        reset_processed_image()

        # get doctor_id and set it in diagnozer
        diagnozer.set_doc_id(2) # doctor_id=2 as an example
        
        if not options[0] == False: # if Vessels was checked
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            vessels = diagnozer.process_vessels(retina)
            retina.set_vessel_features(vessels)
            # save processed image
            cv2.imwrite('static/images/processed.jpg', retina.vessel_features)
        
        if not options[1] == False: # if Optic Nerve was checked
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            optic_nerve = diagnozer.process_optic_nerve(retina)
            retina.set_optic_nerve_features(optic_nerve)
            # save processed image
            cv2.imwrite('static/images/processed.jpg', retina.optic_nerve_features)
        
        if not options[2] == False: # if fovea was checked
            pass
       
        if not options[3] == False: # if lesions was checked
            input_img = cv2.imread('static/images/original.jpg')
            retina = RetinaImage(input_img)
            lesions = diagnozer.process_lesions(retina)
            retina.set_lesion_features(lesions)
            # save processed image
            cv2.imwrite('static/images/processed.jpg', retina.lesion_features)
        
        if not options[4] == False: # if 'full' was checked
            pass

    diagnosis_dict = {'vessel_src':'images/processed.jpg'}
    return render(request, 'RetinaScrApp/diagnosis.html', context=diagnosis_dict)

def customize_algorithm(request):
    pass

def new_algorithm(request):
    data = {
        'client_secret': 'CLIENT_SECRET',
        'async': 0,
        'source': 'source',
        'lang': "PYTHON",
        'time_limit': 5,
        'memory_limit': 262144,
    }

    new_algo_dict = {}
    return render(request, 'RetinaScrApp/new_algorithm.html', context=new_algo_dict)

def how_it_works(request):
    pass

def about(request):
    pass

def contact(request):
    pass

@csrf_exempt 
def requestAjax(request):
    data = {
        'is_valid': False,
        }
    if request.is_ajax():
        message = request.POST.get('message')
        if message == 'I want an AJAX response':
            img_data = request.POST.get('img_data')
            if img_data:
                head, encoded = img_data.split(',')
                decoded = base64.b64decode(encoded)
                with open('static/images/original.jpg', 'wb+') as f:
                    f.write(decoded)
                data.update(is_valid=True)
                data.update(response='This is the response you wanted')
    return JsonResponse(data)

@csrf_exempt
def compileCode(request):
    data = {
        'is_valid': False,
        }
    if request.is_ajax():
        message = request.POST.get('message')
        print(message)
        if message == 'compile and run' or message == 'compile':
            source_code = request.POST.get('source_code')
            if source_code:
                console_response = execute_code(source_code, message)
                data.update(is_valid=True)
                data.update(response=console_response)
    return JsonResponse(data)

def reset_processed_image():
    processed_img = cv2.imread('static/images/original.jpg')
    for i in range(processed_img.shape[0]):
        for j in range(processed_img.shape[1]):
            for k in range(processed_img.shape[2]):
                processed_img[i][j][k] = 255 # set value to white
    cv2.imwrite('static/images/processed.jpg', processed_img)

def execute_code(source_code, order):
    # create file-like string to capture output
    codeOut = io.StringIO()
    # capture output and errors
    sys.stdout = codeOut
    # validate code
    validated_src = validate(source_code)
    if validated_src:
        # execute code
        if order == 'compile and run':
            try:
                exec(validated_src)
                replace(validated_src)
            except Exception as ex:
                print(ex)
        elif order == 'compile':
            try:
                compile(validated_src, 'custom', 'exec')
                print('Code compiled successfully.')
            except Exception as ex:
                print(ex)
    else:
        print('Invalid source code')

    # restore stdout and stderr
    sys.stdout = sys.__stdout__
    # set return values
    returned_output = codeOut.getvalue()
    # close streams
    codeOut.close()
    return returned_output

def validate(source_code):
    # check function definition
    if source_code.startswith('def extract(self, fundus):'):
        # split code into lines
        lines = source_code.splitlines()
        # drop whitespace lines
        temp = [line for line in lines if not line=='']
        # check return statement
        if 'return' in temp[-1]:
            # add extra indentation to be able to fit in file with no whitespace issues
            return source_code.replace('\t', ' ' * 4)
        else:
            print("No 'return' statement detected")
    else:
        print("Function definition [def extract(self, fundus)] not detected")
    return False

def replace(source_code):
    src = textwrap.indent(source_code, ' ' * 4)
    # update .py file
    diagnozer.parse_pyfile(
        'RetinaScrApp/framework_src/extractors/CustomVesselExtractor.py',
        src
    )

def validate_registration(f_name, l_name, email, password, confirm):
    if not password == confirm:
        return 'Input passwords do not match.'
    elif not f_name.isalpha():
        return 'First name cannot contain numbers or special characters, only letters.'
    elif not l_name.isalpha():
        return 'Last name cannot contain numbers or special characters, only letters.'
    elif f_name in password:
        return 'Password cannot contain first name.'
    elif l_name in password:
        return 'Password cannot contain last name.'
    elif parseaddr(email) == ('',''):
        return 'Email address is invalid.'
    elif len(password) < 8:
        return 'Password should be at least 8 characters long'

    seqMatch = SequenceMatcher(None, email, password) 
    match = seqMatch.find_longest_match(0, len(email), 0, len(password)) 
    if (match.size >= 4): 
        return 'Email and password cannot have matching substrings of length >=4'
  
    return None


