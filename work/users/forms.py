from registration.forms import (
    RegistrationForm,
    RegistrationFormTermsOfService,
    RegistrationFormUniqueEmail
    )


class SignUpForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    pass
