from django.db import models
import csv
from datetime import datetime

# Create your models here.
class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def load_data(file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=[
                'Voter ID Number', 'Last Name', 'First Name', 'Residential Address - Street Number',
                'Residential Address - Street Name', 'Residential Address - Apartment Number',
                'Residential Address - Zip Code', 'Date of Birth', 'Date of Registration',
                'Party Affiliation', 'Precinct Number', 'v20state', 'v21town', 'v21primary',
                'v22general', 'v23town', 'voter_score'
            ])
            next(reader)  # Skip the header row
            for row in reader:
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row.get('Residential Address - Apartment Number', ''),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'].strip().upper() == 'TRUE',
                    v21town=row['v21town'].strip().upper() == 'TRUE',
                    v21primary=row['v21primary'].strip().upper() == 'TRUE',
                    v22general=row['v22general'].strip().upper() == 'TRUE',
                    v23town=row['v23town'].strip().upper() == 'TRUE',
                    voter_score=int(row['voter_score'])
                )