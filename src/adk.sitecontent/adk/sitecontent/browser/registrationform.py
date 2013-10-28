from Acquisition import aq_inner
from zope import interface, schema
from zope.formlib import form
from five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from zope.app.form.browser import RadioWidget as _RadioWidget

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from adk.sitecontent import sitecontentMessageFactory as _

MESSAGE_TEMPLATE = """\
Neue Kursanmeldung: %(salutation)s %(firstname)s %(lastname)s
Adresse:
%(street)s
%(city)s %(postalcode)s
%(country)s

Tel: %(phone)s
Fax: %(fax)s
E-Mail: %(email)s
geboren: %(birthday)s
Nationalitaet: %(nationality)s

*** Anmeldung fuer Kurs ***

Kurs: %(course)s
Kursbeginn: %(startdate)s
Dauer: %(duration)s Wochen
Deutschkenntnisse: %(knowledge)s

ADK bekannt durch: %(recommendation)s

Unterkunft: %(accomodation)s

Anreise: %(arrival)s
Abreise: %(departure)s
Anreise mit: %(transport)s
Flughafentransfer: %(airporttransfer)s
Raucher: %(smoker)s

Nachricht an ADK:

%(message)s

---
Anmeldeformular adk-german-courses.com

"""


def validateTermsAccept(value):
    if not value is True:
        return False
    return True


