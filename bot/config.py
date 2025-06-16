#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from os import getenv

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """
    HOST = getenv("HOST", "0.0.0.0")
    PORT = getenv("PORT", "8000")
    APP_ID = getenv("MicrosoftAppId", "")
    APP_PASSWORD = getenv("MicrosoftAppPassword", "")
    APP_TYPE = getenv("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = getenv("MicrosoftAppTenantId", "")
    API_URL = getenv("API_URL", "https://chatbot-api-eshfewc7e3agbhbt.centralus-01.azurewebsites.net")
