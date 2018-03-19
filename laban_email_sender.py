import os
import xml.etree.ElementTree as ET
from email_sender import EmailSender
import time

xml_folder = '/Users/felipelnv/Documents/openFrameworks/of_v0.9.8_osx/apps/Labam/00_laban/bin/data/xmlOutput'
img_folder = '/Users/felipelnv/Documents/openFrameworks/of_v0.9.8_osx/apps/Labam/00_laban/bin/data/imgOutput'
xml_folder += '/'
img_folder += '/'
extension = '.gif'

start_time = time.time()

print('Laban email sender activated...')

while True:
    new_files = False
    for file in os.listdir(xml_folder):
        if file.endswith('.xml'):
            new_files = True
            xml_path = xml_folder + file
            tree = ET.parse(xml_path)
            root = tree.getroot()
            email_to = root[0].text
            file_name = root[1].text + extension
            email_sender = EmailSender(img_folder)
            email_sender.send_email(email_to, file_name)
            os.remove(xml_path)
    if not new_files:
        print('No new files found in xml folder.')
    elapsed_time = time.time() - start_time
    if elapsed_time > 600:
        imgs_to_remove = False
        for file in os.listdir(img_folder):
            if file.endswith(extension):
                imgs_to_remove = True
                file_path = img_folder + file
                os.remove(file_path)
        if imgs_to_remove:
            print('Old images have been removed from images folder.')
        else:
            print('No old images found in images folder.')
        start_time = time.time()
    print('Having a little nap.')
    time.sleep(30)
