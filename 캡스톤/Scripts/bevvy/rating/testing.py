# 현재 로그인한 아이디랑 일치하는 값이 있는가
#
# 노:
# 그냥 저장 순서대로
#
# 예스:
# 이제 맥주 리스트 아이디를 토대로 해서
# 해당 아이디로 불러온 테이블에
# 있다면
#     update
# 없다면
#     save를 통해서 저장할것


# 준비물
# : 가져온 데이터
# : 맥주 아이디 리스트


select = request.POST['choice']
ratingdata = json.loads(select)
beer = [1,2,3,4,5]
id = request.user.id


if RatingBeer.objects.filter(user_id = id) is None:
    for i in range(len(ratingdata)):
        if ratingdata[i] == 0:
            pass
        else:
            RatingBeer(user_id = id, rate = ratingdata[i], beer_id = beer[i]).save()
else:
    user_table = RatingBeer.object.filter(user_id = id)
    for i in range(len(ratingdata)):
        if user_table.get(beer_id = beer[i]) is None:
            RatingBeer(user_id = id, rate = ratingdata[i],beer_id = beer[i]).save()
        else:
            pickdata = user_table.get(beer_id = beer[i])
            pickdata.rate = ratingdata[i]
            pickdata.save()
return HttpResponse(select)

###########################################################################
###########################################################################
###########################################################################
def polls(request):
    select = request.POST['choice']
    data = json.loads(select)
    id = request.user.id
    # beer_id = [12,13,16]
    test_id = RatingBeer.objects.values_list('beer_id').filter(rate = 2) #이걸 쓴걸로 비교할 수 있을듯 어차피 값을 다다르잖아 조건 넣을 수 있나?
    test_ids = RatingBeer.objects.filter(user_id = 20000)
    abc = test_ids.get(beer_id = 7)
    if test_ids.get(beer_id = 7) is None:
        bbb = 1
    else:
        bbb = 2
    # 이거는 none으로 id 일치하는거 있는지 확인하는거
    # if RatingBeer.objects.filter(user_id = 20000) is None:
    #     aa = 11
    # else:
    #     aa = 22

    # 저장하는거 값 평가한경우 안한경우 나눠서
    # for i in range(len(data)): # 배열길이는 len 함수로 확인
    #     if data[i] == 0:
    #         pass
    #     else:
    #         RatingBeer(user_id = id, rate = data[i], beer_id = beer_id[i]).save()

    # RatingBeer(rating = data[0]).save()

    # 쿼리 불러온거 이런식으로 활용한다 test_ids[1].beer_id
    # get으로 선택한경우 그것의 값 이렇게 abc.rate
    return HttpResponse(bbb)


#########################################################################
# 기초적으로 값만 받는거 여기에 json 기능 추가되면 배열도 받을 수 있는거
#########################################################################
# def polls(request):
#     ratingbeers = RatingBeer.objects.all()
#     select = request.POST['choice']
#     try:
#         RatingBeer = RatingBeer.objects.get(rating = select)
#         RatingBeer.save()
#     except:
#         return HttpResponse(select)
#########################################################################
#########################################################################
# 기본으로 템플릿만 보여주는 클레스 뷰
#########################################################################
# class RatingPage(TemplateView):
#     template_name = 'rating_form.html'
