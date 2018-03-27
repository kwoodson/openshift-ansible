#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines
"""
Custom filters for use in openshift_azure role.
"""

import json
import urllib
import urlparse
from dateutil.parser import parse as date_parse
from datetime import datetime, timedelta

from ansible import errors
from collections import Mapping

def openshift_azure_convert_list_to_json(sas_data_list):
    """ Receives a list of stdout sas data objects
        Ex: "{{ sas_urls | openshift_azure_convert_list_to_json }}"
    """
    if not sas_data_list:
        raise errors.AnsibleFilterError("|failed expects sas_data to be set")

    if not isinstance(sas_data_list, list):
        raise errors.AnsibleFilterError("|openshift_azure_convert_list_to_json failed expects to filter on a list object")

    results = []
    for res in sas_data_list:
        results.append(json.loads(res))

    return results


#def openshift_azure_create_sas_url(sas_data):
#    """ Receive a sas data object and create a url with the correct format
#        Ex: "{{ sas_url | openshift_azure_create_sas_url }}"
#
#       {u'accessSas': u'https://md-2tptr3fghtb1.blob.core.windows.net/rrtwhl0vtlz3/abcd?sv=2017-04-17&sr=b&si=4541bd08-d6a4-4acf-be0f-89e232452c48&sig=M%2BLLV6qZaauAAk7qouLv1CiyjWFxGQiChVefTJcq7YI%3D',
#        u'additionalProperties': {u'endTime': u'2018-03-26T17:01:30.7660035+00:00',
#                                  u'name': u'fcf5dcbf-527f-4ca7-893a-e4d3086df4be',
#                                  u'startTime': u'2018-03-26T17:01:30.2660012+00:00',
#                                  u'status': u'Succeeded'}}
#
#    """
#    if not sas_data:
#        raise errors.AnsibleFilterError("|failed expects sas_data to be set")
#
#    if not isinstance(sas_data, list):
#        raise errors.AnsibleFilterError("|openshift_azure_create_sas_url failed expects to filter on a list object")
#
#    # https://docs.microsoft.com/en-us/azure/storage/common/storage-dotnet-shared-access-signature-part-1#examples-of-sas-uris
#    # start time
#    # sig = ''  signature
#    # sr = ''  resource (b = blob, c = container)
#    # sp = ''  permissions (r = read, w = write)
#    # sv = ''  service version
#
#    # found in additional properties
#    # "name": "name",  # not sure where this goes?
#    #sas_additional_params = {"st": "startTime",
#                             #"se": "endTime"}
#
#    results = []
#    for sas in sas_data:
#        url_parts = urlparse.urlparse(sas['accessSas'])
#        qstring = urlparse.parse_qs(url_parts[4])
#
#        qstring['sp'] = ['rl']
#        qstring['sr'] = ['c']
#
#        # start day is today - 1 day
#        timestr = '%Y-%m-%dT00:00:00Z'
#        start_time = date_parse(sas['additionalProperties']['startTime']) - timedelta(days=1)
#        end_time = date_parse(sas['additionalProperties']['endTime']) + timedelta(days=8)
#        qstring['st'] = [start_time.strftime(timestr)]
#        qstring['se'] = [end_time.strftime(timestr)]
#
#        encoded = urllib.urlencode(qstring, doseq=True)
#
#        sas['accessSas'] = urlparse.urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path,
#                                                url_parts.params, encoded, url_parts.fragment))
#
#        results.append(sas)
#    return sas_data


class FilterModule(object):
    """ Custom ansible filter mapping """

    # pylint: disable=no-self-use, too-few-public-methods
    def filters(self):
        """ returns a mapping of filters to methods """
        return {
            #"openshift_azure_create_sas_url": openshift_azure_create_sas_url,
            "openshift_azure_convert_list_to_json": openshift_azure_convert_list_to_json,
        }
