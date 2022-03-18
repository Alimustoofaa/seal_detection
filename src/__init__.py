import os
import cv2
import time
from pathlib import Path
from itertools import chain
from src.app import SealDetection
from .utils import logging, draw_rectangle, datetime_format, sending_file
from config import ID_DEVICE, GATE

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
    
    def save_and_sending_file(self, file, id_file):
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
        cv2.imwrite(f'{path_image}', file)
        
        # Send file to FTP server
        server_path = f'{GATE}/{ID_DEVICE}/{year}-{month}-{day}_{hour}'
        sender = sending_file(file_name=file_name, server_path=server_path)
        if sender:
            os.remove(path_image)
            
        pass
    
    def main(self, image, id=None):
        image_ori = image.copy()
        if not id: id = int(time.time())
        # Detection seal
        result = self.__detection(image, size=None, threshold=0.4)
        if not result: logging.info(f'Seal not found'); image_drawed = image_ori 
        else: logging.info('Seal Found')
        
        # Extract result to list
        result_list = [[[x['bbox'], key,  x['confidence']] for x in value]\
                      for key, value in result.items()]
        result_list = list(chain(*result_list))
        # Draw image and extract result
        for i in result_list:
            image_drawed = draw_rectangle(image_ori, i)
            
        # Save and sending file FTP
        self.save_and_sending_file(image_drawed, id)
        return image_drawed