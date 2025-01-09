from django.db import models

# Create your models here.
class ExcelCustomer(models.Model):
    # 커스터머 아이디
    company = models.CharField(max_length=50) # 회사 이름
    department = models.CharField(max_length=32)  # 업종
    company_size = models.CharField(max_length=10)  # 회사 규모
    region = models.CharField(max_length=64)   # 지역
    sign_up_date = models.DateField() # 가입 날짜
    recent_purchase_date = models.DateField # 최근 서비스 이용 날짜
    purchase_num = models.IntegerField()  # 구매 횟수
    total_car_price = models.IntegerField() # 총 거래 금액
    churn = models.IntegerField()     # 이탈 여부
    car_model = models.CharField(max_length=32) # 차량 모델 명
    car_price = models.IntegerField()         # 차량 구매 가격
    purchase_date = models.DateField      # 구매 일자
    score = models.IntegerField()   # 리뷰 점수
    mean_score = models.FloatField()      # 리뷰 평균 평점


    class Meta:
        db_table = "excel_customer"