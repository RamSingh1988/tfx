# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example of a Hello World TFX custom component.

This custom component simply reads tf.Examples from input and passes through as
output.  This is meant to serve as a kind of starting point example for creating
custom components.

This component along with other custom component related code will only serve as
an example and will not be supported by TFX team.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from hello_world.hello_component import executor
from tfx import types
from tfx.components.base import base_component
from tfx.components.base import executor_spec
from tfx.types import channel_utils
from tfx.types import standard_artifacts
from tfx.types.component_spec import ChannelParameter
from tfx.types.component_spec import ExecutionParameter
from typing import Optional, Text


class HelloComponentSpec(types.ComponentSpec):
  """ComponentSpec for Custom TFX Hello World Component."""

  PARAMETERS = {
      # These are parameters that will be passed in the call to
      # create an instance of this component.
      'name': ExecutionParameter(type=Text),
  }
  INPUTS = {
      # This will be a dictionary with input artifacts, including URIs
      'input_data': ChannelParameter(type=standard_artifacts.Examples),
  }
  OUTPUTS = {
      # This will be a dictionary which this component will populate
      'output_data': ChannelParameter(type=standard_artifacts.Examples),
  }


class HelloComponent(base_component.BaseComponent):
  """Custom TFX Hello World Component.

  This custom component class consists of only a constructor.
  """

  SPEC_CLASS = HelloComponentSpec
  EXECUTOR_SPEC = executor_spec.ExecutorClassSpec(executor.Executor)

  def __init__(self,
               input_data: types.Channel = None,
               output_data: types.Channel = None,
               name: Optional[Text] = None):
    """Construct a HelloComponent.

    Args:
      input_data: A Channel of 'ExamplesPath' type. This will often contain
        two splits, 'train', and 'eval'.
      output_data: A Channel of 'ExamplesPath' type. This will usually contain
        the same splits as input_data.
      name: Optional unique name. Necessary if multiple Hello components are
        declared in the same pipeline.
    """
    output_data = output_data or channel_utils.as_channel([
        standard_artifacts.Examples(split=split_name)
        for split_name in ['train', 'eval']
    ])

    spec = HelloComponentSpec(input_data=input_data,
                              output_data=output_data, name=name)
    super(HelloComponent, self).__init__(spec=spec)