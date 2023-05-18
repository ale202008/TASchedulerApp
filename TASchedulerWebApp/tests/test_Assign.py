from django.test import TestCase
from TASchedulerWebApp.models import Course, User

class CourseAssignmentTest(TestCase):
    def setUp(self):
        # Create test data
        self.instructor1 = User.objects.create_user(email='instructor1@test.com', password='test1234')
        self.instructor2 = User.objects.create_user(email='instructor2@test.com', password='test1234')
        self.ta1 = User.objects.create_user(email='ta1@test.com', password='test1234')
        self.ta2 = User.objects.create_user(email='ta2@test.com', password='test1234')
        self.course1 = Course.objects.create(id='TEST100', name='Test Course 1')
        self.course2 = Course.objects.create(id='TEST101', name='Test Course 2')

    def test_reassign_instructor_to_course(self):
        # Assign an instructor to the course
        self.course1.Instructor = self.instructor1
        self.course1.save()

        # Reassign a different instructor to the course
        self.course1.Instructor = self.instructor2
        self.course1.save()

        # Check the assignment
        self.assertEqual(self.course1.Instructor, self.instructor2)

    def test_reassign_ta_to_course(self):
        # Assign a TA to the course
        self.course1.TeacherAssistant = self.ta1
        self.course1.save()

        # Reassign a different TA to the course
        self.course1.TeacherAssistant = self.ta2
        self.course1.save()

        # Check the assignment
        self.assertEqual(self.course1.TeacherAssistant, self.ta2)

    def test_remove_instructor_from_course(self):
        # Assign an instructor to the course
        self.course1.Instructor = self.instructor1
        self.course1.save()

        # Remove the instructor from the course
        self.course1.Instructor = None
        self.course1.save()

        # Check the assignment
        self.assertIsNone(self.course1.Instructor)

    def test_remove_ta_from_course(self):
        # Assign a TA to the course
        self.course1.TeacherAssistant = self.ta1
        self.course1.save()

        # Remove the TA from the course
        self.course1.TeacherAssistant = None
        self.course1.save()

        # Check the assignment
        self.assertIsNone(self.course1.TeacherAssistant)

    def test_assign_instructor_to_multiple_courses(self):
        # Assign an instructor to two courses
        self.course1.Instructor = self.instructor1
        self.course1.save()
        self.course2.Instructor = self.instructor1
        self.course2.save()

        # Check the assignments
        self.assertEqual(self.course1.Instructor, self.instructor1)
        self.assertEqual(self.course2.Instructor, self.instructor1)

    def test_assign_ta_to_multiple_courses(self):
        # Assign a TA to two courses
        self.course1.TeacherAssistant = self.ta1
        self.course1.save()
        self.course2.TeacherAssistant = self.ta1
        self.course2.save()

        # Check the assignments
        self.assertEqual(self.course1.TeacherAssistant, self.ta1)
        self.assertEqual(self.course2.TeacherAssistant, self.ta1)
