import json
import shutil
import zipfile


with open('serverless-include.json', 'r') as inc_file:
    files_to_keep = json.loads(inc_file.read())

for service_name, file_to_keep in files_to_keep.items():
    archive = zipfile.ZipFile('.serverless/' + service_name + '.zip')
    for file in archive.namelist():
        if file in file_to_keep:
            archive.extract(file, '.serverless/exclude-' + service_name)

    print(shutil.make_archive('.serverless/' + service_name, 'zip',
                              '.serverless/exclude-' + service_name))
    shutil.rmtree('.serverless/exclude-' + service_name)
