from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Survey, SurveyResponse
from .serializers import SurveySerializer, SurveyResponseSerializer
from .validate import validate_survey_request, validate_survey_response_request

class SurveysView(generics.ListCreateAPIView):
    """
    GET  api/surveys/

    Query Parameters:
        user: int - User ID


    POST api/surveys/

    Parameters:
        survey_name: str - Survey Name
        available_places: int - Maximum number of responses allowed
        user_id: int - User ID
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @validate_survey_request
    def get(self, request, *args, **kwargs):
        # if 'user' query present in url, filter on user_id
        user = request.query_params.get('user', None)
        responses = self.queryset.filter(user_id=user) if user else self.queryset.all()

        return Response(
            data = SurveySerializer(responses, many=True).data,
            status = status.HTTP_200_OK
        )

    @validate_survey_request
    def post(self, request, *args, **kwargs):
        # get parameters
        survey_name = request.data.get('survey_name', None)
        available_places = request.data.get('available_places', None)
        user_id = request.data.get('user_id', None)

        # create survey in database
        survey = Survey.objects.create(
            survey_name = request.data['survey_name'],
            available_places = request.data['available_places'],
            user_id = request.data['user_id']
        )

        return Response (
            data = SurveySerializer(survey).data,
            status = status.HTTP_201_CREATED
        )

class SurveyResponsesView(generics.ListCreateAPIView):
    """
    GET  api/survey-responses/

    Query Parameters:
        survey: int - Survey ID
        user: int - User ID


    POST api/survey-responses/

    Parameters:
        survey_id: int - Survey ID
        user_id: int - User ID
    """
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer

    @validate_survey_response_request
    def get(self, request, *args, **kwargs):
        # if 'survey' query present in url, filter on survey_id
        survey = request.query_params.get('survey', None)
        responses = self.queryset.filter(survey_id=survey) if survey else self.queryset.all()

        # if 'user' query present in url, filter on user_id
        user = request.query_params.get('user', None)
        responses = responses.filter(user_id=user) if user else responses

        return Response(
            data = SurveyResponseSerializer(responses, many=True).data,
            status = status.HTTP_200_OK
        )

    @validate_survey_response_request
    def post(self, request, *args, **kwargs):
        # get parameters
        survey_id = request.data.get('survey_id', None)
        user_id = request.data.get('user_id', None)

        # create response in database
        survey_response = SurveyResponse.objects.create(
            survey_id = request.data['survey_id'],
            user_id = request.data['user_id']
        )

        return Response (
            data = SurveyResponseSerializer(survey_response).data,
            status = status.HTTP_201_CREATED
        )
