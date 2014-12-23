import datetime
import factory

from django.utils.timezone import now

from bluebottle.fundraisers.models import Fundraiser

from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from onepercentclub.tests.factory_models.project_factories import OnePercentProjectFactory


class FundraiserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Fundraiser

    title = factory.Sequence(lambda n: 'John Doe-{0}'.format(n))
    amount = 5000
    owner = factory.SubFactory(BlueBottleUserFactory)
    project = factory.SubFactory(OnePercentProjectFactory)
    deadline = now() + datetime.timedelta(days=30)  # 1 month deadline