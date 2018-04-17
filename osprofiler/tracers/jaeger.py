# Copyright 2017-2018 Massachusetts Open Cloud.
# Copyright 2011 OpenStack Foundation.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

""" OpenTracing implementation tracers (use Jaeger tracing) for OpenStack.
"""

import opentracing
from oslo_log import log

from osprofiler import _utils


LOG = log.getLogger(__name__)


def init_tracer(tracer_string, *args, **kwargs):
    """Select tracer based on tracer_string.
    Select tracer based on tracer_string in configuration file
    of OpenStack service.
    """
    for tracer in _utils.itersubclasses(Tracer):
        if tracer_string == tracer.get_name():
            tracer(*args, **kwargs)

    return opentracing.tracer


class Tracer(opentracing.Tracer):
    """Base Tracer class.
    This class is base class for all tracer that can be used to work with
    OpenTracing API.
    """

    def __init__(self):
        super(Tracer, self).__init__()

    @classmethod
    def get_name(cls):
        """Return name of tracer that used to initialize OpenTracing tracer.
        :returns: A string represents name of a compatible OpenTracing tracer.
                  For example, `jaeger`, `lightstep`,...
        """
        raise NotImplementedError("This method has to be overridden.")
