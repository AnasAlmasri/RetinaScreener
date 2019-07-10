from RetinaScrApp.framework_src.image_utils.RetinaImage import RetinaImage
from RetinaScrApp.framework_src.extractors.VesselExtractor import VesselExtractor
from RetinaScrApp.framework_src.extractors.OpticNerveExtractor import OpticNerveExtractor
from RetinaScrApp.framework_src.extractors.LesionExtractor import ExudateExtractor
from RetinaScrApp.models import Doctor
import cv2

class RetinaDiagnozer:
    """
        extractors['vessel']: 'default' or 'algo_id',
        extractors['optic']: 'default' or 'algo_id',
        extractors['fovea']: 'default' or 'algo_id',
        extractors['lesion']: 'default' or 'algo_id',
    """

    def __init__(self, doc_id):
        self.extractors = None
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
                vessels_extractor = VesselExtractor(retina)
                vessels = vessels_extractor.morph_extractor()
                return vessels
            else:
                pass

    def process_optic_nerve(self, retina):
        if not self.extractors == None:
            if self.extractors['optic'] == 'default':
                optic_nerve_extractor = OpticNerveExtractor(retina)
                optic_nerve = optic_nerve_extractor.morph_extractor()
                return optic_nerve
            else:
                pass
    
    def process_fovea(self, retina):
        if not self.extractors == None:
            if self.extractors['fovea'] == 'default':
                pass
            else:
                pass

    def process_lesions(self, retina):
        if not self.extractors == None:
            if self.extractors['lesion'] == 'default':
                lesion_extractor = ExudateExtractor(retina)
                lesions = lesion_extractor.clahe_extractor()
                return lesions
            else:
                pass


