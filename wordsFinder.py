import subprocess
from winreg import *
from PIL import Image, ImageEnhance, ImageFilter

class WordsFinder():

    def __init__(self):
        self.tesseract_path = self.findTesseract()
        self.letters = self.getLetters()

    def findTesseract(self):
        key = r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        oKey = OpenKey(HKEY_LOCAL_MACHINE, key)
        unistall_path = ''
        try:
            i = 0
            while True:
                subkey = EnumKey(oKey, i)
                newKey = key+'\\'+subkey
                oSub = OpenKey(HKEY_LOCAL_MACHINE, newKey)
                try:
                    if 'Tesseract' in QueryValueEx(oSub, 'DisplayName')[0]:
                            unistall_path = QueryValueEx(oSub, 'UninstallString')[0]
                            break
                except:
                    pass
                CloseKey(oSub)
                i += 1
        except WindowsError as e:
            print(str(e))

        tesseract = '\\'.join(unistall_path.split('\\')[:-1])
        return tesseract+'\\tesseract'

    def getLetters(self):
        letters = ''
        letlist = []
        image = Image.open('letters.bmp').convert('L')
        bw = image.point(lambda x: 255 if x<220 else 0, '1')
        bw.save('letters_bw.bmp')
        command = '"'+self.tesseract_path+'" letters_bw.bmp letters -l ces'
        subprocess.call(command)
        with open('letters.txt', 'r', encoding='utf8') as file:
            for line in file:
                lines = line.strip()
                for letter in lines:
                    letlist.append(letter.lower())

        print(letlist)
        return letlist

    def testWord(self, word):
        l = self.letters[:]
        for letter in word.strip('\n'):
            if letter in l:
                l.remove(letter)
            else:
                return False
        return True