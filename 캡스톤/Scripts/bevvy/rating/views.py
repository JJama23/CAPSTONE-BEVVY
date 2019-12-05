#ratig/views.py

from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponse

########################################
from rating.models import RatingBeer
# import requests
# from django.views.decorators.csrf import csrf_exempt #이거는 csrf 안할떄 쓰는거
import json # json을 바꿔줄떄
from rating.recommend import reco
from rating.models import Beer
## 로그인 여부를 통해서 페이지 제한하는거
from django.contrib.auth.mixins import LoginRequiredMixin #로그인 여부 제한하는거
from django.conf import settings # 하하 이거였음 settings 값 가져오는게



import collections

########################################

class MyPageTap(TemplateView):
    template_name = 'mypage_tap.html'
    def get(self, request, *args, **kwargs):
        id = request.user.id
        queryset = RatingBeer.objects.filter(user_id = id)
        queryset2 = queryset.filter(tap = 1)

        test = queryset2.values_list('rate',flat =True).order_by('beer_id') # rating 값
        beer_review = queryset2.values_list('review',flat =True).order_by('beer_id') # Revuew 값

        test2 = queryset2.values_list('beer_id',flat =True).order_by('beer_id')
        mybeerlist = list(test2)

        beerinfo = Beer.objects.filter(pk__in = mybeerlist)

        beername = beerinfo.values_list('beer_name',flat = True).order_by('beer_id')
        beerurl = beerinfo.values_list('url',flat = True).order_by('beer_id')

        # beer_review = beerinfo.values_list('review',flat = True).order_by('beer_id')

        print(request.GET)

        ctx = {
            # 'userlists': queryset,
            'rate' : list(test), #여기서 list로 해줘야지 쿼리셋으로 안나감 #이거 rating 값
            'beername' : list(beername),
            'beerurl' : list(beerurl),
            'beer_review' : list(beer_review),
            'totalbeer' : len(mybeerlist)

            # 'userlists': self.queryset
        }
        return self.render_to_response(ctx)



##  my page
class MyPage(TemplateView):
    template_name = 'mypage_form.html'
    # id = request.user.id
    # queryset = RatingBeer.objects.filter(user_id = 20000)
    # queryset = RatingBeer.objects.all()
    def get(self, request, *args, **kwargs):
        id = request.user.id
        queryset = RatingBeer.objects.filter(user_id = id)
        test = queryset.values_list('rate',flat =True).order_by('beer_id') # rating 값
        beer_review = queryset.values_list('review',flat =True).order_by('beer_id') # Revuew 값

        test2 = queryset.values_list('beer_id',flat =True).order_by('beer_id')
        mybeerlist = list(test2)

        beerinfo = Beer.objects.filter(pk__in = mybeerlist)

        beername = beerinfo.values_list('beer_name',flat = True).order_by('beer_id')
        beerurl = beerinfo.values_list('url',flat = True).order_by('beer_id')

        # beer_review = beerinfo.values_list('review',flat = True).order_by('beer_id')

        print(request.GET)

        ctx = {
            # 'userlists': queryset,
            'rate' : list(test), #여기서 list로 해줘야지 쿼리셋으로 안나감 #이거 rating 값
            'beername' : list(beername),
            'beerurl' : list(beerurl),
            'beer_review' : list(beer_review),
            'totalbeer' : len(mybeerlist)

            # 'userlists': self.queryset
        }
        return self.render_to_response(ctx)


