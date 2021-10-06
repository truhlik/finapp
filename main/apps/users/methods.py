from main.apps.users.models import User


def is_user_exist(email: str, pk=None) -> bool:
    """ Vrací zda uživatel s daným email již existuje. """

    qs = User.objects.filter(email=email)
    if pk is not None:
        qs = qs.exclude(pk=pk)
    return qs.exists()


def set_printer_profile_id(user: User, profile_id: int = None):
    """ Denormalizuje IDčko profilu modeláře. Pokud je profil smazán, tak nastav None. """

    user.d_printer_profile_id = profile_id
    user.save()


def set_modeler_profile_id(user: User, profile_id: int = None):
    """ Denormalizuje IDčko profilu modeláře. Pokud je profil smazán, tak nastav None. """

    user.d_modeler_profile_id = profile_id
    user.save()
