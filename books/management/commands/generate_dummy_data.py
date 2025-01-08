from django.core.management.base import BaseCommand
from django.utils import timezone
from books.models import Category, Book, BookLoan
from faker import Faker
import random
from decimal import Decimal
from datetime import timedelta

# Faker를 한국어로 설정
fake = Faker('ko_KR')

class Command(BaseCommand):
    help = '도서관 시스템을 위한 더미 데이터 생성'

    def handle(self, *args, **kwargs):
        self.stdout.write('더미 데이터 생성 중...')

        # 카테고리 생성
        categories = [
            '경영', '소설', '과학', '역사', '예술', '철학',
            '기술', '경제', '자기계발', '여행', '요리'
        ]

        category_objects = []
        for cat_name in categories:
            category = Category.objects.create(
                name=cat_name,
                description=fake.paragraph()  # 한국어 설명 생성
            )
            category_objects.append(category)

        self.stdout.write(f'{len(categories)}개의 카테고리 생성 완료')

        # 도서 생성
        for _ in range(100):  # 100권의 책 생성
            published_date = fake.date_between(start_date='-10y', end_date='today')

            book = Book.objects.create(
                title=fake.catch_phrase(),  # 한국어 제목 생성
                author=fake.name(),  # 한국어 이름 생성
                isbn=fake.unique.random_number(digits=13),
                category=random.choice(category_objects),
                publication_date=published_date,
                price=Decimal(random.uniform(10000, 50000)).quantize(Decimal('0.01')),  # 가격을 원화로 설정
                stock=random.randint(0, 20)
            )

        self.stdout.write('100권의 도서 생성 완료')

        # 대출 기록 생성
        books = Book.objects.all()

        for _ in range(20):  # 2000개의 대출 기록 생성
            book = random.choice(books)
            borrowed_date = fake.date_between(start_date='-1y', end_date='today')
            due_date = borrowed_date + timedelta(days=14)
            status = random.choice(['B', 'R', 'O'])  # B: 대출 중, R: 반납됨, O: 연체

            return_date = None
            if status in ['R', 'O']:
                if status == 'R':
                    return_date = borrowed_date + timedelta(days=random.randint(1, 14))
                else:  # 연체
                    return_date = due_date + timedelta(days=random.randint(1, 30))

            BookLoan.objects.create(
                book=book,
                borrower_name=fake.name(),  # 한국어 이름 생성
                borrowed_date=borrowed_date,
                due_date=due_date,
                return_date=return_date,
                status=status
            )

        self.stdout.write(self.style.SUCCESS('더미 데이터 생성 완료'))