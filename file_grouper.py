import os
import platform
import datetime
import shutil
import ntpath
import sys

def group_files(src_dir, output_dir):
    files_by_c_year = group_by_creation_year(src_dir, output_dir)
    
    print("Files were successfully scanned. Copying... ")
    counter = 0
    # copy and group the files
    files_count = sum(map(len, files_by_c_year.values()))
    for year, f_names in files_by_c_year.items():
        year_dir_name = output_dir + '/' + str(year)
        os.makedirs(year_dir_name) # raises exeption if dir already exists
        for absolute_file_name in f_names:
            file_name_only = ntpath.basename(absolute_file_name)
            shutil.copy2(absolute_file_name, year_dir_name+ "/" + file_name_only)
            counter+=1
            proggress_percentage = (counter / files_count) * 100
            update_proggress(proggress_percentage)
   
    print("  Copying finished")
      
def group_by_creation_year(src_dir, output_dir):
    """Returns a dict with key: creation year of the files and value: list of file names 
    """
    files_by_c_year = {}
    # traverse and collect files data
    print("Scanning files started.")
    for cur, _dirs, files in os.walk(src_dir):
        # if out_dir already exist -> throw error cause we dont want to override existing files
        if output_dir == cur:
            raise Exception("Output dir is already existing!") 
            
        for file in files:
            file_name = cur + '/'+ file
            c_year = get_creation_date(file_name).year
            if c_year in files_by_c_year:
                files_by_c_year[c_year].append(file_name)
            else:
                file_names_by_year = []
                file_names_by_year.append(file_name)
                files_by_c_year[c_year] = file_names_by_year
    return files_by_c_year

def update_proggress(proggress_perc):
    print('\r[{0}] {1:.2f}%'.format('#' * int((proggress_perc // 10)), proggress_perc), end= "", flush= True) 

def get_creation_date(file_name):
    t = generate_creation_date_timestamp(file_name)
    return datetime.datetime.fromtimestamp(t)

def generate_creation_date_timestamp(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
        
if __name__ == "__main__":
    src_dir = sys.argv[1].strip()
    dest_dir = sys.argv[2].strip()
    
    if os.path.isabs(src_dir) and os.path.isabs(dest_dir):
        group_files(src_dir, dest_dir)
    else: 
        raise Exception("src and dest dirs should be absolute!")
