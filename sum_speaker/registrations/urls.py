from django.contrib.auth import views as auth_views
from django.conf.urls import url,include

urlpatterns = [
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset' 
    , kwargs={'template_name': 'registrations/password_reset_form.html'
                ,'email_template_name': 'registrations/password_reset_email.html'
                ,'subject_template_name':'registrations/password_reset_subject.txt'
                }),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done', kwargs={'template_name': 'registrations/password_reset_done.html'}),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.password_reset_confirm, name='password_reset_confirm' , kwargs={'template_name': 'registrations/password_reset_confirm.html'}),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete', kwargs={'template_name': 'registrations/password_reset_complete.html'}),
]