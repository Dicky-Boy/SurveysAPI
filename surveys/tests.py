from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Survey, SurveyResponse
from .serializers import SurveySerializer, SurveyResponseSerializer

class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_survey(survey_name='', available_places=-1, user_id=0):
        # create survey directly in database
        if survey_name and available_places >= 0 and user_id:
            Survey.objects.create(
                survey_name = survey_name,
                available_places = available_places,
                user_id = user_id)

    @staticmethod
    def create_survey_response(survey_id=-1, user_id=0):
        # create survey response directly in database
        if user_id and survey_id >= 0:
            SurveyResponse.objects.create(
                survey_id = survey_id,
                user_id = user_id)

    def setUp(self):
        # add test data
        self.create_survey(
            survey_name='Survey 1',
            available_places=30,
            user_id=1)
        self.create_survey(
            survey_name='Survey 2',
            available_places=1,
            user_id=1)
        self.create_survey(
            survey_name='Survey 3',
            available_places=10,
            user_id=2)

        self.create_survey_response(
            survey_id=1,
            user_id=1)
        self.create_survey_response(
            survey_id=1,
            user_id=2)
        self.create_survey_response(
            survey_id=2,
            user_id=2)

class ListSurveysTest(BaseTest):
    def test_list_all_surveys(self):
        """
        Test all surveys added in the setUp method are listed when
        making a GET request to the /api/surveys/ endpoint
        """
        # make API request
        response = self.client.get(reverse('surveys'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # fetch the data from database
        expected = Survey.objects.all()
        serialized = SurveySerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)

    def test_list_all_surveys_for_user(self):
        """
        Test all surveys for a given user added in the setUp method
        are listed when making a GET request to the /api/surveys/
        endpoint with the ?user query parameter
        """
        # make API request
        test_user = 1
        response = self.client.get(reverse('surveys'), {'user': test_user})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # fetch the data from database
        expected = Survey.objects.filter(user_id=test_user)
        serialized = SurveySerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)

    def test_list_all_surveys_for_invalid_user(self):
        """
        Test correct response received when making a GET request to the
        /api/surveys/ endpoint with a non-integer ?user query
        parameter
        """
        # make API request
        test_user = 'a'
        response = self.client.get(reverse('surveys'), {'user': test_user})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ListSurveyResponsesTest(BaseTest):
    def test_list_all_survey_responses_for_survey(self):
        """
        Test all responses for a given survey added in setUp method are
        listed when making a GET request to the /api/survey-responses/
        endpoint with the ?survey query parameter
        """
        # make API request
        test_survey = 1
        response = self.client.get(reverse('survey-responses'), {'survey': test_survey})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # fetch the data from database
        expected = SurveyResponse.objects.filter(survey_id=test_survey)
        serialized = SurveyResponseSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)

    def test_list_all_survey_responses_for_invalid_survey(self):
        """
        Test correct response received when making a GET request to the
        /api/survey-responses/ endpoint with a non-integer ?survey query
        parameter
        """
        # make API request
        test_survey = 'a'
        response = self.client.get(reverse('survey-responses'), {'survey': test_survey})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_survey_responses_for_survey_not_found(self):
        """
        Test correct response received when making a GET request to the
        /api/survey-responses/ endpoint with a non-existing ?survey query
        parameter
        """
        # make API request
        test_survey = 4
        response = self.client.get(reverse('survey-responses'), {'survey': test_survey})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_survey_responses_for_user(self):
        """
        Test all responses for a given user added in setUp method are
        listed when making a GET request to the /api/survey-responses/
        endpoint with the ?user query parameter
        """
        # make API request
        test_user = 2
        response = self.client.get(reverse('survey-responses'), {'user': test_user})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # fetch the data from database
        expected = SurveyResponse.objects.filter(user_id=test_user)
        serialized = SurveyResponseSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)

    def test_list_all_survey_responses_for_invalid_user(self):
        """
        Test correct response received when making a GET request to the
        /api/survey-responses/ endpoint with a non-integer ?user query
        parameter
        """
        # make API request
        test_user = 'a'
        response = self.client.get(reverse('survey-responses'), {'user': test_user})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateSurveyTest(BaseTest):
    def test_create_survey(self):
        """
        Test creation of new survey via POST request to
        /api/surveys/ endpoint
        """
        # make API request
        response = self.client.post(reverse('surveys'),
                        {'survey_name': 'Test Survey',
                        'available_places': 100,
                        'user_id': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # fetch data from database
        expected = Survey.objects.get(survey_name='Test Survey')
        serialized = SurveySerializer(expected)
        self.assertEqual(response.data, serialized.data)

    def test_create_survey_invalid_params(self):
        """
        Test correct response received when attempting to create a
        new survey with invalid POST request data
        """
        # make API request
        response = self.client.post(reverse('surveys'),
                        {'survey_name': 'Test Survey',
                        'available_places': 'thirty',
                        'user_id': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survey_missing_params(self):
        """
        Test correct response received when attempting to create a
        new survey with invalid POST request data
        """
        # make API request
        response = self.client.post(reverse('surveys'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreateSurveyResponseTest(BaseTest):
    def test_create_survey_response(self):
        """
        Test creation of new survey response via POST request to
        /api/survey-responses/ endpoint
        """
        # make API request
        test_survey = 3
        test_user = 3
        response = self.client.post(reverse('survey-responses'),
                        {'survey_id': test_survey,
                        'user_id': test_user})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # fetch data from database
        expected = SurveyResponse.objects.get(survey_id=test_survey)
        serialized = SurveyResponseSerializer(expected)
        self.assertEqual(response.data, serialized.data)

    def test_create_survey_response_for_full_survey(self):
        """
        Test that survey response cannot be created when specified
        survey has all available places filled
        """
        #make API request
        test_survey = 2
        test_user = 3
        response = self.client.post(reverse('survey-responses'),
                        {'survey_id': test_survey,
                        'user_id': test_user})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_survey_response_invalid_params(self):
        """
        Test correct response received when attempting to create a
        new survey response with invalid POST request data
        """
        # make API request
        test_user = 3
        response = self.client.post(reverse('survey-responses'),
                        {'survey_id': 'two',
                        'user_id': test_user})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_survey_response_missing_params(self):
        """
        Test correct response received when attempting to create a
        new survey response with missing POST request data
        """
        # make API request
        response = self.client.post(reverse('survey-responses'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