class IRegistrationFormSchema(interface.Interface):
    # -*- extra stuff goes here -*-

    salutation = schema.Choice(
        title=u'Salutation',
        description=u'',
        required=True,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='Mrs.', token='Misses', title=_(u'Mrs.')),
            SimpleTerm(value='Mr.', token='Mister', title=_(u'Mr.'))
        ))
    )
    firstname = schema.TextLine(
        title=u'Firstname',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    lastname = schema.TextLine(
        title=u'Lastname',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    street = schema.TextLine(
        title=u'Street',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    city = schema.TextLine(
        title=u'City',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    postalcode = schema.TextLine(
        title=u'Postal code',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    country = schema.TextLine(
        title=u'Country',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    occupation = schema.TextLine(
        title=u'Occupation',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    phone = schema.TextLine(
        title=u'Phone',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    fax = schema.TextLine(
        title=u'Fax',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    email = schema.TextLine(
        title=u'E-Mail',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    birthday = schema.TextLine(
        title=u'Date of Birth',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    nationality = schema.TextLine(
        title=u'Nationality',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    course = schema.Choice(
        title=u'Herby, I register for following course',
        description=u'',
        required=True,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='Intensive Course',
                       token='Intensive Course', title=_(u'Intensive Course')),
            SimpleTerm(value='Intensive Plus Course 24h',
                       token='Intensive Plus Course (24 lessons)',
                       title=_(u'Intensive Plus Course (24 lessions)')),
            SimpleTerm(value='Intensive Plus Course 30h',
                       token='Intensive Plus Course (30 lessions)',
                       title=_(u'Intensive Plus Course (30 lessons)')),
            SimpleTerm(value='Private Tuition',
                       token='Private Tuition', title=_(u'Private Tuition')),
            SimpleTerm(value='DSH Preperation Course',
                       token='DSH Preparation Course',
                       title=_(u'DSH Preparation Course')),
            SimpleTerm(value='TestDAF',
                       token='TestDAF Preparation Course',
                       title=_(u'TestDAF Preparation Course')),
            SimpleTerm(value='Summer Course Classic',
                       token='Summer Course Classic',
                       title=_(u'Summer Course Classic')),
        ))
    )

    startdate = schema.Date(
        title=u'Course starting date',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    duration = schema.TextLine(
        title=u'Course duration in weeks',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    knowledge = schema.Choice(
        title=u'German language skills',
        description=u'',
        required=True,
        readonly=False,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='none', token='none', title=_(u'none')),
            SimpleTerm(value='elementary', token='elementary',
                       title=_(u'elementary')),
            SimpleTerm(value='intermediate', token='intermediate',
                       title=_(u'intermediate')),
            SimpleTerm(value='good', token='good', title=_(u'good')),
            SimpleTerm(value='advanced', token='advanced',
                       title=_(u'advanced'))
        ))
    )
    recommendation = schema.Choice(
        title=u'I learned about Augsburger Deutschkurse from',
        description=u'',
        required=False,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='advertisment', token='advertisment',
                       title=_(u'advertisment')),
            SimpleTerm(value='former student', token='former student',
                       title=_(u'former student')),
            SimpleTerm(value='recommendation', token='recommendation',
                       title=_(u'recommendation')),
            SimpleTerm(value='website', token='website', title=_(u'website')),
            SimpleTerm(value='other sources', token='other sources',
                       title=_(u'other sources'))
        ))
    )
    accomodation = schema.Choice(
        title=u'Preferred type of accomodation',
        description=u'',
        required=True,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='host family, double room, half board',
                       token='host family, double room, half board',
                       title=_(u'host family, double room, half board')),
            SimpleTerm(value='host family, double room, full board',
                       token='host family, double room, full board',
                       title=_(u'host family, double room, full board')),
            SimpleTerm(value='host family, single room,half board',
                       token='host family, single room, half board',
                       title=_(u'host family, single room, half board')),
            SimpleTerm(value='host family, single room, full board',
                       token='host family, single room, full board',
                       title=_(u'host family, single room, full board')),
            SimpleTerm(value='hotel or guesthouse',
                       token='hotel or guesthouse',
                       title=_(u'hotel or guesthouse')),
            SimpleTerm(value='room in a shared flat',
                       token='room in a shared flat',
                       title=_(u'room in a shared flat')),
            SimpleTerm(value='no accomodation needed',
                       token='no accomodation needed',
                       title=_(u'no accomodation needed'))
        ))
    )
    arrival = schema.Date(
        title=u'Day of arrival',
        description=u'',
        required=True,
        readonly=False,
        default=None,
    )
    departure = schema.Date(
        title=u'Day of departure',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    transport = schema.Choice(
        title=u'I will arrive by',
        description=u'',
        required=True,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='plane', token='plane', title=_(u'plane')),
            SimpleTerm(value='train', token='train', title=_(u'train')),
            SimpleTerm(value='car', token='car', title=_(u'car'))
        ))
    )
    airporttransfer = schema.Choice(
        title=u'Airport transfer',
        description=u'',
        required=True,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='yes', token='yes', title=_(u'yes')),
            SimpleTerm(value='no', token='no', title=_(u'no'))
        ))
    )
    smoker = schema.Choice(
        title=u'Do you smoke?',
        description=u'',
        required=False,
        readonly=False,
        default=None,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='yes', token='yes', title=_(u'yes')),
            SimpleTerm(value='no', token='no', title=_(u'no'))
        ))
    )
    message = schema.Text(
        title=u'Message',
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    terms_accept = schema.Bool(
        title=_(u"I confirm the correctness of my entries and acknowledge the "
                u"terms and conditions of ADK."),
        required=True,
        constraint=validateTermsAccept,
    )


def RadioWidget(field, request):
    vocabulary = field.vocabulary
    widget = _RadioWidget(field, vocabulary, request)
    return widget


class RegistrationForm(formbase.PageForm):
    form_fields = form.FormFields(IRegistrationFormSchema)
    form_fields['salutation'].custom_widget = RadioWidget
    label = _(u'Registration Form')
    description = _(u'Register with Augsburger Deutschkurse.')
    template = ViewPageTemplateFile('registrationform.pt')
    result_template = ViewPageTemplateFile('reservation_result.pt')

    @form.action(_(u'Register'))
    def actionRegister(self, action, data):
        pass
        context = aq_inner(self.context)
        mailhost = getToolByName(context, 'MailHost')
        to_address = 'info@adk-german-courses.com'
        mFrom = data['email']
        subject = 'Neue Kursanmeldung: %s %s' % (data['firstname'],
                                                 data['lastname'])
        messageText = MESSAGE_TEMPLATE % data
        mailhost.send(messageText,
                      mto=to_address,
                      mfrom=mFrom,
                      subject=subject,
                      encode=None,
                      immediate=False,
                      charset='utf8',
                      msg_type='text/plain')
        IStatusMessage(self.request).add(
            _(u'Your reservation has been forwarded successfully.'),
            type='info')
        return self.result_template()