#rating 페이지 완성
class RatingPage(LoginRequiredMixin,TemplateView):
    login_url = settings.LOGIN_URL       # 설정파일의 값으로 설정, 로그인 안된경우 이곳으로 이동
    template_name = 'rating_form.html'
    #rating 한 결과를 전송시켜주는 역할
    def post(self, request):
        select = request.POST['choice']
        ratingdata = json.loads(select) # json으로 묶은 파일을 풀러줌
        # beer = [145,247,433,440,686,973,4792,8107,13108,226538] #맥주 데이터 순서를 미리 지정해줘야한다 rating data와 길이 맞춰줘야함
        beer = [153,362,393,433,671,742,953,973,1645,1756] #맥주 데이터 순서를 미리 지정해줘야한다 rating data와 길이 맞춰줘야함
        id = request.user.id


        if RatingBeer.objects.filter(user_id = id).first() is None: #아직 평가를 안한 회원인 경우
            for i in range(len(ratingdata)):
                if ratingdata[i] == 0:
                    pass
                else:
                    RatingBeer(user_id = id, rate = ratingdata[i], beer_id = beer[i], review = "").save()
        else: #평가를 이미 했고 결과값을 수정하는 경우
            user_table = RatingBeer.objects.filter(user_id = id)
            for i in range(len(ratingdata)):
                if user_table.filter(beer_id = beer[i]).first() is None: # 평가안한 beer_id 값이 엄는 경우에는
                    if ratingdata[i] == 0:
                        pass
                    else:
                        RatingBeer(user_id = id, rate = ratingdata[i],beer_id = beer[i], review = "").save()
                else: #비어아디이 있는경우?
                    if ratingdata[i] == 0:
                        pass
                    else:
                        pickdata = user_table.get(beer_id = beer[i])
                        pickdata.rate = ratingdata[i]
                        pickdata.save()

    #데이터를 미리 전송해주는것, 평가한 사람의 경우 보여주기 위해서 db데이터를 전송

    def get(self, request, *args, **kwargs):
        id = request.user.id
        beerset = Beer.objects.filter(candidate = 2)
        beersets = beerset.values_list('url',flat = True)
        beertitle = beerset.values_list('beer_name',flat = True)

        if RatingBeer.objects.filter(user_id = id).first() is None: #평가한 데이터가 없는경우
            ctx = {
                'test' : [0,0,0,0,0,0,0,0,0,0],
                'test3' : list(beersets),
                'title' : list(beertitle)

            }
            return self.render_to_response(ctx)

        else: #평가한 데이터가 있는 경우
            id = request.user.id
            queryset = RatingBeer.objects.filter(user_id = id)
            test = queryset.values_list('rate',flat =True).order_by('beer_id') #필요한것만 전송하는것 rating_id순으로 하면 한두개씩 하는경우 문제
            print(request.GET)

            #평가를 다 안하고 일부만 한 사람꺼를 처음에 출력해수주는거
            beerids = beerset.values_list('beer_id',flat = True)
            list_beerids = list(beerids)

            befquery = queryset.exclude(tap = 1) ## 추천된 맥주를 평가한 사람을 여기서 걸러줘야한다
            user_beerid = befquery.values_list('beer_id',flat =True).order_by('beer_id') #필요한것만 전송하는것
            list_userbid = list(user_beerid) # 여기서 10개 내에 있는것만
            user_rate = list(test)

            a = []
            #현재 사용자가 평가했던 맥주의 index를 찾아주는거

            # beer = [145,247,433,440,686,973,4792,8107,13108,226538] #위에 있던거 잠시만 가져옴
            beer = [153,362,393,433,671,742,953,973,1645,1756] #위에 있던거 잠시만 가져옴
            for i in list_userbid:
                d = 0
                d = beer.index(i)  #이게 저 리스트수가 안맞아서 그런거 같음
                # d = list_beerids.index(i)  #이게 저 리스트수가 안맞아서 그런거 같음
                a.append(d)

            b = [0,0,0,0,0,0,0,0,0,0]
            #찾은 index 를 통해서 b의 값을 바꿔주는것
            for i in range(len(a)):
                c = a[i]
                b[c] = user_rate[i]

            ctx = {
                'userlists': queryset,
                # 'test' : list(test), #여기서 list로 해줘야지 쿼리셋으로 안나감
                'test' : b,
                'test2' : 2,
                'test3' : list(beersets),
                'title' : list(beertitle)
                # 'userlists': self.queryset
            }
            return self.render_to_response(ctx)


class ResultPage(LoginRequiredMixin,TemplateView):
    login_url = settings.LOGIN_URL       # 설정파일의 값으로 설정, 로그인 안된경우 이곳으로 이동
    template_name = 'result_form.html'

    def post(self, request):
        message = request.POST['message']
        rate = request.POST['rate']
        idofbeer = request.POST['idofbeer']
        id = request.user.id

        user_table = RatingBeer.objects.filter(user_id = id)

        if user_table.filter(beer_id = idofbeer).first() is None:
            RatingBeer(user_id = id, rate = rate, beer_id = idofbeer,review = message, tap = 1).save()
        else:
            pickdata = user_table.get(beer_id = idofbeer)
            pickdata.review = message
            pickdata.rate = rate
            pickdata.beer_id = idofbeer
            pickdata.save()



    # 기본적으로 데이터 보내는것
    def get(self,request) :
        a = reco(request)
        tmp_beer = []
        tmp_rate = []
