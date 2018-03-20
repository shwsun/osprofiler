# Copyright 2017-2018 Massachusetts Open Cloud.
# Copyright 2014 Mirantis Inc.
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

import collections
import datetime
import functools
import inspect
import logging
import socket
import threading

from jaeger_client import Config

from oslo_utils import reflection, uuidutils
from osprofiler import notifier
from osprofiler.raw_profiler import (Trace, TraceMeta, _clean,
                                     _ensure_no_multiple_traced, _Profiler,
                                     trace_cls)

# NOTE(boris-42): Thread safe storage for profiler instances.
__local_ctx = threading.local()


def init_tracer(service):
    # NOTE(jethros): I don't think the logging is working
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={  # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


# NOTE(jethros):
def init(hmac_key,
         base_id=None,
         parent_id=None,
         connection_str=None,
         project=None,
         service=None):
    """Init profiler instance for current thread.

    You should call profiler.init() before using osprofiler.
    Otherwise profiler.start() and profiler.stop() methods won't do anything.

    :param hmac_key: secret key to sign trace information.
    :param base_id: Used to bind all related traces.
    :param parent_id: Used to build tree of traces.
    :param connection_str: Connection string to the backend to use for
                           notifications.
    :param project: Project name that is under profiling
    :param service: Service name that is under profiling
    :returns: Profiler instance
    """
    __local_ctx.profiler = _Profiler(
        hmac_key,
        base_id=base_id,
        parent_id=parent_id,
        connection_str=connection_str,
        project=project,
        service=service)
    return __local_ctx.profiler


# XXX(jethros): OSProfiler use get() to determine if tracing is turned on, for
# our framework we will always initialize a tracer
def get():
    """Get profiler instance.

    :returns: Profiler instance or None if profiler wasn't inited.
    """
    return getattr(__local_ctx, "profiler", None)


# XXX(jethros): span.start
def start(name, info=None):
    """Send new start notification if profiler instance is presented.

    :param name: The name of action. E.g. wsgi, rpc, db, etc..
    :param info: Dictionary with extra trace information. For example in wsgi
                  it can be url, in rpc - message or in db sql - request.
    """
    # profiler = get()
    # if profiler:
    #     profiler.start(name, info=info)
    tracer = init_tracer(name + info)
    span = tracer.start_span('say-hello')
    span.finish()


# XXX(jethros): span.stop
def stop(info=None):
    """Send new stop notification if profiler instance is presented."""
    # profiler = get()
    # if profiler:
    #     profiler.stop(info=info)
    pass


# XXX(jethros): Trace decorator, need to implement another version based on our
# framework, see dec_hello
#def trace(name, info=None, hide_args=False, allow_multiple_trace=True):


def trace_notworking(name,
                     info=None,
                     hide_args=True,
                     allow_multiple_trace=True):
    """ Trace decorator for bu framework
    """
    if not info:
        info = {}
    else:
        info = info.copy()

    info["function"] = {}

    def decorator(f):
        trace_times = getattr(f, "__traced__", 0)
        if not allow_multiple_trace and trace_times:
            raise ValueError("Function '%s' has already"
                             " been traced %s times" % (f, trace_times))

        try:
            f.__traced__ = trace_times + 1
        except AttributeError:
            # Tries to work around the following:
            #
            # AttributeError: 'instancemethod' object has no
            # attribute '__traced__'
            try:
                f.im_func.__traced__ = trace_times + 1
            except AttributeError:  # nosec
                pass

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if "name" not in info["function"]:
                # Get this once (as it should **not** be changing in
                # subsequent calls).
                info["function"]["name"] = reflection.get_callable_name(f)

            if not hide_args:
                info["function"]["args"] = str(args)
                info["function"]["kwargs"] = str(kwargs)

            #with Trace(name, info=info):
            #    return f(*args, **kwargs)

            tracer = init_tracer(name + info)
            with tracer.start_span('xxx') as span:
                return f(*args, **kwargs)

        return wrapper

    return decorator


# NOTE(jethros): Need to be implemented using span context
#class _Profiler(object):
# NOTE(jethros): the thread-local profiler instance
