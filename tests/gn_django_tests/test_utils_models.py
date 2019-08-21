from unittest.mock import call, patch

from django.dispatch import Signal
from django.test import TestCase

from gn_django.utils import super_receiver


class TestSuperReceiver(TestCase):
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(C):
        pass

    @patch('django.dispatch.Signal.connect')
    def test_connect_to_subclasses(self, connect):
        """
        Test connecting to a class with multiple descendants.
        """
        signal = Signal()

        @super_receiver(signal, self.A)
        def fn():
            pass

        connect.assert_has_calls([
            call(fn, self.B),
            call(fn, self.C),
            call(fn, self.D),
        ], any_order=True)

    @patch('django.dispatch.Signal.connect')
    def test_connect_to_class(self, connect):
        """
        Test connecting to a class with no descendants (which does nothing).
        """
        signal = Signal()

        @super_receiver(signal, self.B)
        def fn():
            pass

        connect.assert_not_called()
