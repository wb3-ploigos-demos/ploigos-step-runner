import os

import unittest
from testfixtures import TempDirectory

from tssc import TSSCFactory
from tssc.step_implementers.generate_metadata import Npm
from tssc.step_result import StepResult
from tssc import StepImplementer

from tests.helpers.base_tssc_test_case import BaseTSSCTestCase
from tests.helpers.test_utils import run_step_test_with_result_validation
from tests.helpers.base_step_implementer_test_case import BaseStepImplementerTestCase

from tssc import StepImplementer

class TestStepImplementerGenerateMetadataNpm(BaseStepImplementerTestCase):
    def create_step_implementer(
            self,
            step_config={},
            test_config={},
            results_dir_path='',
            results_file_name='',
            work_dir_path=''
    ):
        return self.create_given_step_implementer(
            step_implementer=Npm,
            step_config=step_config,
            test_config=test_config,
            results_dir_path=results_dir_path,
            results_file_name=results_file_name,
            work_dir_path=work_dir_path
        )

    def test_step_implementer_config_defaults(self):
        defaults = Npm.step_implementer_config_defaults()
        expected_defaults = {
            'package-file': 'package.json'
        }
        self.assertEqual(defaults, expected_defaults)

    def test_required_runtime_step_config_keys(self):
        required_keys = Npm.required_runtime_step_config_keys()
        expected_required_keys = ['package-file']
        self.assertEqual(required_keys, expected_required_keys)

    """
    def test_run_step_pass(self):
        
        with TempDirectory() as temp_dir:
            repo = Repo.init(str(temp_dir.path))

            create_git_commit_with_sample_file(temp_dir, repo)
        
            "below is my change"

            "package_file = self.get_config_value('package-file')"

            package_file = {
                'package-file': 'package.json'
            }

            os.path.exists(package_file)

            step_config = {
                'package-file': package_file
            }
            test_config = {'step-name': 'generate-metadata', 'implementer': 'Npm'}

            step_implementer = self.create_step_implementer(
                step_config=step_config,
                test_config=test_config,
            )

            result = step_implementer._run_step()
            self.assertTrue(result.success, True)
    """

    def test_package_file(self):
        with TempDirectory() as temp_dir:
            temp_dir.write('package.json',b'''{
              "name": "my-awesome-package",
              "version": "1.0.0"
            }''')
            package_file_path = os.path.join(temp_dir.path, 'package.json')
           
            step_config = {
                'package-file': str(package_file_path)
            }
            test_config = {'step-name': 'generate-metadata', 'implementer': 'Npm'}

            step_implementer = self.create_step_implementer(
                step_config=step_config,
                test_config=test_config
            )

            result = step_implementer._run_step()

            expected_step_result = StepResult(step_name='generate-metadata', sub_step_name='Npm',sub_step_implementer_name='Npm')
            expected_step_result.success = True
            expected_step_result.message = f''

            "self.assertEqual(result.get_step_result(), expected_step_result.get_step_result())"
            self.assertAlmostEqual(result.success, expected_step_result.success)

    """
    def test_package_file_missing_version(self):
        with TempDirectory() as temp_dir:
            temp_dir.write('package.json',b'''{
              "name": "my-awesome-package"
            }''')
            package_file_path = os.path.join(temp_dir.path, 'package.json')
            config = {
                'tssc-config': {
                    'generate-metadata': {
                        'implementer': 'Npm',
                        'config': {
                            'package-file': str(package_file_path)
                        }
                    }
                }
            }

            expected_step_results = {}

            with self.assertRaisesRegex(
                    ValueError,
                    r"Given npm package file: " + package_file_path + " does not contain a \"version\" key"):
                run_step_test_with_result_validation(temp_dir, 'generate-metadata', config, expected_step_results, runtime_args={'repo-root': str(temp_dir.path), 'build': '1234'})
    """