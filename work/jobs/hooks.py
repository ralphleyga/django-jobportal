from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import (
    valid_ipn_received,
    invalid_ipn_received)


def show_me_the_money(sender, **kwargs):
    instance = sender
    # if instance.payment_status == ST_PP_COMPLETED:
    #     job = Job.objects.get(id=instance.job_id)
    #     expiration = timezone.now() + timedelta(days=settings.PREMIUM_DAYS)
    #     job.expired_date = expiration.date()
    #     job.save()
    import pdb; pdb.set_trace()
    
def do_not_show_me_the_money(sender, **kwargs):
    import pdb; pdb.set_trace()

valid_ipn_received.connect(show_me_the_money)
invalid_ipn_received.connect(do_not_show_me_the_money)