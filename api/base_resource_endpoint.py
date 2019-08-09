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


from authlete.django.web.access_token_validator import AccessTokenValidator
from authlete.django.web.request_utility        import RequestUtility


class BaseResourceEndpoint(object):
    def __init__(self, api):
        super().__init__()
        self._api = api


    @property
    def api(self):
        return self._api


    def validateAccessToken(self, request, requiredScopes=None, requiredSubject=None):
        """Validate an access token.

        This method extracts an access token from the request and then validates
        the access token.

        Args:
            request (django.http.HttpRequest)
            requiredScopes (list of str):
                Scopes that the access token should have. If this parameter is not
                `None`, the implementation of Authlete's /api/auth/introspection
                API checks whether the access token covers all the required scopes.
                On the other hand, if `None` is given, Authlete does not conduct
                the validation on scopes.
            requiredSubject (str):
                Subject (= unique identifier of an end-user) that the access
                token should be associated with. If this parameter is not `None`,
                the implementation of Authlete's /api/auth/introspection API checks
                whether the access token is associated with the required subject.
                On the other hand, if `None` is given, Authlete does not conduct
                the validation on subject.

        Returns:
            authlete.django.web.AccessTokenValidator
        """

        # Extract an access token from the request.
        accessToken = RequestUtility.extractBearerToken(request)

        # Create a validator to validate the access token.
        validator = AccessTokenValidator(self.api)

        # Validate the access token. As a result of this method call,
        # some properties of 'validator' are set. For example, the
        # 'valid' property holds the validation result.
        validator.validate(accessToken, requiredScopes, requiredSubject)

        # Return the validator that holds the result of the validation.
        return validator
