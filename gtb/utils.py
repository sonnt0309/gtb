from rest_framework.response import Response
from django.http import JsonResponse
from . import constant
from rest_framework import status
from django.utils import translation
from datetime import timezone

class Helper():
    # Method format response
    def ResponseFormat(statusCode, message, responseData):
        if message != constant.STR_BLANK:
            responseData['message'] = message

        return Response(responseData, status = statusCode)

    def JsonResponseFormat403(url, serviceName):
        return Response({
            "error": {
                "url": str(url),
                "infos": [
                    {
                        "service": serviceName,
                        "reason": translation.ugettext("Request includes Wrong content."),
                        "detail": translation.ugettext("Invalid format: ") + ("\"Not permission\"")
                    }
                ],
                "message": translation.ugettext("Authentication credentials were not provided.")
            }
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Method format response for function base
    def JsonResponseFormat400(url, serviceName, errors):
        responseData = {
            'error' : {
                'url' : str(url),
                'infos' : [],
                'message' : translation.ugettext('The app throw bad request.')
            }
        }

        print(errors)
        for key in errors:
            print(errors[key])
            if isinstance(errors[key] , dict) is True:
                object2 = errors[key]
                for key2 in object2:
                    lsErr = object2[key2]
                    for err in lsErr:
                        rs_err = {
                            'service' : serviceName,
                            'reason' : translation.ugettext(err.code) if err.code == 'required' else translation.ugettext(constant.INVALID_FORMAT_CODE),
                            'detail' : translation.ugettext('Required key: ') + '"' + key + '"."' + key2 + '"'if err.code == 'required' else translation.ugettext('Invalid format: ') + '"' + key + '"."' + key2 + '" '+ translation.ugettext(str(err))
                        }
                        responseData['error']['infos'].append(rs_err)
            else:
                lsErr = errors[key]
                for err in lsErr:
                    rs_err = {
                        'service' : serviceName,
                        'reason' : translation.ugettext(err.code) if err.code == 'required' else translation.ugettext(constant.INVALID_FORMAT_CODE),
                        'detail' : translation.ugettext('Required key: ') + '"' + key +'"' if err.code == 'required' else translation.ugettext('Invalid format: ') + '"' + key + '" '+ translation.ugettext(str(err))
                    }
                    responseData['error']['infos'].append(rs_err)

        return JsonResponse(responseData, status = status.HTTP_400_BAD_REQUEST)

    # POST以外のメソッド使用
    def JsonResponseFormat405(url, serviceName):
        responseData = { 
            "error": {
                "url": str(url),
                "infos": [
                    {
                        "service": serviceName,
                        "reason": translation.ugettext("Request used illegal method."),
                        "detail": translation.ugettext("Please use legal method.")
                    }
                ],
                "message": translation.ugettext("The app used illegal request method.")
            }
        }
        return JsonResponse(responseData, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def JsonResponseFormat(statusCode, message, responseData):
        if message != constant.STR_BLANK:
            responseData['message'] = message

        return JsonResponse(responseData, status = statusCode)

class Utils():
    def datetimeTOTimestamp(date_time):
        if not date_time is None:
            return int(date_time.replace(tzinfo=timezone.utc).timestamp())
        else:
            return 0