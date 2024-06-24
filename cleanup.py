import os
import shutil

def cleanUp():
    dir = os.path.join("download")
    try:
        if os.path.exists(dir):
            shutil.rmtree(dir)

        os.mkdir(dir)

    except Exception as e:
        print(e)

def cleanOne(name):
    dir = os.path.join("doenload", name)
    try:
        if os.path.exists(dir):
            os.remove(dir)

    except Exception as e:
        print(e)