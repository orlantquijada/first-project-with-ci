from django.conf import settings
from django.db import models
from django.utils import timezone


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModelMixin(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModelMixin, self).delete()


class ArchivableQuerySet(models.QuerySet):
    def active(self):
        return self.filter(archived_at=None)

    def archived(self):
        return self.exclude(archived_at=None)


class ArchivableManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.non_archived_only = kwargs.pop("non_archived_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.non_archived_only:
            return ArchivableQuerySet(self.model).active()
        return ArchivableQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()

    def archived(self):
        return self.get_queryset().archived()


class ArchivableModelMixin(models.Model):
    archived_at = models.DateTimeField(blank=True, null=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.PROTECT,
        related_name="archived_%(class)s",
        null=True,
        blank=True,
    )

    objects = ArchivableManager()
    all_objects = ArchivableManager(non_archived_only=False)

    class Meta:
        abstract = True

    def archive(self, user):
        self.archived_at = timezone.now()
        self.archived_by = user
        self.save()

    def unarchive(self):
        self.archived_at = None
        self.archived_by = None
        self.save()


class ArchivableAndSoftDeletionQuerySet(ArchivableQuerySet, SoftDeletionQuerySet):
    pass


class ArchivableAndSoftDeletionManager(ArchivableManager, SoftDeletionManager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        self.non_archived_only = kwargs.pop("non_archived_only", True)
        models.Manager.__init__(self, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {}
        if self.alive_only:
            filter_kwargs["deleted_at"] = None
        if self.non_archived_only:
            filter_kwargs["archived_at"] = None
        if filter_kwargs:
            return ArchivableAndSoftDeletionQuerySet(self.model).filter(**filter_kwargs)
        return ArchivableAndSoftDeletionQuerySet(self.model)


class ArchivableAndSoftDeletionModelMixin(ArchivableModelMixin, SoftDeletionModelMixin):
    objects = ArchivableAndSoftDeletionManager()
    all_excluding_deleted_objects = ArchivableAndSoftDeletionManager(
        non_archived_only=False
    )
    all_objects = ArchivableAndSoftDeletionManager(
        non_archived_only=False, alive_only=False
    )

    class Meta:
        abstract = True