##############################################################################
        for i in range(0,len(a)) :
            tmp_beer.append(a[i][0])
            b = a[i][1]*25
            tmp_rate.append(int(b))

        idofbeer = []
        beerlist = []
        beerurl = []
        percentage = []
        for i in range(len(tmp_beer)):
            beer = Beer.objects.get(beer_id = int(tmp_beer[i]))
            idofbeer.append(int(tmp_beer[i]))
            beerlist.append(beer.beer_name)
            beerurl.append(beer.url)
            percentage.append(tmp_rate[i])

##############################################################################
#이거 수정하기전꺼 // 지금 텝퍼블릭 1번으로 바꾸는 작업중
        # for i in range(0,3) :
        #     tmp_beer.append(a[i][0])
        #     b = a[i][1]*25
        #     tmp_rate.append(int(b))
        #
        # beer1 = Beer.objects.get(beer_id = int(tmp_beer[0]))
        # beer2 = Beer.objects.get(beer_id = int(tmp_beer[1]))
        # beer3 = Beer.objects.get(beer_id = int(tmp_beer[2]))
        #
        # idofbeer = [int(tmp_beer[0]), int(tmp_beer[1]), int(tmp_beer[2])]
        # beerlist = [beer1.beer_name, beer2.beer_name, beer3.beer_name]
        # beerurl = [beer1.url, beer2.url, beer3.url]
        # percentage = [tmp_rate[0],tmp_rate[1],tmp_rate[2]]
###############################################################################

        ctx = {
            # 'beer1' : beer1,
            # 'beer2' : beer2,
            # 'beer3' : beer3,
            # 'rate1' : tmp_rate[0],
            # 'rate2' : tmp_rate[1],
            # 'rate3' : tmp_rate[2],

            'rating' : [0]*39,
            'height': ["9.8125rem"]*39,
            'addtext': [1]*39,
            'fbtu': [0]*39,
            'finb': [0]*39,
            # 'message' : [,]*39,
            'blurdata' : ['blur(0px)'] +['blur(7px)']*38,


            'percen' : percentage,
            'beerlist' : beerlist,
            'beerurl' : beerurl,
            'idofbeer' : idofbeer
        }

        return self.render_to_response(ctx)

        # return render(request, 'result_form.html',ctx)




## 이쪽을 기반으로 만들기 시작해야함
class checkdata(TemplateView):
    template_name = 'datatest.html'

    def get(self, request, *args, **kwargs):
            id = request.user.id
            queryset = RatingBeer.objects.filter(user_id = id)
            # test = queryset.values_list('rate',flat =True).order_by('beer_id') # rating 값
            # beer_review = queryset.values_list('review',flat =True).order_by('beer_id') # Revuew 값
            test2 = queryset.values_list('beer_id',flat =True).order_by('beer_id')
            mybeerlist = list(test2)
            beerinfo = Beer.objects.filter(pk__in = mybeerlist)
            beername = beerinfo.values_list('style_big',flat = True).order_by('beer_id')
            #beerurl = beerinfo.values_list('url',flat = True).order_by('beer_id')

            # beer_review = beerinfo.values_list('review',flat = True).order_by('beer_id')

            #이걸 통해서 기본적으로 마신 맥주/ 그리고 각 지금까지 마신 맥주 수/비율
            b = list(beername)
            a = set(b) # 이거가 set으로 해서 종류만 딱 알 수 있게해줌
            c = 32 #총 맥주 수 등록된거
            d = round(len(b)/32 *100)
            e = {}

            # 이걸 통해서 스타일이랑 그거 개수를 구할 수 있다
            for i in a:
                k = b.count(i)
                e[i] = k

            #나라
            country2 = beerinfo.values_list('country',flat = True).order_by('beer_id')
            countrylist = list(country2)
            countrycount = collections.Counter(countrylist)

            national = list(countrycount.keys())
            nationalcount = list(countrycount.values())

            national = national[:3]
            nationalratio = nationalcount[:3]
            #생각해보니까 비율은 그냥 전체 내가 마신거에서 특정 국가 개수 로 구하면 되는거잖아 len(b)

            queryset = Beer.objects.filter(country = national[0])
            test = queryset.values_list('country_url',flat =True).order_by('beer_id') #필요한것만 전송하는것 rating_id순으로 하면 한두개씩 하는경우 문제


            ctx = {
                'beername' : len(b),
                'persentage' : d,
                'counter' : e,
                'country' : national


            }
            return self.render_to_response(ctx)
