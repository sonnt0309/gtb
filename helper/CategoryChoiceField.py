from django import forms
from django.utils.translation import ugettext_lazy as _


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.profile.full_name_kanji


class OptionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.option_name,)


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.product_name,)


class ProductNameIDChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.product_name, obj.product_key)
