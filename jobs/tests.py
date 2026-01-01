from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Company, JobPosting, JobAppQuestion, JobAppAnswer, Application
from django.core.files.uploadedfile import SimpleUploadedFile


class ApplicationFlowTests(APITestCase):
    def setUp(self):
        # create applicant user
        self.applicant = User.objects.create_user(username='applicant', password='pass')
        self.applicant.profile.account_type = self.applicant.profile.ACCOUNT_APPLICANT
        self.applicant.profile.save()

        # create company and employer
        self.company = Company.objects.create(name='TestCo')
        self.employer = User.objects.create_user(username='employer', password='pass')
        self.employer.profile.account_type = self.employer.profile.ACCOUNT_EMPLOYER
        self.employer.profile.company = self.company
        self.employer.profile.save()

        # create a job posting
        self.job = JobPosting.objects.create(title='Engineer', company=self.company, location='Remote', description='Desc')

        # add questions: one required, one optional
        self.q1 = JobAppQuestion.objects.create(job=self.job, question_prompt='Why do you want this job?', required=True)
        self.q2 = JobAppQuestion.objects.create(job=self.job, question_prompt='Have you worked in this field before?', required=False)

        self.client = APIClient()

    def test_apply_creates_application_and_answers(self):
        self.client.force_authenticate(user=self.applicant)
        resp = self.client.post(f"/api/job-postings/{self.job.id}/apply/")
        self.assertIn(resp.status_code, (200, 201))
        data = resp.json()
        self.assertIn('application', data)
        app_id = data['application']['id']
        app = Application.objects.get(id=app_id)
        self.assertEqual(app.job, self.job)
        # answers created for both questions
        answers = JobAppAnswer.objects.filter(application=app)
        self.assertEqual(answers.count(), 2)

    def test_submit_requires_answers_and_resume(self):
        # create application via apply
        self.client.force_authenticate(user=self.applicant)
        resp = self.client.post(f"/api/job-postings/{self.job.id}/apply/")
        app_id = resp.json()['application']['id']
        app = Application.objects.get(id=app_id)

        # Attempt to submit with missing required answers -> expect 400 and missing_questions
        resp = self.client.post(f"/api/applications/{app.id}/submit/")
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertIn('missing_questions', data)  # missing required Q1

        # Fill required answer
        ans = JobAppAnswer.objects.get(application=app, question=self.q1)
        ans.answer_value = 'Because I love it'
        ans.save()

        # Try again -> resume missing
        resp = self.client.post(f"/api/applications/{app.id}/submit/")
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Resume', resp.json()['detail'])

        # Attach resume and submit -> success
        resume = SimpleUploadedFile('resume.pdf', b'resume content', content_type='application/pdf')
        app.resume = resume
        app.save()

        resp = self.client.post(f"/api/applications/{app.id}/submit/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'AP')
