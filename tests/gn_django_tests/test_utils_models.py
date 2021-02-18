from datetime import timedelta
from unittest.mock import call, patch

from django.dispatch import Signal
from django.test import TestCase
from django.utils.timezone import now

from core.models import UpdatableModel
from gn_django.utils import autonow_off, super_receiver


class TestAutonowOff(TestCase):
    def test_autonow_off(self):
        """
        Test the autonow_off context manager.
        """
        # Test default model behaviour.
        obj = UpdatableModel.objects.create(
            created_at='2020-09-01T12:30:00+00:00',
            updated_at='2020-09-09T18:22:33+00:00',
        )
        obj.refresh_from_db()
        self.assertAlmostEqual(now(), obj.updated_at, delta=timedelta(seconds=1))
        self.assertAlmostEqual(now(), obj.created_at, delta=timedelta(seconds=1))
        # Test creation with autonow_off.
        with autonow_off(UpdatableModel):
            obj = UpdatableModel.objects.create(
                created_at='2020-09-01T12:30:00+00:00',
                updated_at='2020-09-09T18:22:33+00:00',
            )
        obj.refresh_from_db()
        self.assertEqual('2020-09-01T12:30:00+00:00', obj.created_at.isoformat())
        self.assertEqual('2020-09-09T18:22:33+00:00', obj.updated_at.isoformat())
        # Test creation after using autonow_off (that should behave as normal).
        obj = UpdatableModel.objects.create(
            created_at='2020-10-10T08:00:00+00:00',
            updated_at='2020-10-10T09:13:04+00:00',
        )
        obj.refresh_from_db()
        self.assertAlmostEqual(now(), obj.created_at, delta=timedelta(seconds=1))
        self.assertAlmostEqual(now(), obj.updated_at, delta=timedelta(seconds=1))

    def test_autonow_off_exception(self):
        """
        Test that autonow_off returns the model to its normal state, even if
        an exception occurs in its context.
        """
        with self.assertRaises(Exception):
            with autonow_off(UpdatableModel):
                raise Exception('Test exception')
        obj = UpdatableModel.objects.create(
            created_at='2020-10-10 08:00:00',
            updated_at='2020-10-10 09:13:04',
        )
        obj.refresh_from_db()
        self.assertLessEqual(now() - obj.created_at, timedelta(seconds=1))
        self.assertLessEqual(now() - obj.updated_at, timedelta(seconds=1))


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
