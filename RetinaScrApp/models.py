from django.db import models

class Doctor(models.Model):
    # primary key
    doctor_id = models.AutoField(primary_key=True)
    # other fields
    f_name = models.CharField(max_length=24)
    l_name = models.CharField(max_length=24)
    email = models.CharField(max_length=48, unique=True) # no duplicates allowed
    login_method = models.CharField(max_length=10) # facebook/twitter/google
    vessel_pref = models.CharField(max_length=24, default='default') # 'default' or 'algo_id'
    optic_pref = models.CharField(max_length=24, default='default') # 'default' or 'algo_id'
    fovea_pref = models.CharField(max_length=24, default='default') # 'default' or 'algo_id'
    lesion_pref = models.CharField(max_length=24, default='default') # 'default' or 'algo_id'

    def __str__(self):
        args = (
            self.doctor_id, self.f_name, self.l_name, self.email, self.login_method
        )
        return """
            doctor_id: {0}
            f_name: {1}
            l_name: {2}
            email: {3}
            login_method: {4}
        """.format(*args) + '\n'
        
class Patient(models.Model):
    # primary key
    patient_id = models.AutoField(primary_key=True)
    # foreign key
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None)
    # other fields
    f_name = models.CharField(max_length=24)
    l_name = models.CharField(max_length=24)
    record_date = models.DateField() # creation date

    def __str__(self):
        args = (
            self.patient_id, self.doctor, self.f_name, self.l_name, str(self.record_date)
        )
        return """
            patient_id: {0}
            doctor: {1}
            f_name: {2}
            l_name: {3}
            record_date: {4}
        """.format(*args) + '\n'

class Algorithm(models.Model):
    # primary key
    algo_id = models.AutoField(primary_key=True)
    # foreign key
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None)
    # other fields
    record_date = models.DateField() # creation date
    algo_type = models.CharField(max_length=10) # vessel/optic/fovea/lesion
    algo_status = models.CharField(max_length=10) # execution: valid/invalid
    last_modified = models.DateField()
    source_code = models.CharField(max_length=20000, default=None) # actual source code

    def __str__(self):
        args = (self.algo_id, '\n', self.doctor, str(self.record_date), self.algo_type,
            self.algo_status, str(self.last_modified)
        )
        return """
            algo_id: {0} 
            doctor: {1}
            record_date: {2}
            algo_type: {3}
            algo_status: {4}
            last_modified: {5}
        """.format(*args) + '\n'
        
class Diagnosis(models.Model):
    # primary key
    diagnosis_id = models.AutoField(primary_key=True)
    # foreign keys
    doctor = models.ForeignKey(Doctor, on_delete=None, default=None)
    patient = models.ForeignKey(Patient, on_delete=None, default=None)
    vessel_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='vessel')
    optic_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='optic')
    fovea_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='fovea')
    lesion_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='lesion')
    # other fields
    record_date = models.DateField() # creation date
    final_result = models.CharField(max_length=24)

    def __str__(self):
        args = (
            self.diagnosis_id, self.doctor, self.patient, self.vessel_algo, self.optic_algo, 
            self.fovea_algo, self.lesion_algo, str(self.record_date), self.final_result
        )
        return """
            diagnosis_id: {0}
            doctor: {1}
            patient: {2}
            vessel_algo: {3}
            optic_algo: {4}
            fovea_algo: {5}
            lesion_algo: {6}
            record_date: {7}
            final_result: {8}
        """.format(*args) + '\n'