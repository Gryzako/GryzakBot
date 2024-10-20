import time
import pyautogui
import cv2
import threading
from obswebsocket import obsws, requests

class AmuletAndRingDetector():
    def __init__(self):
        self.host = "localhost"
        self.port = '4455'
        self.password = 'Ewelina1234'
        self.pictureOfAmulet = 'C:/Users/michal/Documents/amu.PNG'
        self.pictureOfRing = 'C:/Users/michal/Documents/ring.PNG'
        self.temp_file = "C:/Users/michal/Documents/screenshot.png" 
        #colours
        self.life_target_color = (239, 96, 96) 
        self.mana_target_color = (82, 79, 217)
        #coordinates
        self.manaY = 137
        self.lifeY = 125
        self.almostFullX = 1850
        self.halfX = 1810
        self.lessThenHalfX = 1794


    def connectToOBS(self, host, port, password):
        ws = obsws(host=host, port=port, password=password)
        ws.connect()
        return ws
    
    def disconnectFromOBS(self, connection):
        connection.disconnect()

    def capture_screenshot(self, connection):
        try:
            response = connection.call(requests.GetCurrentProgramScene())
            current_scene = response.datain.get('currentProgramSceneName')
            screenshot_request = requests.SaveSourceScreenshot(sourceName=current_scene, imageFormat="png",imageFilePath=self.temp_file)
            connection.call(screenshot_request)
            return self.temp_file
        except Exception as e:
            print(f'Error: {e}')

    def find_image_on_screenshot(self, template_path, image_path, threshold=0.95):
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f'Nie można wczytać obrazu szablonu: {template_path}')
            return False, None
        if image is None:
            print(f'Nie można wczytać obrazu: {image_path}')
            return False, None
        
        # Match picture to screen
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        # search max value of match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # check is max value of match cross a threshold
        if max_val >= threshold:
            print(f'Znaleziono obraz! Wartość dopasowania: {max_val}')
            return True, max_loc  # Return True + item position (x, y)
        else:
            print(f'Nie znaleziono obrazu. Wartość dopasowania: {max_val}')
            return False, None

    def compare(self, stop_event, ss, might):
        conn = self.connectToOBS(self.host, self.port, self.password)

        while not stop_event.is_set():
            screenShotFromObs = self.capture_screenshot(conn)

            if screenShotFromObs is not None:
                ring = self.find_image_on_screenshot(screenShotFromObs, self.pictureOfRing)
                if ring[0] == True and might == 1:
                    print(f'znaleziono ring: {ring}')
                    pyautogui.press('2')
                amulet = self.find_image_on_screenshot(screenShotFromObs, self.pictureOfAmulet)
                if amulet[0] == True and ss == 1:
                    print(f'znaleziono amulet: {amulet}')
                    pyautogui.press('1')
            time.sleep(1)
        
        conn.disconnect()

    def startAmuAndRingEvent(self, stop_event, ss, might):
        stop_event = threading.Event()
        thread  = threading.Thread(target=self.compare, args=(stop_event, ss, might))
        thread .start()
        return thread , stop_event
    
    def stopAmuAndRingEvent(self, stop_event, process):
        stop_event.set()
        process.join()



            