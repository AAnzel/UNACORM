import os
import time
import shutil


path_uploaded = os.path.join('..', 'Data', 'uploaded')
path_uploaded_txt = os.path.join(path_uploaded, 'txt')
path_uploaded_jpg = os.path.join(path_uploaded, 'jpg')
path_uploaded_wav = os.path.join(path_uploaded, 'wav')
path_encoded_data = os.path.join('..', 'Data', 'Encoded')
path_decoded_data = os.path.join('..', 'Data', 'Decoded')
path_encoded_dna = os.path.join('..', 'Data', 'Encoded', 'DNA')
path_decoded_dna = os.path.join('..', 'Data', 'Decoded', 'DNA')

path_uploaded_dict = {
    'txt': path_uploaded_txt,
    'jpg': path_uploaded_jpg,
    'wav': path_uploaded_wav
}


def remove_cached_data():

    SAVE_TIME = 3600  # Time is given in seconds, 5400s = 1.5h, 3600 = 1h
    time_limit = time.time() - SAVE_TIME

    # Traversing every cache directory and deleting everything from it
    for subdir in os.listdir(path_uploaded):
        subdir_path = os.path.join(path_uploaded, subdir)
        for file_name in os.listdir(subdir_path):
            if 'gitkeep' in file_name:
                continue
            else:
                file_path = os.path.join(subdir_path, file_name)

                # Check if file is older than 1h, and if yes, delete it
                if os.stat(file_path).st_mtime < time_limit:
                    try:
                        if os.path.isfile(file_path) or\
                                os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except OSError as e:
                        print('Failed to delete ' + file_path + '. Reason: '
                              + e)

                    print('Successfully removed everything from ' + subdir +
                          ' data set')

                else:
                    pass

    return None


remove_cached_data()
