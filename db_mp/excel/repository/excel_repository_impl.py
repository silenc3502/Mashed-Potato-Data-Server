from excel.entity.excel_customer import ExcelCustomer
from excel.repository.excel_repository import ExcelRepository


class ExcelRepositoryImpl(ExcelRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createMany(self, excelDictionary):
        customerDictionary = [
            ExcelCustomer(
                company=excelElement['회사명'],
                department=excelElement['업종'],
                company_size=excelElement['회사 규모'],
                region=excelElement['지역'],
                sign_up_date=excelElement['가입 일자'],
                recent_purchase_date=excelElement['최근 서비스 이용 날짜'],
                purchase_num=excelElement['구매 횟수'],
                total_car_price=excelElement['총 거래 금액'],
                churn=excelElement['이탈 여부'],
                car_model=excelElement['모델명'],   # 차량 모델 명
                car_price=excelElement['구매 가격'],     # 차량 구매 가격
                purchase_date=excelElement['구매 일자'],
                score=excelElement['평점'],            #리뷰 점수
                mean_score = excelElement['평균 평점'],  # 리뷰 평균 평점
            )
            for excelElement in excelDictionary
        ]

        ExcelCustomer.objects.bulk_create(customerDictionary)

    def list(self):
        return ExcelCustomer.objects.all()


  