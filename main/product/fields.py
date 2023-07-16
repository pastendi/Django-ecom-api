from django.core import checks
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Model


class OrderField(models.PositiveIntegerField):
    description = "Ordering product line of product"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_for_field_attribute(**kwargs)]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [checks.Error("OrderField must define a 'unique_for_field' attribute")]
        elif self.unique_for_field not in [f.name for f in self.model._meta.get_fields()]:
            return [
                checks.Error("'unique_for_field' entered doesn't match any existing model fields")
            ]
        return []

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            q = self.model.objects.all()
            try:
                # dynamic condition which can be used for both productline and product images ordering
                filterCondition = {
                    self.unique_for_field: getattr(model_instance, self.unique_for_field)
                }
                q = q.filter(**filterCondition)
                last_item = q.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:  # if there no product line and this is first item
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)
