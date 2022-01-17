#Requests 패키지 사용
import requests_json

r = requests_json.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
rjson = r.json()

print(rjson)

gus = rjson['RealtimeCityAir']['row']

for gu in gus:
    gu_name = gu['MSRSTE_NM']
    gu_mise = gu['IDEX_MVL']
    if(gu_mise>100):
        print(gu_name, ':', gu_mise)

