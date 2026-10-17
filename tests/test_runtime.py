from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import run


class RuntimeTests(unittest.TestCase):
    def test_standalone_exe_keeps_data_beside_exe(self):
        with tempfile.TemporaryDirectory() as temp:
            executable = Path(temp) / 'Musica.exe'
            with patch.object(run.sys, 'frozen', True, create=True), patch.object(run.sys, 'executable', str(executable)):
                self.assertEqual(run.application_home(), Path(temp).resolve())

    def test_project_release_reuses_existing_project_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'run.py').touch()
            executable = root / 'releases' / 'Musica-Windows-x64-v0.2.0' / 'Musica.exe'
            with patch.object(run.sys, 'frozen', True, create=True), patch.object(run.sys, 'executable', str(executable)):
                self.assertEqual(run.application_home(), root.resolve())
