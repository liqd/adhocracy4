def _(s):
    return s


django_standard_messages_to_override = [
    _("You have signed out."),
    _("Verify Your E-mail Address"),
    _("You must type the same password each time."),
    _("You have confirmed %(email)s."),
    _("You cannot remove your primary e-mail address (%(email)s)."),
    _("We have sent you an e-mail. Please contact us if "
      "you do not receive it within a few minutes.")
]
