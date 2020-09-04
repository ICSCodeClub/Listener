import os
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

download_path = os.path.abspath('requirements')

def get_pyaudio():
    os.system('pipwin install pyaudio')

def delete():
    '''Deletes the last downloaded file'''
    if os.path.exists(os.path.join(download_path,'SoundVolumeView.exe')):
        os.remove(os.path.join(download_path,'SoundVolumeView.exe'))
    try:
        os.rmdir(download_path)
    except OSError:
        pass

def download(path=download_path, clean=True):
    '''Downloads a new SoundVolumeView'''
    global download_path
    if path != download_path and os.path.abspath(path) != download_path:
        if clean:
            delete()
        download_path = os.path.abspath(path)

    if os.path.exists(os.path.join(download_path,'SoundVolumeView.exe')):
        return
    
    os.makedirs(path,exist_ok=True)
    resp = urlopen("https://www.nirsoft.net/utils/soundvolumeview-x64.zip")
    with ZipFile(BytesIO(resp.read())) as f:
        f.extract('SoundVolumeView.exe',path=download_path)

def enable(device:str):
    command('Enable',device)

def disable(device:str):
    command('Enable',device)

def toggle(device:str):
    command('DisableEnable',device)

def command(cmd:str, args, wait_for:int=-1):
    if isinstance(args, list):
        args = ' '.join(args)
    if wait_for >= 0:
        args = str(args) + ' /WaitForItem ' + str(wait_for)
    
    try:
        os.system(os.path.join(download_path,'SoundVolumeView.exe')+' /'+cmd+' '+args)
        return True
    except OSError:
        import warnings
        warnings.warn('Sound Volume View command failed: '+cmd+' '+args)
        return False


if __name__ == "__main__":
    print('Downloading to ./aaa')
    download(path='aaa')

    print('Cleaning and downloading to ./requirements')
    download(path='requirements')

    print('Toggling Stereo Mixer')
    toggle('Stereo Mixer')