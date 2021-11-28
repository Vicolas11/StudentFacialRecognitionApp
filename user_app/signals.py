from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'first_name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "<a id='reset_token' href='http://127.0.0.1:8000/password_confirm/'>" + "{}?token={}".format(instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),reset_password_token.key) + "></a></body></html>",
        'reset_password': "{}?token={}".format(instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),reset_password_token.key)
    }

    link = context['reset_password'].split("/")[6].split("=")[1] 
    instance.request.session['reset_link'] = link

    # render email text
    email_html_message = render_to_string('passwordreset/user_reset_password.html', context)
    email_plaintext_message = render_to_string('passwordreset/user_reset_password.txt', context)    

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="FaceAttandanceApp"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
