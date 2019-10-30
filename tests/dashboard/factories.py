import factory

from adhocracy4.dashboard import DashboardComponent


class DashboardTestComponent(DashboardComponent):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def is_effective(self, project_or_module):
        return self.effective

    def get_progress(self, project_or_module):
        return self.progress

    def get_urls(self):
        return self.urls

    def get_base_url(self, project_or_module):
        return self.urls[0]


class DashboardTestComponentFactory(factory.Factory):
    class Meta:
        model = DashboardTestComponent

    identifier = factory.Sequence(lambda n: 'test-component-%d' % n)
    weight = factory.Sequence(lambda n: n)
    label = factory.Faker('sentence', nb_words=2)

    effective = True
    progress = (1, 1)
    urls = [('^test/dashboard/component/$',
             lambda *args: None,
             'dashboard-component-test-url')]
