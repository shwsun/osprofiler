# Copyright 2011 OpenStack Foundation.
# Copyright 2017-2018 Massachusetts Open Cloud.
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



#from tracers.jaeger import *
#from middleware.jaeger import *

import logging
import time
from jaeger_client import Config


def jaeger_tracer(service_name='default-tracer'):
    """Jaeger tracing normal tracer implementation for OpenStack """
    tracer_config = Config(
        config={  # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )

    return tracer_config.initialize_tracer()


def jaeger_middleware(service_name='default-middleware'):
    """Jaeger tracing middleware tracer implementation for OpenStack"""
    middleware_config = Config(
        config={  # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service_name,
        validate=True,
    )

    return middleware_config.initialize_tracer()





"""
    tracer = osprofiler_middleware.Tracer()

    if tracer.extract(Format.HTTP_HEADERS, kwargs['headers']):
            # use tracer.extract to determine if the request is traced
            self._traced = True

        if self._traced:
            headers = kwargs['headers']
            # TODO: extract() -- deal with kwargs headers
            span_ctx = tracer.extract(Format.HTTP_HEADERS, headers)
            new_span = tracer.start_span(
                operation_name='novaclient-session-client',
                child_of(span_ctx))
            # TODO: Tagging?
            #span.set_tag('x', 'y')
            #span.set_baggage_item('a', 'b')
            #span.log_event('z')
            # TODO: inject -- deal with kwargs again
            tracer.inject(new_span, Format.HTTP_HEADERS, headers)
            kwargs['headers'].update(headers)

    if self._traced:
            new_span.finish()


    if api_version.ver_minor != 0:
        # FIXME: can I set headers here?
        kwargs.setdefault('headers', kwargs.get('headers', {}))
        headers = kwargs['headers']
        tracer = osprofiler_tracer.Tracer()  # request is sampled
        # NOTE(jethros): Since there is no way to know when the Client will
        # finish we will have to *defer* the span.finish with *with*
        with tracer.start_span(operation_name="novaclient-client") as span:
            # inject headers
            tracer.inject(span, Format.HTTP_HEADERS, headers)
            kwargs['headers'].update(headers)
            return client_class(api_version=api_version, auth_url=auth_url,
                                direct_use=False, username=username, **kwargs)
    else:
        return client_class(api_version=api_version, auth_url=auth_url,
                            direct_use=False, username=username, **kwargs)
"""
