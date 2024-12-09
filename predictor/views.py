from django.shortcuts import render

from django.shortcuts import render
from .forms import PredictionForm
from .utils import district_mapping, predict_groundwater

def predict_view(request):
    result = None
    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            district = district_mapping[form.cleaned_data['district']]
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            result = predict_groundwater(district, latitude, longitude, month, year)
    else:
        form = PredictionForm()
    return render(request, "predictor/templates/predict.html", {"form": form, "result": result})
