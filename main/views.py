import uuid
import cv2
import face_recognition
from django.http import StreamingHttpResponse
from django.shortcuts import render
from flask import redirect
from .models import *
import datetime
from datetime import datetime



def index(request):
    return render(request, 'main/index.html')

def createUser(request):
    return render(request, 'main/createUser.html')

def reconhecimento_facial(request):
    return render(request, 'main/reconhecimento_facial.html')


def estacaoForms(request):
    mac_address = obter_mac_address()
    return render(request, 'main/estacao_form.html' , {'mac_address': mac_address})

def adicionar_pessoa(request):
    if request.method == 'POST':
        nome = request.POST['name']
        foto = request.FILES['photo']
        pessoa = Pessoa(name=nome, photo=foto)
        pessoa.save()
    return render(request, 'main/createUser.html')


def obter_mac_address():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return mac_address

class FaceRecognition:
    def __init__(self):
        self.mac_address = obter_mac_address()
        self.known_face_encodings = []
        self.known_face_names = []
        self.encode_faces()

    def encode_faces(self):
        for pessoa in Pessoa.objects.all():
            face_image = face_recognition.load_image_file(pessoa.photo.path)
            if len(face_recognition.face_encodings(face_image)) > 0:
                face_encoding = face_recognition.face_encodings(face_image)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(pessoa.name)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()

            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_face_names[first_match_index]
                    face_names.append(name)

                #Parte de reconhecimento facial
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    if name != "Unknown":
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Face reconhecida: {name}, Tempo: {now}, MAC Address: {self.mac_address}")

                    estacao_trabalho = EstacaoTrabalho.objects.get(mac_address = self.mac_address)
                    registro_acesso = RegistroAcesso.objects.create(pessoa=Pessoa.objects.get(name=name), estacao_trabalho=estacao_trabalho, data_hora_acesso=datetime.now(), mac_address=self.mac_address)
                    registro_acesso.save()



                ret, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video_feed(self, request):
        return StreamingHttpResponse(self.run_recognition(), content_type='multipart/x-mixed-replace; boundary=frame')

face_recognition_instance = FaceRecognition()
def video_feed(request):
    return face_recognition_instance.video_feed(request)

def estacao_create(request, mac_address_param=None):
    if request.method == 'POST':
        name = request.POST['name']
        if EstacaoTrabalho.objects.filter(mac_address=mac_address_param).exists():
            return render(request, 'main/estacao_form.html', {'mac_address': mac_address_param, 'error_message': 'Endereço MAC já existe'})

        else:
            EstacaoTrabalho.objects.create(name=name, mac_address=mac_address_param)
            return redirect('index')

    # Se o método não for POST, apenas renderize o formulário
    return render(request, 'main/estacao_form.html')
