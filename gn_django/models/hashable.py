from django.conf import settings
from django.db import models
from hashids import Hashids

_hashids = Hashids(
    salt=settings.SECRET_KEY,
    alphabet='abcdefghijklmnopqrstuvwxyz1234567890',
)


class HashableManager(models.Manager):
    """
    Manager for a model which uses hash IDs.
    """
    def get_by_hashid(self, hashid, *args, **kwargs):
        """
        Return a single object matching the given hash ID value.

        Args:
            * `hashid` - `str` - a valid hash ID.
            * Any additional args/kwargs to filter by, same as the QuerySet
              filter() method.

        Returns:
            `Model`

        Raises:
            * `DoesNotExist` - if hash ID is not decodable or the ID does not
              correspond to an object within the filtered results.
            * `MultipleObjectsReturned` - if hash ID is somehow ambiguous.
        """
        decoded = _hashids.decode(hashid)
        if len(decoded) != 1:
            raise self.model.DoesNotExist('Hash does not correspond to a valid ID')
        return self.filter(*args, **kwargs).get(id=decoded[0])


class Hashable(models.Model):
    """
    Abstract model class for a model which uses hash IDs.

    Classes that extend from this model should also use HashableManager for
    their objects property.
    """
    class Meta:
        abstract = True

    @property
    def hashid(self):
        """
        Returns the hash ID for this object.

        Returns:
            `str`

        Raises:
            * `ValueError` - if model has not been saved. The primary key field
              is required to generate the hash ID.
        """
        if not self.pk:
            raise ValueError('hashid cannot be used on unsaved objects.')
        return _hashids.encode(self.pk)
