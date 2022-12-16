import os
import shutil
import logging as log
import configparser
import argparse

create_folders=[]
move_from_folders=[]
empty_folders_remove = True
automatically_create_folders = True
move_files_to_root = False

parser = argparse.ArgumentParser(description='A test program.')
config = configparser.ConfigParser()

def write_config_file():
    config.write(open('config.ini', 'w'))

def remove_empty_folders():
    for item in os.listdir(file_path):
        if os.path.isdir(file_path + item) and len(os.listdir(file_path + item)) == 0:
            os.rmdir(file_path + item)
            log.debug("Deleted folder: " + item)


if not os.path.exists('config.ini'):
    config['APP'] = {'debug': 'False', 'file_path': ''}
    write_config_file()

config.read("config.ini")

if config['APP'].getboolean('debug'):
    log.basicConfig(level=log.DEBUG)
else:
    log.basicConfig(level=log.INFO)

file_path = config['APP']['file_path'] #"C:/Users/Miha/Desktop/TestDownloads/" or use r"C:\Users\Miha\Desktop\TestDownloads"
print("Root file path: " + file_path)

parser.add_argument('-p', "--path", help="Sets root file path", default=file_path)
parser.add_argument('-f', "--folders", help="Moves files from specified folders to root folder. Folders must be separated with comma(,)", default="")
parser.add_argument('-mr', "--movetoroot", help="Enables move files to root folder. Set to 1 or 0", default=False)
parser.add_argument('-c', "--createfolders", help="Crates and moves files only to specified folders. Folders must be separated with comma(,)", default="")
args = parser.parse_args()
file_path = args.path
move_from_folders = args.folders.split(',')
move_files_to_root = args.movetoroot
create_folders = args.createfolders.split(',')

if len(create_folders) > 0:
    automatically_create_folders = False

if len(file_path) == 0:
    file_path = input("Set root file path: \n")
    config.set('APP', 'file_path', file_path)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("File path: " + file_path)

#Move all files from folders to root folder
if move_files_to_root:   
    for folder in move_from_folders:
        if os.path.exists(file_path + folder):
            for file in os.listdir(file_path + folder):
                src = os.path.join(file_path, folder, file)

                if os.path.isfile(src):
                    try:
                        shutil.move(src, file_path, copy_function=shutil.copy2)
                    except:
                        log.debug("Source and destination are same")  
#Move files to folders if folder exist
else:
    for file in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, file)):
            file_extension = os.path.splitext(file_path + file)[1][1:] #removes . from extension string

            if automatically_create_folders:
                try:
                    os.makedirs(file_path + file_extension)
                    log.debug("Created folder: " + file_extension)
                except FileExistsError:
                    #directory already exists
                    pass

                if os.path.exists(file_path + file): #if file exists
                    shutil.move(file_path + file, file_path + file_extension + '/', copy_function=shutil.copy2)

            if len(file_extension) == 0:
                continue

#Iterate through root directory and delete empty folders
if empty_folders_remove:
    remove_empty_folders()
