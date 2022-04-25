import json
import shutil
import zipfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="path of the .json file with the configuration")
args = parser.parse_args()

config_file = 'serverless-include.json'
if args.config:
    config_file = str(args.config)

folder_to_keep = {}
files_to_keep = {}

with open(config_file, 'r') as inc_file:
    inc_dict = json.loads(inc_file.read())
    for pname in inc_dict:
        for path in inc_dict[pname]:
            if path.startswith('*'):
                folder_to_keep[pname] = path[1:]
            else:
                files_to_keep[pname] = path

for service_name, file_to_keep in files_to_keep.items():
    archive = zipfile.ZipFile('.serverless/' + service_name + '.zip')
    for file in archive.namelist():
        if file in file_to_keep:
            archive.extract(file, '.serverless/exclude-' + service_name)

for service_name, folder_to_keep in folder_to_keep.items():
    archive = zipfile.ZipFile('.serverless/' + service_name + '.zip')
    for file in archive.namelist():
        for folder in folder_to_keep:
            if file.startswith(folder):
                archive.extract(file, '.serverless/exclude-' + service_name)

    print(shutil.make_archive('.serverless/' + service_name, 'zip',
                              '.serverless/exclude-' + service_name))
    shutil.rmtree('.serverless/exclude-' + service_name)
