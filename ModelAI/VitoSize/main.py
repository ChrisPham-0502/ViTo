import pickle
import numpy as np

def size_recommend(weight, height, age, model):
    id2label = {3: 'XL', 0: 'L', 1: 'M', 2: 'S', 5: 'XXS', 6: 'XXXL', 4: 'XXL'}
    X = np.array([weight, age, height]).reshape(1, -1)
    #df = pd.DataFrame(scaler.fit_transform(X), columns=["weight", "age", "height"])
    #X = scaler.fit_transform(X)
    pred = model.predict(X)
    return id2label[pred[0]]

def main():
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    
    scaler = StandardScaler()
    kmeans = KMeans()
    with open("kmeans_model.pkl", 'rb') as f:
        kmeans, scaler = pickle.load(f)
        
    while True:
        weight = float(input("Enter your weight:"))
        age = int(input("Enter your age:"))
        height = float(input("Enter your height:"))
        if None not in [weight, age, height]:
            break
            
    size = size_recommend(weight, height, age, model=kmeans)
    return size

class SR_feature:
    def __init__(self, weight, height, age, model):
        weight = weight
        height = height
        age = age
        model = model
    
    def return_size(weight, height, age, model):
        id2label = {3: 'XL', 0: 'L', 1: 'M', 2: 'S', 5: 'XXS', 6: 'XXXL', 4: 'XXL'}
        X = np.array([weight, age, height]).reshape(1, -1)
        pred = model.predict(X)
        return id2label, pred
        


if __name__=="__main__":
    print(main())