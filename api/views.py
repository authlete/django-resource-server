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


from django.conf                                      import settings
from django.views.decorators.csrf                     import csrf_exempt
from django.views.decorators.http                     import require_GET, require_http_methods
from authlete.django.handler.userinfo_request_handler import UserInfoRequestHandler
from .spi.userinfo_request_handler_spi_impl           import UserInfoRequestHandlerSpiImpl
from .time_api                                        import TimeApi


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def userinfo(request):
    """UserInfo Endpoint"""
    return UserInfoRequestHandler(
        settings.AUTHLETE_API, UserInfoRequestHandlerSpiImpl(request)).handle(request)


@require_GET
def time(request):
    """Time API"""
    return TimeApi(settings.AUTHLETE_API).handle(request)
