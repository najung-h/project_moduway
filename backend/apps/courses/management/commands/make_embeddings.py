import os
import requests
import json
from django.core.management.base import BaseCommand
from apps.courses.models import Course

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. 환경 변수 및 설정
        GMS_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/embeddings"
        GMS_KEY = os.environ.get("GMS_KEY")
        
        if not GMS_KEY:
            self.stdout.write(self.style.ERROR("GMS_KEY가 설정되지 않았습니다."))
            return

        # 2. 임베딩이 필요한 강의
        courses = Course.objects.filter(embedding__isnull=True)
        
        if not courses.exists():
            self.stdout.write(self.style.SUCCESS("임베딩할 새로운 데이터가 없습니다."))
            return

        self.stdout.write(f"총 {courses.count()}명의 유저 임베딩을 시작합니다.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GMS_KEY}"
        }

        for course in courses:
            try:
                # 3. 데이터 결합 (제목 + 대분류 + 중분류 + 요약)
                raw_text = f"강의명: {course.name or ''}, 대분류: {course.classfy_name or ''}, 중분류: {course.middle_classfy_name or ''}, 상세정보: {course.summary or ''}"
                combined_text = raw_text.replace('\n', ' ').replace('\r', ' ').strip()
                if not combined_text:
                    continue

                # 4. GMS 호출
                data = {
                    "model": "text-embedding-3-small",
                    "input": combined_text
                }
                
                response = requests.post(GMS_URL, headers=headers, data=json.dumps(data))
                
                if response.status_code == 200:
                    result = response.json()
                    embedding_vector = result['data'][0]['embedding']
                    
                    # 5. DB 저장 (pgvector 필드에 리스트 형태로 저장)
                    course.embedding = embedding_vector
                    course.save()
                    self.stdout.write(self.style.SUCCESS(f"성공: Course {course.id}"))
                else:
                    self.stdout.write(self.style.ERROR(f"실패: Course {course.id} (Status: {response.status_code})"))
                    self.stdout.write(response.text)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"에러 발생 (Course {course.id}): {e}"))

        self.stdout.write(self.style.SUCCESS("모든 작업이 완료되었습니다."))