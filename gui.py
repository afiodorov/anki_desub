import os
import os.path
import Tkinter as tk
import PIL.Image as image


def isImage(filepath):
    filename, fileExt = os.path.splitext(filepath)
    return fileExt in ['.jpg', '.png', '.gif']


def getImages(path):
    return filter(isImage, next(os.walk(path))[2])


def resizeImage(imagePath):
    maxWidth, maxHeight = (250, 250)
    imageTempPath = os.path.join('tmp', imagePath)
    try:
        originalImage = image.open(imageTempPath)
    except IOError:
        originalImage = image.open(imagePath)

        if(originalImage.width > maxWidth):
            scalingFactorW = originalImage.width / maxWidth
        if(originalImage.height > maxHeight):
            scalingFactorH = originalImage.height / maxHeight

        scalingFactor = max(scalingFactorW, scalingFactorH)

        if scalingFactor > 1.0:
            newWidth = originalImage.width / scalingFactor
            newHeight = originalImage.height / scalingFactor
            resizedImaged = originalImage.resize((newWidth, newHeight),
                                                 image.ANTIALIAS)
            resizedImaged.save(imageTempPath)

    return imageTempPath


class Application(tk.Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "left"})

        self.photoImages = []
        for imagePath in getImages('.'):
            imageTk = tk.PhotoImage(file=resizeImage(imagePath))
            label = tk.Label(self, image=imageTk)
            label.image = imageTk
            label.pack()
            self.photoImages.append(image)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
