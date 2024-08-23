from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import numpy as np
from core.models import Student
from core.serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def percentile(self, request):
        students = self.get_queryset().order_by('grade')
        if students.count() is 0:
            return Response({})
        
        grades = list(students.values_list('grade',  flat=True))

        p95 = np.percentile(grades, 95)
        p98 = np.percentile(grades, 98)

        p95_below_or_equal = [s.name for s in students if s.grade <= p95]
        p95_above = [s.name for s in students if s.grade > p95]

        p98_below_or_equal = [s.name for s in students if s.grade <= p98]
        p98_above = [s.name for s in students if s.grade > p98]

        total_student = students.count()
        average_grade = np.mean(grades)
        highest_grade = max(grades)
        lowest_grade = min(grades)

        grade_distribution = {
            'A': students.filter(grade__gte=90).count(),
            'B': students.filter(grade__gte=80, grade__lt=90).count(),
            'C': students.filter(grade__gte=70, grade__lt=80).count(),
            'D': students.filter(grade__lt=69).count(),
        }

        result = {
            "percentiles": {
                "p95": {
                    "value": p95,
                    "description": "95% of the students have grades below or equal to this value.",
                    "students_above": p95_above,
                    "students_below_or_equal": p95_below_or_equal
                },
                "p98": {
                    "value": p98,
                    "description": "98% of the students have grades below or equal to this value.",
                    "students_above": p98_above,
                    "students_below_or_equal": p98_below_or_equal
                }
            },
            "summary": {
                "total_students": total_student,
                "grade_distribution": grade_distribution,
                "grade_distribution_desc": {
                    'A': 'This category have grades greater than or equal 90',
                    'B': 'This category have grades between 89 and 80',
                    'C': 'This category have grades between 79 and 70',
                    'D': 'This category have grades less than 70',
                },
                "average_grade": average_grade,
                "highest_grade": highest_grade,
                "lowest_grade": lowest_grade
            }
        }

        return Response(result)


# class PresentilesViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
