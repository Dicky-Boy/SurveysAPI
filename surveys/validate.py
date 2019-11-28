from rest_framework.response import Response
from rest_framework.views import status
from .models import Survey, SurveyResponse

def is_int_param_invalid(param, name):
    if not param.isdigit():
        return Response (
            data = {
                'message': name + 'parameter must be an integer'
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return None

def is_survey_id_invalid(survey_id):
    # check survey_id is an integer
    invalid_int = is_int_param_invalid(survey_id, 'survey_id')
    if invalid_int:
        return invalid_int
    # check survey_id corresponds to an existing survey
    try:
        Survey.objects.get(pk=survey_id)
    except:
        return Response (
            data = {
                'message': 'Survey with id {} does not exist'.format(survey_id)
            },
            status = status.HTTP_404_NOT_FOUND
        )

def validate_survey_request(fn):
    def decorated(*args, **kwargs):
        head = args[0]
        request = args[1]
        user_id = None

        if head.request.method == 'POST':
            # check all required data provided
            survey_name = request.data.get('survey_name', None)
            available_places = request.data.get('available_places', None)
            user_id = request.data.get('user_id', None)
            if not (survey_name and available_places and user_id):
                return Response (
                    data = {
                        'message': 'survey_name, available_places, and user_id required to create a new survey'
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            # validate available_places
            if available_places:
                invalid_available_places_response = is_int_param_invalid(available_places, 'available_places')
                if invalid_available_places_response:
                    return invalid_available_places_response

        elif head.request.method == 'GET':
            user_id = request.query_params.get('user', None)

        # validate user_id
        if user_id:
            invalid_user_response = is_int_param_invalid(user_id, 'user_id')
            if invalid_user_response:
                return invalid_user_response

        return fn(*args, **kwargs)
    return decorated

def validate_survey_response_request(fn):
    def decorated(*args, **kwargs):
        head = args[0]
        request = args[1]
        user_id = None
        survey_id = None

        if head.request.method == 'POST':
            # check all required data provided
            survey_id = request.data.get('survey_id', None)
            user_id = request.data.get('user_id', None)
            if not (survey_id and user_id):
                return Response (
                    data = {
                        'message': 'survey_id and user_id required to create a new survey response'
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            # validate survey_id
            if survey_id:
                invalid_survey_response = is_survey_id_invalid(survey_id)
                if invalid_survey_response:
                    return invalid_survey_response

            # check survey isn't already full
            response_count = SurveyResponse.objects.filter(survey_id=survey_id).count()
            if response_count >= Survey.objects.get(pk=survey_id).available_places:
                return Response (
                    data = {
                        'message': 'Survey id {} has already received its maximum number of responses'.format(survey_id)
                    },
                    status = status.HTTP_403_FORBIDDEN
                )

        elif head.request.method == 'GET':
            user_id = request.query_params.get('user', None)
            survey_id = request.query_params.get('survey', None)

            # validate survey_id
            if survey_id:
                invalid_survey_response = is_survey_id_invalid(survey_id)
                if invalid_survey_response:
                    return invalid_survey_response

        # validate user_id
        if user_id:
            invalid_user_response = is_int_param_invalid(user_id, 'user_id')
            if invalid_user_response:
                return invalid_user_response



        return fn(*args, **kwargs)
    return decorated
