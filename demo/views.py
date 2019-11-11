# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
import os


def _get_lang(request):
    return "zh" if "HTTP_ACCEPT_LANGUAGE" in request.META and request.META.get('HTTP_ACCEPT_LANGUAGE').startswith(
        "zh") else "en"


def index(request):
    config = json.loads(open("webplus_python_demo/config.json").read())
    ctx = {
        "_lang": _get_lang(request),
        "siteId": config["site"]["id"],
        "quickstartDocUrl": config["quickstart"]["doc"]["url"],
        "quickstartRepoName": config["quickstart"]["repo"]["name"],
        "quickstartRepoUrl": config["quickstart"]["repo"]["url"],
        "appUrl": config["app"]["url"] % os.environ,
        "envUrl": config["env"]["url"] % os.environ,
        "nextStep": config["next"]["step"]["show"],
        "nextStepPackageUrl": config["next"]["step"]["package"]["url"],
        "consoleUrl": config["webplus"]["console"]["url"],
        "envs": {
            "appRegionId": os.environ["WP_APP_REGION_ID"],
            "appId": os.environ["WP_APP_ID"],
            "appName": os.environ["WP_APP_NAME"],
            "envId": os.environ["WP_ENV_ID"],
            "envName": os.environ["WP_ENV_NAME"],
            "fromCLI": "CLI" == os.environ["WP_CHANGE_TRIGGER_FROM"],
            "fromConsole": 'Console' == os.environ["WP_CHANGE_TRIGGER_FROM"]
        }
    }

    return render(request, "index", ctx)
