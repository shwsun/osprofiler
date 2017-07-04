# Copyright 2014 Fujitsu Ltd.
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

import opentracing
from osprofiler.tracers import base


class Jaeger(base.Tracer):

    def __init__(self, *args, **kwargs):
        super(Jaeger, self).__init__()

        try:
            import jaeger_client
        except ImportError:
            raise ImportError(
                "To use OSprofiler with Uber Jaeger tracer, "
                "you have to install `jaeger-client` manually. "
                "Install with pip:\n `pip install jaeger-client`."
            )

        # Initialize tracer for each profiler
        jaeger_client.Config._initialized = False
        config = jaeger_client.Config(
            # NOTE(tovin07): This config should be loaded from yaml file
            config={
                "sampler": {
                    "type": "const",
                    "param": 1
                },
                "logging": True
            },
            service_name="{}-{}".format(
                kwargs.get("project"),
                kwargs.get("service")
            )
        )
        config.initialize_tracer()
    @classmethod
    def get_name(cls):
        return "jaeger"
