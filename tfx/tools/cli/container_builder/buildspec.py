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
"""BuildSpec helper."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import click
from typing import Text
import yaml

from tfx.tools.cli.container_builder import commons


class BuildSpec(object):
  """Build specification.

  BuildSpec generates a default build spec if it does not exist.

  Attributes:
    filename: build spec filename.
    build_context: build working directory.
    target_image: target image path.
    _buildspec: in-memory representation of the build spec.
  """

  def __init__(self,
               filename: Text = commons.BUILD_SPEC_FILENAME,
               target_image: Text = None,
               build_context: Text = commons.BUILD_CONTEXT,
               dockerfile_name: Text = commons.DOCKERFILE_NAME):
    self.filename = filename
    self.build_context = build_context
    self.target_image = target_image
    if os.path.exists(self.filename):
      self._read_existing_build_spec()
      return
    if target_image is None:
      raise ValueError('BuildSpec: target_image is not given and there is no '
                       'existing build spec file.')
    self._generate_default(dockerfile_name)

  def _read_existing_build_spec(self):
    """Read existing build spec yaml."""
    with open(self.filename, 'r') as f:
      click.echo('Reading build spec from %s' % self.filename)
      if self.target_image is not None:
        click.echo(
            'Target image %s is not used. If the build spec is'
            'provicded, update the target image in the build spec'
            'file %s.' % self.target_image, self.filename)
      self._buildspec = yaml.safe_load(f)
      if len(self._buildspec['build']['artifacts']) != 1:
        raise RuntimeError('The build spec contains multiple artifacts however'
                           'only one is supported.')
      self.build_context = self._buildspec['build']['artifacts'][0]['workspace']

  def _generate_default(self, dockerfile_name: Text):
    """Generate a default build spec yaml.

    Args:
      dockerfile_name: dockerfile name.
    """
    self._buildspec = {
        'apiVersion': commons.SKAFFOLD_API_VERSION,
        'kind': 'Config',
        'build': {
            'artifacts': [{
                'image': self.target_image,
                'workspace': self.build_context,
                'docker': {
                    'dockerfile': dockerfile_name
                }
            }]
        }
    }
    with open(self.filename, 'w') as f:
      yaml.dump(self._buildspec, f)
