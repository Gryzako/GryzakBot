import time
import pyautogui
import cv2
from PIL import Image
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
        self.almostFullX = 1845
        self.halfX = 1810
        self.criticalX = 1790

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
        
    def check_pixel_color(self, x, y, target_color, tolerance=5):
        image = Image.open("C:/Users/michal/Documents/screenshot.png" )

        # Get the RGB value of the pixel at the specified coordinates
        pixel_color = image.getpixel((x, y))
        pixel_color_rgb = pixel_color[:3]
        print(pixel_color_rgb)

        r_diff = abs(pixel_color_rgb[0] - target_color[0])
        g_diff = abs(pixel_color_rgb[1] - target_color[1])
        b_diff = abs(pixel_color_rgb[2] - target_color[2])

        # If all differences are within the specified tolerance, return True
        if r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance:
            return True
        else:
            return False
        
    def checkingLife(self, buttons):
        might = buttons[0]
        ss = buttons[1]
        vita = buttons[3]
        try:
            if not self.check_pixel_color(self.criticalX, self.lifeY, self.life_target_color):
                print('stone skin might i utama + leczenie')
            elif not self.check_pixel_color(self.halfX, self.lifeY, self.life_target_color):
                print('max vita')
            elif not self.check_pixel_color(self.almostFullX, self.lifeY, self.life_target_color):
                pyautogui.press(vita)
                print('vita')
        except Exception as e:
            print(e)

    def compare(self, stop_event, buttonStatuses, assignedKeyStatus):
        conn = self.connectToOBS(self.host, self.port, self.password)

        while not stop_event.is_set():
            screenShotFromObs = self.capture_screenshot(conn)

            if screenShotFromObs is not None:
                if buttonStatuses[0] == 1:
                    ring = self.find_image_on_screenshot(screenShotFromObs, self.pictureOfRing)
                    if ring[0] == True:
                        print(f'znaleziono ring: {ring}')
                        pyautogui.press(assignedKeyStatus[0])
                if buttonStatuses[1] == 1:
                    amulet = self.find_image_on_screenshot(screenShotFromObs, self.pictureOfAmulet)
                    if amulet[0] == True:
                        print(f'znaleziono amulet: {amulet}')
                        pyautogui.press(assignedKeyStatus[1])
                if buttonStatuses[2] == 1:
                    if self.check_pixel_color(self.almostFullX, self.manaY, self.mana_target_color):
                        print('Mana Pełna')
                    else:
                        print('doladuj mane')
                        pyautogui.press('0')
                if buttonStatuses[3] == 1:
                    if self.check_pixel_color(self.almostFullX, self.manaY, self.mana_target_color):
                        pyautogui.press('f6')
                        print('tylko runa')
                        time.sleep(1)
                    else:
                        pyautogui.press('0')
                        time.sleep(0.1)
                        pyautogui.press('f6')
                        print('mana i runa')
                if buttonStatuses[4] == 1:
                    self.checkingLife(assignedKeyStatus)

            time.sleep(1)
        conn.disconnect()

    def startAmuAndRingEvent(self, stop_event, buttonStatuses, assignedKeyStatus):
        stop_event = threading.Event()
        thread  = threading.Thread(target=self.compare, args=(stop_event, buttonStatuses, assignedKeyStatus))
        thread.start()
        return thread , stop_event
    
    def stopAmuAndRingEvent(self, stop_event, process):
        stop_event.set()
        process.join()



            