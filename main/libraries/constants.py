from django.utils.translation import ugettext_lazy as _

REGION_CHOICES = (
    (19, 'Hlavní město Praha'),
    (27, 'Středočeský kraj'),
    (35, 'Jihočeský kraj'),
    (43, 'Plzeňský kraj'),
    (51, 'Karlovarský kraj'),
    (60, 'Ústecký kraj'),
    (78, 'Liberecký kraj'),
    (86, 'Královéhradecký kraj'),
    (94, 'Pardubický kraj'),
    (108, 'Kraj Vysočina'),
    (116, 'Jihomoravský kraj'),
    (124, 'Olomoucký kraj'),
    (132, 'Moravskoslezský kraj'),
    (141, 'Zlínský kraj'),
    (1, 'Bratislavský kraj'),
    (2, 'Trnavský kraj'),
    (3, 'Trenčiansky kraj'),
    (4, 'Nitriansky kraj'),
    (5, 'Žilinský kraj'),
    (6, 'Banskobystrický kraj'),
    (7, 'Prešovský kraj'),
    (8, 'Košický'),
)

WEEKDAYS = [  # starting from 0 to match Python weekday formatting
    (0, _('Pondělí')),
    (1, _('Úterý')),
    (2, _('Středa')),
    (3, _('Čtvrtek')),
    (4, _('Pátek')),
    (5, _('Sobota')),
    (6, _('Neděle')),
]

WEEKDAYS_PLURAL = [  # starting from 0 to match Python weekday formatting
    (0, _('Pondělí')),
    (1, _('Úterý')),
    (2, _('Středy')),
    (3, _('Čtvrtky')),
    (4, _('Pátky')),
    (5, _('Soboty')),
    (6, _('Neděle')),
]

WEEKDAYS_SHORT = [  # starting from 0 to match Python weekday formatting
    (0, _('Po')),
    (1, _('Út')),
    (2, _('St')),
    (3, _('Čt')),
    (4, _('Pá')),
    (5, _('So')),
    (6, _('Ne')),
]

