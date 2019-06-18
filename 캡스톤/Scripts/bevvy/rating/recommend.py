#!/usr/bin/env python
# coding: utf-8

# In[ ]:
def reco(request) :
    #원하는 한명에게만 나오게 하기
    import time
    import pandas as pd
    from surprise import Dataset
    from surprise import Reader
    from surprise import BaselineOnly
    #db 불러오기
    from rating.models import Beer # 안쓰임
    from rating.models import RatingBeer
    from time import sleep ## 저장되는 시간을 벌어주는거
    sleep(0.5) ## 저장되는시간 벌어준거 저장되면서 이게 실행 안되도록

    user = RatingBeer.objects.values_list('user_id', flat=True)
    beer = RatingBeer.objects.values_list('beer_id', flat=True)
    rate = RatingBeer.objects.values_list('rate', flat=True)
    rating_id = RatingBeer.objects.values_list('rating_id', flat=True)

    user = list(user)
    beer = list(beer)
    rate = list(rate)
    rating_id = list(rating_id)
    d = {'user' : user, 'beer': beer, 'rate' : rate, 'rating_id' : rating_id}

    df = pd.DataFrame(data=d)
    #reader class using only the rating parameter
    reader= Reader(rating_scale=(1, 5.0))

    #arranging dataframe
    data= Dataset.load_from_df(df[['user', 'beer', 'rate']], reader)
    # First train an SVD algorithm on the movielens dataset.
    #reader = Reader(line_format="user item rating timestamp", sep=',', rating_scale=(1, 5), skip_lines=1)
    #data = Dataset.load_from_file('candi_beer_rating.csv', reader=reader)

    trainset = data.build_full_trainset()
    algo = BaselineOnly()
    algo.train(trainset)

    # Than predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    recommend = {}

    # tap = [90,260,413]
    # tap = [90,260,413,438,742,1001,1244,1756,2219,4113,4442,7609,7742,8352,8778,10951,11575,13108,18919,19502,
    # 20387,21407,21514,26046,27699,28285,35689,64468,68742,75158,149246,161303,193089,226527,226528,226529,226530,226531,226532]

    tap = [90, 742, 1001]

    #총 39개 13108 한개가 겹치는게 있음

    # cadidate 1로 바꾸는 작업중
    # tap = [227000,227001,227002]


    id = request.user.id
    #i = 1  ,   1434
    for beer in tap :
            predictions = algo.predict(id,beer)
            recommend[predictions.iid] = predictions.est

    return sorted(recommend.items(), key=lambda t : t[1], reverse=True)
