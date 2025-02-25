from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class SimpleCartDeleteProductForm(forms.Form):
    pass


class AbstractCartForm(object):
    quantity: int
    override: bool


class SimpleCartAddProductForm(
    AbstractCartForm,
    forms.Form,
):
    quantity = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.HiddenInput,
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )


class SimpleCartRemoveProductForm(
    AbstractCartForm,
    forms.Form,
):
    quantity = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.HiddenInput,
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )


class CartAddProductForm(AbstractCartForm, forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="Количество",
    )

    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )
