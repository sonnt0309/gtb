import oscar.apps.catalogue.apps as apps


class CatalogueConfig(apps.CatalogueConfig):
    label = 'catalogue'
    name = 'apps.custom_oscar.catalogue'
    verbose_name = 'catalogue'
