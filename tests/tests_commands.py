# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.management import call_command


class CommandTestCase(TestCase):
    def test_scanlogfiles(self):
        call_command('scanlogfiles')
