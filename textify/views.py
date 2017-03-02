import json

from PIL import Image
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from textify.exceptions import *
from textify.utils.image_processing import *
from textify.services import drawings, recognition, user


# user services
@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password'].encode('utf-8')
        confirm_pass = request.POST['confirmation'].encode('utf-8')

        try:
            result = user.register_user(email, password, confirm_pass)
            return HttpResponse(result)
        except InvalidEmailFormatException as message:
            return HttpResponseBadRequest(str(message))
        except PasswordsDoNotMatchException as message:
            return HttpResponseBadRequest(str(message))
        except PasswordTooSHortException as message:
            return HttpResponseBadRequest(str(message))
        except ExistingUsernameException as message:
            return HttpResponseBadRequest(str(message))
    else:
        return HttpResponse('Allowed only via POST')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST["email"].encode('utf-8')
        password = request.POST["password"].encode('utf-8')

        try:
            result = user.authenticate_user(email, password)
            return HttpResponse(result)
        except UserDoesNotExistException as e:
            return HttpResponseBadRequest(e)


@csrf_exempt
def textify(request):
    if request.method == 'POST':
        img = PIL.Image.open(request.FILES['img'])
        text = recognition.textify(img)
        return HttpResponse(text)

    return HttpResponse('Allowed only via POST')


@csrf_exempt
def textify_handwritten(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        img = PIL.Image.open(request.FILES['img'])
        text = recognition.textify_handprinted(user_id, img)
        return HttpResponse(text)

    return HttpResponse('Allowed only via POST')


# machines and images server logic
@csrf_exempt
def upload_drawings(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        label_index = request.POST['label_index']
        name = request.POST['name']
        file = request.FILES[name]

        is_successful = drawings.upload_drawings(user_id, name, label_index, file)

        if is_successful:
            return HttpResponse()
        else:
            raise Http404("User does not exist")
    else:
        return HttpResponse('Allowed only via POST')


@csrf_exempt
def get_drawings(request):
    user_id = request.POST['userId']
    label = request.POST['label']
    user_drawings = drawings.get_drawings(user_id, label)
    return HttpResponse(json.dumps(user_drawings), content_type="application/json")


@csrf_exempt
def train_machines(request):
    if request.method == 'POST':
        user_id = request.POST["user_id"]

        try:
            recognition.schedule_training(user_id)
            return HttpResponse('Classifier is now being trained!')
        except UserDoesNotExistException as e:
            raise Http404(e)
        except MachineCurrentlyTrainingException as m:
            return HttpResponseBadRequest(m)


@csrf_exempt
def check_completion(request):
    if request.method == 'GET':
        user_id = request.GET["user_id"]

        try:
            recognition.check_for_completion(user_id)
            return HttpResponse('Training completed!')
        except UserDoesNotExistException as e:
            raise Http404(e)
        except MachineCurrentlyTrainingException as m:
            return HttpResponseBadRequest(m)
