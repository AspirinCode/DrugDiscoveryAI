from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
import os
from . import helpers as hp
from . import forms as fo
from . import models as mo

# Create your views here.


def success(request):
    return render(request, "generative_model/success.html")


def home(request):
    context = {
        'form' : fo.GenerativeForm()
    }
    if request.method == "POST":
        form = fo.GenerativeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            complex = form.cleaned_data
            input_path = os.path.abspath(os.path.join(mo.GENERATIVE_OUT, str(complex["sdf"])))
            output_dir = hp.launch_generative_model(input_path)
            zip_file = hp.make_zip(output_dir)
            zip_file_obj = open(zip_file, 'rb')
            return FileResponse(zip_file_obj)
        else:
            raise(form.errors)
    else:
        return render(request, "generative_model/generative.html", context)

def RNN(request):
    return render(request, "generative_model/rnn.html")

def VAE(request):
    return render(request, "generative_model/vae.html")

