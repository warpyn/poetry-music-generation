from poem_VA_model import*
import pandas as pd
import math

class VAcalculator:

    def read_emotion_file_to_VA_dic(self, file_path):
        emotion_dataframe = pd.read_csv(file_path)
        emotion_dic = emotion_dataframe.to_dict(orient='records')
        VA_format = {emotion['word']: [emotion['valance'], emotion['arousal']] for emotion in emotion_dic}
        return VA_format


    def __init__(self, emotions, emotion_data_path = './content/emotionVAScaled.csv'):
        self.emotion_dic = self.read_emotion_file_to_VA_dic(emotion_data_path)
        self.emotions = emotions
        

    def get_VA_vectors(self, kept_emotions):
        VA_vectors = []
        for emotion in kept_emotions:
            emo = emotion['label']
            VA_vectors.append([self.emotion_dic[emo], emotion['score']])
        return VA_vectors #format: [[[v1,a1], prob2], [[v2,a2], prob2]...]
    
    def get_VA_sum(self, VA_vectors):
        vector_sum = [0, 0]
        weight_sum = 0
        for vector in VA_vectors:
            vector_sum[0] += vector[0][0] * vector[1]
            vector_sum[1] += vector[0][1] * vector[1]
            weight_sum += vector[1]
        return vector_sum, weight_sum
    
    # def VA_normalize(self, VA_vector_sum):
    #     sum_of_squares = VA_vector_sum[0] ** 2 + VA_vector_sum[1] ** 2
    #     magnitude = math.sqrt(sum_of_squares)
    #     sum_normalized = [VA_vector_sum[0] / magnitude, VA_vector_sum[1] / magnitude]
    #     return sum_normalized

    def VA_weighting(self, VA_vector_sum, weight_sum):
        sum_normalized = [VA_vector_sum[0] / weight_sum, VA_vector_sum[1] / weight_sum]
        return sum_normalized
            
    
    def wrapper(self, emotions):
        VA_vectors = self.get_VA_vectors(emotions)
        vector_sum, weight_sum = self.get_VA_sum(VA_vectors)
        # sum_normalized = self.VA_normalize(vector_sum)
        sum_normalized = self.VA_weighting(vector_sum, weight_sum)
        return sum_normalized
    

# if __name__ == "__main__":
#     kept_emotions = [{'label': 'joy', 'score': 0.8082323670387268}, {'label': 'anger', 'score': 0.051088836044073105}, {'label': 'annoyance', 'score': 0.03365428373217583}, {'label': 'neutral', 'score': 0.0223822221159935}]
#     my_calculator = VAcalculator(kept_emotions)
#     # vector = my_calculator.get_VA_vectors(kept_emotions)
#     # print(vector)
#     result = my_calculator.wrapper(kept_emotions)
#     print(result)
