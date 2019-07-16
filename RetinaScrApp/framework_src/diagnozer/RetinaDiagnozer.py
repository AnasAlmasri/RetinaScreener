from RetinaScrApp.framework_src.image_utils.RetinaImage import RetinaImage
# import default extractors
from RetinaScrApp.framework_src.extractors.VesselExtractor import VesselExtractor
from RetinaScrApp.framework_src.extractors.OpticNerveExtractor import OpticNerveExtractor
from RetinaScrApp.framework_src.extractors.LesionExtractor import LesionExtractor
# import custom extractors
from RetinaScrApp.framework_src.extractors.CustomVesselExtractor import CustomVesselExtractor
from RetinaScrApp.framework_src.extractors.CustomOpticNerveExtractor import CustomOpticNerveExtractor
from RetinaScrApp.framework_src.extractors.CustomLesionExtractor import CustomLesionExtractor
# import models
from RetinaScrApp.models import Doctor
import cv2
import re

class RetinaDiagnozer:
    """
        extractors['vessel']: 'default' or 'algo_id',
        extractors['optic']: 'default' or 'algo_id',
        extractors['fovea']: 'default' or 'algo_id',
        extractors['lesion']: 'default' or 'algo_id',
    """

    def __init__(self):
        self.extractors = None
    
    def set_doc_id(self, doc_id):
        self.get_extractor_preferences(doc_id)
    
    def get_extractor_preferences(self, doc_id):
        doctor = Doctor.objects.get(doctor_id=doc_id)
        self.extractors = {
            'vessel': doctor.vessel_pref,
            'optic': doctor.optic_pref,
            'fovea': doctor.fovea_pref,
            'lesion': doctor.lesion_pref
        }

    def process_vessels(self, retina):
        if not self.extractors == None:
            if self.extractors['vessel'] == 'default':
                vessels_extractor = VesselExtractor()
                vessels = vessels_extractor.extract(retina.fundus)
            else:
                vessels_extractor = CustomVesselExtractor()
                vessels = vessels_extractor.extract(retina.fundus)
            return vessels

    def process_optic_nerve(self, retina):
        if not self.extractors == None:
            if self.extractors['optic'] == 'default':
                optic_nerve_extractor = OpticNerveExtractor()
                optic_nerve = optic_nerve_extractor.extract(retina.fundus)
            else:
                optic_nerve_extractor = CustomOpticNerveExtractor()
                optic_nerve = optic_nerve_extractor.extract(retina.fundus)
            return optic_nerve
    
    def process_fovea(self, retina):
        if not self.extractors == None:
            if self.extractors['fovea'] == 'default':
                pass
            else:
                pass

    def process_lesions(self, retina):
        if not self.extractors == None:
            if self.extractors['lesion'] == 'default':
                lesion_extractor = LesionExtractor()
                lesions = lesion_extractor.extract(retina.fundus)
            else:
                lesion_extractor = CustomLesionExtractor()
                lesions = lesion_extractor.extract(retina.fundus)
            return lesions

    # function to find and replace part of the code to execute later
    def parse_pyfile(self, filepath, new_code):
        original_src = open(filepath, 'r').read()
        pattern = '# BEGINNING OF EXTRACT FUNCTION.*?# END OF EXTRACT FUNCTION'

        updated_code = re.sub(
            pattern, 
            '# BEGINNING OF EXTRACT FUNCTION\n' + new_code + '\n\t# END OF EXTRACT FUNCTION', 
            original_src, 
            flags=re.DOTALL
        )
        #original_src.replace(pattern, new_code)
        with open(filepath, 'w') as f:
            f.write(updated_code)
            f.close()
