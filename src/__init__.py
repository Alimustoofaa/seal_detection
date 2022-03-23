import os
from urllib import response
import cv2
import time
import requests

from datetime import datetime
from pathlib import Path
from itertools import chain
from src.app import SealDetection
from .utils import logging, draw_rectangle, datetime_format, sending_file

from config import DEVICE_ID, GATE_ID,END_POINT,SEND_TIMEOUT,READ_TIMEOUT
from config import DATETIME_FORMAT,TIMEID_FORMAT,DELAY_IN_SECONDS,FTP_HOST, USER_NAME, USER_PASSWD

from io import BytesIO
import ftplib
import requests
from requests.exceptions import HTTPError
from datetime import datetime

class MainProcess:
	'''
		Main process seal detection
	'''
	def __init__(self):
		self.seal_detection = SealDetection('seal_detection')

	def __detection(self, image, size, threshold):
		'''
			Detection object
			Args:
				image(np.array) : image for detection
				size(int)       : size image detection
				threshold(float): min confidence
			Return:
				result(dict): {
				casess:[{
					confidence(float): confidence,
					bbox(list) : [x_min, y_min, x_max, y_max]
				}]
			}
		'''
		results = self.seal_detection.\
				detection(image=image, image_size=size)
		result  = self.seal_detection.\
				extract_result(results=results, min_confidence=threshold)
		return result
	
	""" def __save_and_sending_file(self, file, id_file):
		'''
			Send image to server
			Args:
				file_path(str): path of image
			Return:
				
		'''
		# Save File
		year, month, day, hour, _, _,_ = datetime_format()
		save_path = f'results/{year}/{month}/{day}/{hour}'
		Path(save_path).mkdir(parents=True, exist_ok=True)
		
		file_name   = f'{id_file}.jpg'
		path_image  = f'{save_path}/{file_name}'
		print(path_image)
		cv2.imwrite(f'{path_image}', file)
		
		# Send file to FTP server
		server_path = f'{GATE}/{ID_DEVICE}/{year}-{month}-{day}_{hour}'
		#sender = sending_file(file_name=file_name, server_path=server_path)
		#if sender:
		 #   os.remove(path_image)
			
		return server_path
	
	@staticmethod
	def __send_api(server_path, start_time, end_time):
		
		#send json to API
		result_json = {
			'gateId'    : GATE,
			'deviceId'  : ID_DEVICE,
			'result'    : 0,
			'box'       : 
				{
				'x_min': 10,
				'y_min': 11,
				'x_max': 12,
				'y_max': 13
			},
			'filePath'  : server_path,
			'startTime' : datetime.fromtimestamp(start_time),
			'endTime'   : datetime.fromtimestamp(end_time),
			'delayInSeconds' : 2
			
		}
		response = requests.post(url = f'{IP_API}/{END_POINT}', data = result_json)
		print(response)
		try:
			if response.status_code() == 200:
				logging.info(f'Send API success')
				return True
		except:
			logging.error('Cannot send data to API')
			return False """
	def chdir(self,ftp_path, ftp_conn):
		dirs = [d for d in ftp_path.split('/') if d != '']
		for p in dirs:
			self.check_dir(p, ftp_conn)


	def check_dir(dir, ftp_conn):
		filelist = []
		ftp_conn.retrlines('LIST', filelist.append)
		found = False

		for f in filelist:
			if f.split()[-1] == dir and f.lower().startswith('d'):
				found = True

		if not found:
			ftp_conn.mkd(dir)
		ftp_conn.cwd(dir)

	def img_upload(self,img,time_id):
		try:
			year, month, day, hour, _, _,_ = datetime_format()
			dest_path = f'/{GATE_ID}/{year}/{month}/{day}/'
			"""Transfer file to FTP."""
			# Connect
			session = ftplib.FTP(FTP_HOST, USER_NAME, USER_PASSWD)
			session.set_pasv(False)
			# Change to target dir
			self.chdir(dest_path,session)

			# Transfer file
			name = time_id.strftime(TIMEID_FORMAT)[:-4]
			file_name  = f'{DEVICE_ID}{name}.jpg'
			logging.info("Transferring %s to %s..." % (file_name,dest_path))
			print("Transferring %s to %s..." % (file_name,dest_path))
			#using memory, can also use file
			retval, buffer = cv2.imencode('.jpg', img)
			flo = BytesIO(buffer)
			session.storbinary('STOR %s' % os.path.basename(dest_path+file_name), flo)
			
			# Close session
			session.quit()
			return dest_path+file_name
		except:
			logging.info('error: upload file error')
			return 'error: upload file error'
	def send_data(self,result, confidence, file_path, start_time, end_time): 
		try:
			url= END_POINT+'seal/'
			x_min_c=y_min_c=x_max_c=y_max_c=0
			json_data = {
				'gateId': GATE_ID,
				'deviceId': DEVICE_ID,
				'result': result,
				'confidence': confidence,
				'box' : {
					"x_min": x_min_c,
					"y_min": y_min_c,
					"x_max": x_max_c,
					"y_max": y_max_c
				},
				'filePath': file_path,
				'startTime': start_time.strftime(DATETIME_FORMAT),
				'EndTime': end_time.strftime(DATETIME_FORMAT),
				'delayInSeconds' : DELAY_IN_SECONDS,
			}
			print('sending...')
			print(json_data)
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			r = requests.post(url=url,json=json_data,headers=headers,timeout=(SEND_TIMEOUT,READ_TIMEOUT))
			ret = r.json()
			return ret
		except HTTPError as e:
			print(e.response.text)
		except:
			return 'send error'

	def main(self, image):
		image_ori = image.copy()
		if not id: id = datetime.now()
		# Detection seal
		result = self.__detection(image, size=360, threshold=0.2)
		if not result: logging.info(f'Seal not found'); image_drawed = image_ori 
		else: logging.info(f'Seal Found : {result}')
		
		# Extract result to list
		result_list = [[[x['bbox'], key,  x['confidence']] for x in value]\
					  for key, value in result.items()]
		result_list = list(chain(*result_list))

		# Draw image and extract result
		for i in result_list:
			image_drawed = draw_rectangle(image_ori, i)
		
		""" # Save and sending file FTP
		try: server_path = self.__save_and_sending_file(image_drawed, id)
		except: pass
		
		# send data to API
		try: self.__send_api(server_path, start_time=id, end_time=id)
		except: pass """
		
		path = self.img_upload(image_drawed,id)
		if 'error' in path :
			path=''
		end_time = datetime.now()
		self.send_data(1 if result else 0,0,path,id,end_time)
		return image_drawed
