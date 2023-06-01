from scipy.spatial import distance as dist
import cv2
import mediapipe as mp
import numpy as np

#Define um set com o 2 olhos 
FACEMESH_EYES = frozenset().union(*[mp.solutions.face_mesh.FACEMESH_LEFT_EYE, 
                                    mp.solutions.face_mesh.FACEMESH_RIGHT_EYE])

#define os pontos para o olho esquedo
LEFT_EYE  = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
#define os pontos para o olho direito
RIGHT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]

# Define duas constantes, uma para o EAR que indica
# um piscar de olhos e uma segunda constante para o número de quadros consecutivos
# que o olho deve estar abaixo do limiar para disparar o alarme
LIMIAR_EAR = 0.22
QTD_CONSEC_FRAMES = 5

class BlinkDetector():
    def __init__(self, staticMode=False, maxFaces=1, minDetectConf=0.5, minTrackConf=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectConf = minDetectConf
        self.minTrackConf = minTrackConf
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.staticMode, 
                                                 max_num_faces=self.maxFaces,
                                                 refine_landmarks=True,
                                                 min_detection_confidence=self.minDetectConf,
                                                 min_tracking_confidence=self.minTrackConf)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=2, circle_radius=1)
        
    def findFaceMesh(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ih, iw, _ = img.shape
        faces = []
        results = self.faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            for lms in results.multi_face_landmarks:
                mesh_points = np.array([np.multiply([p.x, p.y], [iw, ih]).astype(int) for p in lms.landmark])
                cv2.polylines(img, [mesh_points[LEFT_EYE]], True, (0,255,0), 1, cv2.LINE_AA)
                cv2.polylines(img, [mesh_points[RIGHT_EYE]], True, (0,255,0), 1, cv2.LINE_AA)
                faces.append(mesh_points)

        return img, faces


    # Função para calcular a relação de aspecto dos olhos (EAR)
    def calcular_ear(self, landmarks, eye):
        # Calcula as distâncias euclidianas entre os dois conjuntos de
        # marcos oculares verticais (coordenadas x, y)
        A = dist.euclidean(landmarks[eye[12]], landmarks[eye[3]]) 
        B = dist.euclidean(landmarks[eye[11]], landmarks[eye[4]])

        # Calcula a distância euclidiana entre os marcos oculares horizontais
        # (coordenadas x, y)
        C = dist.euclidean(landmarks[eye[0]], landmarks[eye[8]])

        # Calcula e retorna o EAR
        return ((A + B) / (2.0 * C))
    
    def is_blinking(self, face):
        ear_dir = self.calcular_ear(face, RIGHT_EYE)
        ear_esq = self.calcular_ear(face, LEFT_EYE)

        ear = (ear_esq + ear_dir) / 2.0

        return  ((ear < LIMIAR_EAR), ear)