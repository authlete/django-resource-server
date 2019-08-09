#
# Copyright (C) 2019 Authlete, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.


from datetime import datetime
from authlete.django.web.response_utility import ResponseUtility
from .base_resource_endpoint              import BaseResourceEndpoint


class TimeApi(BaseResourceEndpoint):
    def __init__(self, api):
        super().__init__(api)


    def handle(self, request):
        # Extract an access token from the request and validate it.
        # The instance of AccessTokenValidator returned from
        # validateAccessToken() method holds the result of the
        # access token validation.
        #
        # Note that validateAccessToken() can optionally take
        # 'requiredScopes' and 'requiredSubject' parameters
        # although they are not used in this example.
        validator = self.validateAccessToken(request)

        # If the access token is not valid.
        if validator.valid == False:
            # When 'valid' holds False, 'errorResponse' holds an error response
            # that should be returned to the client application. The response
            # complies with RFC 6750 (The OAuth 2.0 Authorization Framework:
            # Bearer Token Usage).
            #
            # You can refer to 'introspectionResponse' or 'introspectionException'
            # for more information.
            return validator.errorResponse

        # The access token is valid, so it's okay for this protected resource
        # endpoint to return the requested protected resource.

        # Generate a response specific to this protected resource endpoint
        # and return it to the client.
        return self.__buildResponse()


    def __buildResponse(self):
        # This simple example generates JSON that holds information about
        # the current time.

        # The current time in UTC.
        current = datetime.utcnow()

        # Build JSON manually.
        lines = [
            '{',
            '  "year":   {},'.format(current.year),
            '  "month":  {},'.format(current.month),
            '  "day":    {},'.format(current.day),
            '  "hour":   {},'.format(current.hour),
            '  "minute": {},'.format(current.minute),
            '  "second": {}' .format(current.second),
            '}'
        ]

        content = '\n'.join(lines) + '\n'

        # "200 OK", "application/json;charset=UTF-8"
        return ResponseUtility.okJson(content);
