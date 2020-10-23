"""Step Implementer for the generate-metadata step for npm.

Step Configuration
------------------

Step configuration expected as input to this step.
Could come from either configuration file or
from runtime configuration.

| Configuration Key | Required? | Default          | Description
|-------------------|-----------|------------------|-----------
| `package-file     | True      | `'package.json'` | node.js package file to
|                   |            |                 | ead the app version out of

Expected Previous Step Results
------------------------------

Results expected from previous steps that this step requires.

.. Note:: This step implementer does not expect results from any previous steps.

Results
-------

Results output by this step.

| Result Key    | Description
|---------------|------------
| `app-version` | Value to use for `version` portion of semantic version (https://semver.org/). \
                    Uses the version read out of the given pom file.
"""

import os.path
import json

from tssc import StepImplementer
from tssc.step_result import StepResult

DEFAULT_CONFIG = {
    'release-branch': 'master'
}

REQUIRED_CONFIG_KEYS = [
    'package-file'
]

class Npm(StepImplementer): # pylint: disable=too-few-public-methods
    """
    StepImplementer for the generate-metadata step for npm.
    """

    @staticmethod
    def step_implementer_config_defaults():
        """
        Getter for the StepImplementer's configuration defaults.

        Notes
        -----
        These are the lowest precedence configuration values.

        Returns
        -------
        dict
            Default values to use for step configuration values.
        """
        return DEFAULT_CONFIG

    @staticmethod
    def required_runtime_step_config_keys():
        """
        Getter for step configuration keys that are required before running the step.

        See Also
        --------
        _validate_runtime_step_config

        Returns
        -------
        array_list
            Array of configuration keys that are required before running the step.
        """
        return []

    def _run_step(self):
        """Runs the TSSC step implemented by this StepImplementer.

        Returns
        -------
        dict
            Results of running this step.
        """
        step_result = StepResult.from_step_implementer(self)

        app_version = None
        pre_release = None
        build = None
        release_branch = self.get_config_value('release-branch')

        app_version = self.get_config_value('app-version')
        if app_version is None:
            app_version = self.get_result_value(artifact_name='app-version')
        if app_version is None:
          step_result.success = False
          step_result.message = f'No value for (app-version) provided via runtime flag' \
                '(app-version) or from prior step implementer ({self.step_name}).'
          return step_result

        pre_release = self.get_config_value('pre-release')
        if pre_release is None:
            pre_release = self.get_result_value(artifact_name='pre-release')
        if pre_release is None:
          step_result.success = False
          step_result.message = f'No value for (pre-release) provided via runtime flag' \
                '(pre-release) or from prior step implementer ({self.step_name}).'
          return step_result

        build = self.get_config_value('build')
        if build is None:
            build = self.get_result_value(artifact_name='build')
        if build is None:
          step_result.success = False
          step_result.message = f'No value for (build) provided via runtime flag' \
                '(build) or from prior step implementer ({self.step_name}).'
          return step_result

        if pre_release == release_branch:
            version = f'{app_version}+{build}'
            image_tag = f'{app_version}'
        else:
            version = f'{app_version}-{pre_release}+{build}'
            image_tag = f'{app_version}-{pre_release}'

        step_result.add_artifact(
            name='version',
            value=version
        )
        step_result.add_artifact(
            name='container-image-version',
            value=image_tag
        )

        return step_result
