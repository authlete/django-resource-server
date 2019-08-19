Resource Server Implementation in Python
========================================

Overview
--------

This is a resource server implementation in Python. It supports a
[userinfo endpoint][UserInfoEndpoint] defined in
[OpenID Connect Core 1.0][OIDCCore] and includes an example of a protected
resource endpoint that accepts an access token in the way defined in
[2.1. Authorization Request Header Field][RFC6750_2_1] of [RFC 6750][RFC6750]
(The OAuth 2.0 Authorization Framework: Bearer Token Usage).

This implementation is written using [Django][Django] and
[authlete-python-django][AuthletePythonDjango] library which is an Anthlete's
open-source library for Django.

To validate an access token presented by a client application, this resource
server makes an inquiry to the Authlete server. This means that this resource
server expects that the authorization server which has issued the access token
uses Authlete as a backend service. [django-oauth-server][DjangoOAuthServer]
is such an authorization server implementation and it supports
[OAuth 2.0][RFC6749] and [OpenID Connect][OIDC].

License
-------

  Apache License, Version 2.0

Source Code
-----------

  <code>https://github.com/authlete/django-resource-server</code>

About Authlete
--------------

[Authlete][Authlete] is a cloud service that provides an implementation of
OAuth 2.0 & OpenID Connect ([overview][AuthleteOverview]). You can easily get
the functionalities of OAuth 2.0 and OpenID Connect either by using the default
implementation provided by Authlete or by implementing your own authorization
server using [Authlete Web APIs][AuthleteAPI].

To use this resource server implementation, you need to get API credentials
from Authlete and set them in `authlete.ini`. The steps to get API credentials
are very easy. All you have to do is just to register your account
([sign up][AuthleteSignUp]). See [Getting Started][AuthleteGettingStarted] for
details.

How To Run
----------

1. Install authlete-python and authlete-python-django libraries.

        $ pip install authlete
        $ pip install authlete-django

2. Download the source code of this resource server implementation.

        $ git clone https://github.com/authlete/django-resource-server.git
        $ cd django-resource-server

3. Edit the configuration file to set the API credentials of yours.

        $ vi authlete.ini

4. Create a user account for testing.

        $ python manage.py migrate
        $ python manage.py shell
        >>> from django.contrib.auth.models import User
        >>> user = User()
        >>> user.username = 'john'
        >>> user.first_name = 'John'
        >>> user.last_name = 'Smith'
        >>> user.email = 'john@example.com'
        >>> user.set_password('john')
        >>> user.is_active = True
        >>> user.save()
        >>> quit()

5. Start the resource server on `http://localhost:8001`.

        $ python manage.py runserver 8001

Endpoints
---------

This implementation exposes endpoints as listed in the table below.

| Endpoint          | Path            |
|:------------------|:----------------|
| UserInfo Endpoint | `/api/userinfo` |
| Time Endpoint     | `/api/time`     |

#### UserInfo Endpoint

The userinfo endpoint is an implementation of the requirements described in
[5.3. UserInfo Endpoint][UserInfoEndpoint] of [OpenID Connect Core 1.0][OIDCCore].

The endpoint returns user information in JSON or JWT format, depending on the
configuration of the client application. If both `userinfo_signed_response_alg`
and `userinfo_encrypted_response_alg` of the metadata of the client application
are not specified, user information is returned as a plain JSON. Otherwise, it
is returned as a serialized JWT. Authlete provides you with a Web console
([Developer Console][DeveloperConsole]) to manage metadata of client applications.
As for metadata of client applications, see [2. Client Metadata][OIDCDynReg_Metadata]
of [OpenID Connect Dynamic Client Registration 1.0][OIDCDynReg].

User information returned from the endpoint contains [claims][OIDCCore_Claims]
of the user. In short, _claims_ are pieces of information about the user such
as a given name and an email address. Because Authlete does not manage user
data (although it supports OpenID Connect), you have to provide claim values.
It is achieved by implementing `UserInfoRequestHandlerSpi` interface.

In this resource server implementation, `UserInfoRequestHandlerSpiImpl` is an
example implementation of `UserInfoRequestHandlerSpi` interface and it retrieves
claim values from `django.contrib.auth`.

#### Time Endpoint

The time endpoint implemented in this resource server is just an example of a
protected resource endpoint. Its main purpose is to show how to validate an
access token at a protected resource endpoint.

The path of the time endpoint is `/api/time`. The endpoint accepts an access
token in the way defined in [2.1. Authorization Request Header Field][RFC6750_2_1]
of [RFC 6750][RFC6750].

```
$ ACCESS_TOKEN=YOUR_ACCESS_TOKEN
$ curl -v http://localhost:8001/api/time \
       -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

The time endpoint returns information about the current time (UTC) in JSON
format. The following is an example response.

```
{
  "year":   2019,
  "month":  8,
  "day":    9,
  "hour":   14,
  "minute": 45,
  "second": 2
}
```

As for generic and Authlete-specific information regarding how to protect Web
APIs by OAuth 2.0 access tokens, see [Protected Resource][ProtectedResource].

See Also
--------

- [Authlete][Authlete] - Authlete Home Page
- [authlete-python][AuthletePython] - Authlete Library for Python
- [authlete-python-django][AuthletePythonDjango] - Authlete Library for Django
- [django-oauth-server][DjangoOAuthServer] - Authorization Server Implementation

Contact
-------

Contact Form : https://www.authlete.com/contact/

| Purpose   | Email Address        |
|:----------|:---------------------|
| General   | info@authlete.com    |
| Sales     | sales@authlete.com   |
| PR        | pr@authlete.com      |
| Technical | support@authlete.com |

[Authlete]:               https://www.authlete.com/
[AuthleteAPI]:            https://docs.authlete.com/
[AuthleteGettingStarted]: https://www.authlete.com/developers/getting_started/
[AuthleteOverview]:       https://www.authlete.com/developers/overview/
[AuthletePython]:         https://github.com/authlete/authlete-python/
[AuthletePythonDjango]:   https://github.com/authlete/authlete-python-django/
[AuthleteSignUp]:         https://so.authlete.com/accounts/signup
[DeveloperConsole]:       https://www.authlete.com/developers/cd_console/
[Django]:                 https://www.djangoproject.com/
[DjangoOAuthServer]:      https://github.com/authlete/django-oauth-server/
[OIDC]:                   https://openid.net/connect/
[OIDCCore]:               https://openid.net/specs/openid-connect-core-1_0.html
[OIDCCore_Claims]:        https://openid.net/specs/openid-connect-core-1_0.html#Claims
[OIDCDynReg]:             https://openid.net/specs/openid-connect-registration-1_0.html
[OIDCDynReg_Metadata]:    https://openid.net/specs/openid-connect-registration-1_0.html#
[ProtectedResource]:      https://www.authlete.com/developers/definitive_guide/protected_resource/
[RFC6749]:                https://tools.ietf.org/html/rfc6749
[RFC6750]:                https://tools.ietf.org/html/rfc6750
[RFC6750_2_1]:            https://tools.ietf.org/html/rfc6750#section-2.1
[UserInfoEndpoint]:       https://openid.net/specs/openid-connect-core-1_0.html#UserInfo
