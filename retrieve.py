import os, sys, ftplib
from wradlib_io import *
from config import *

'''
Create the directory structure for the project.

@param directories - List of directories to create.
'''
def CreateDirectoryStructure(directories):
  for directory in directories:
    if not os.path.exists(directory):
      os.makedirs(directory)

def retrieve_radar(path = 'data/raw', download = -1):
  ftp = ftplib.FTP(config['ftp_host'])
  ftp.login(config['ftp_username'], config['ftp_password'])
  ftp.cwd('weather/radar/composit/pg/')

  filesTemp = ftp.nlst()
  files = []
  for x in filesTemp:
      if x.endswith("bin"):
          files.append(x)
  exfiles = os.listdir(path)
  downloaded = 0
  newFiles = []
  for file in files:
    if file not in exfiles and (download == -1 or download > downloaded):
      ftp.retrbinary('RETR ' + file, open(os.path.join(path, file), 'wb').write)
      downloaded += 1
      newFiles.append(file)
      sys.stdout.write('  Downloaded ' + str(downloaded) + ' new radar images from max ' + str(len(files)) + '!   \r')
      sys.stdout.flush()

  ftp.quit()
  print(' ')
  return newFiles

def retrieve_fx(path = 'data/fx', download = -1):
  ftp = ftplib.FTP(config['ftp_host'])
  ftp.login(config['ftp_username'], config['ftp_password'])
  ftp.cwd('weather/radar/composit/fx/')

  filesTemp = ftp.nlst()
  files = []
  for x in filesTemp:
      if x.endswith("bz2"):
          files.append(x)
  exfiles = os.listdir(path)
  downloaded = 0
  newFiles = []
  for file in files:
    if file not in exfiles and (download == -1 or download > downloaded):
      ftp.retrbinary('RETR ' + file, open(os.path.join(path, file), 'wb').write)
      downloaded += 1
      newFiles.append(file)
      sys.stdout.write('  Downloaded ' + str(downloaded) + ' new radar fz from max ' + str(len(files)) + '!   \r')
      sys.stdout.flush()

  ftp.quit()
  print(' ')
  return newFiles

def convert_composite_files(files, src = 'data/raw', dst = 'data/converted'):
  x = config['center_x']
  y = config['center_y']
  c = config['size']
  for i, file in enumerate(files):
    data, metadata = read_RADOLAN_composite(os.path.join(src, file))
    data = np.flipud(data)
    np.savetxt(os.path.join(dst, file + '.csv'), data[x-c:x+c,y-c:y+c], delimiter=',', fmt='%d')
    sys.stdout.write('  Converted ' + str(i) + ' radar images from ' + str(len(files)) + '!   \r')
    sys.stdout.flush()

if __name__ == '__main__':
  CreateDirectoryStructure(['data/raw', 'data/converted', 'data/fx'])
  files = retrieve_radar()
  print(str(len(files)) + ' new radar files!')

  files = retrieve_fx()
  print(str(len(files)) + ' new fx files!')
