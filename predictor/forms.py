from django import forms

class PredictionForm(forms.Form):
    
    district = forms.ChoiceField(choices=[
        ('Araria', 'Araria'), ('Arwal', 'Arwal'), ('Aurangabad', 'Aurangabad'), 
        ('Banka', 'Banka'), ('Begusarai', 'Begusarai'), ('Bhagalpur', 'Bhagalpur'),
        ('Bhojpur', 'Bhojpur'), ('Buxar', 'Buxar'), ('Darbhanga', 'Darbhanga'),
        ('Gaya', 'Gaya'), ('Gopalganj', 'Gopalganj'), ('Jamui', 'Jamui'),
        ('Jehanabad', 'Jehanabad'), ('Kaimur (Bhabua)', 'Kaimur (Bhabua)'), ('Katihar', 'Katihar'),
        ('Khagaria', 'Khagaria'), ('Kishanganj', 'Kishanganj'), ('Lakhisarai', 'Lakhisarai'),
        ('Madhepura', 'Madhepura'), ('Madhubani', 'Madhubani'), ('Nawada', 'Nawada'),
        ('Munger', 'Munger'), ('Muzaffarpur', 'Muzaffarpur'), ('Nalanda', 'Nalanda'),
        ('Pashchim Champaran', 'Pashchim Champaran'), ('Patna', 'Patna'), 
        ('Purba Champaran', 'Purba Champaran'), ('Purnia', 'Purnia'), ('Rohtas', 'Rohtas'),
        ('Saharsa', 'Saharsa'), ('Samastipur', 'Samastipur'), ('Saran (Chhapra)', 'Saran (Chhapra)'),
        ('Sheikhpura', 'Sheikhpura'), ('Sheohar', 'Sheohar'), ('Sitamarhi', 'Sitamarhi'),
        ('Siwan', 'Siwan'), ('Supaul', 'Supaul'), ('Vaishali', 'Vaishali')

    ])
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    month = forms.IntegerField()
    year = forms.IntegerField()