from utils import logging
from src.app import SealDetection


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
                detection(image=image, size=size)
        result  = self.seal_detection.\
                extract_result(results=results, min_confidence=threshold)
        return result
        
    def main(self, image):
        # Detection seal
        result = self.__detection(image, 480, threshold=0.4)
        if not result: logging.info(f'Seal not found'); return list()
        else: logging.info('Seal Found')
        
        # Extract result to list
        result_list = [[[x['bbox'], key,  x['confidence']] for x in value]\
                      for key, value in result.items()][0]
        # Draw image
# def process(image)