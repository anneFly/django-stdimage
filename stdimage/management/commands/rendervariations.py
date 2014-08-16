# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

from django.core.management import BaseCommand
from django.db.models import get_model


class Command(BaseCommand):
    help = 'Renders all variations of a StdImageField.'
    args = '<app.model.field app.model.field>'

    def handle(self, *args, **options):
        for route in args:
            app_name, model_name, field_name = route.rsplit('.')
            model_class = get_model(app_name, model_name)
            queryset = model_class.objects\
                .exclude(**{"%s__isnull" % field_name: True})\
                .exclude(**{field_name: ''})
            for instance in queryset:
                field_file = getattr(instance, field_name)
                field = field_file.field
                self.stdout.write('Rendering variations for "%s" using file: %s' % (instance, field_file))
                for name, variation in field.variations.items():
                    variation_file_name = field_file.render_and_save_variation(field_file.name, field_file, variation)
                    self.stdout.write("--> %s: %s" % (name, variation_file_name))