def _(s):
    return s


django_standard_messages_to_override = [
    _("You have signed out."),
    _("Verify Your E-mail Address"),
    _("You must type the same password each time."),
    _("You have confirmed %(email)s."),
    _("You cannot remove your primary e-mail address (%(email)s)."),
    _("We have sent you an e-mail. Please contact us if "
      "you do not receive it within a few minutes."),
    _("We have sent an e-mail to you for verification. "
      "Follow the link provided to finalize the signup process. "
      "If you do not see the verification e-mail in your main inbox, "
      "check your spam folder. "
      "Please contact us if you do not receive the verification e-mail "
      "within a few minutes."),
    _("We have sent you an e-mail. If you have not received it "
      "please check your spam folder. Otherwise contact us if you "
      "do not receive it in a few minutes."),
    _(u'You must select a minimum of  %(limit_value)d choices.'),
    _(u'You must select a maximum of  %(limit_value)d choices.'),
    _('Enter a valid email address.')
]
