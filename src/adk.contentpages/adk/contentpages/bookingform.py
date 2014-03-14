from Acquisition import aq_inner
from five import grok
from plone import api
from plone.directives import form

from zope import schema
from z3c.form import button

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from adk.contentpages.sectionfolder import ISectionFolder

from adk.contentpages import MessageFactory as _


def validateAcceptConstraint(value):
    """ Check if the terms and conditions have been accepted. """
    if not value is True:
        return False
    return True


class IBooking(form.Schema):

    salutation = schema.Choice(
        title=_(u"Salutation"),
        values=[_(u'Frau'), _(u'Herr')],
        required=True,
    )
    firstname = schema.TextLine(
        title=_(u"Firstname"),
        required=True,
    )
    lastname = schema.TextLine(
        title=_(u'Lastname'),
        required=True,
    )

    city = schema.TextLine(
        title=_(u'City'),
        required=True,
    )

    postcode = schema.TextLine(
        title=_(u'Postal Code'),
        required=True,
    )

    country = schema.TextLine(
        title=_(u'Country'),
        required=True,
        default=u'Deutschland',
    )
    occupation = schema.TextLine(
        title=_(u"Occupation"),
        description=u'',
        required=False,
        readonly=False,
        default=None,
    )
    phone = schema.TextLine(
        title=_(u"Phone"),
        description=u'',
        required=True,
    )
    fax = schema.TextLine(
        title=_(u"Fax"),
        description=u'',
        required=False,
    )
    email = schema.TextLine(
        title=_(u"E-Mail"),
        description=u'',
        required=True,
    )
    birthday = schema.TextLine(
        title=_(u"Date of Birth"),
        description=u'',
        required=True,
    )
    nationality = schema.TextLine(
        title=_(u"Nationality"),
        description=u'',
        required=False,
    )
    course = schema.Choice(
        title=u'Herby, I register for following course',
        description=u'',
        required=True,
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
    )
    duration = schema.TextLine(
        title=u'Course duration in weeks',
        description=u'',
        required=False,
    )
    knowledge = schema.Choice(
        title=u'German language skills',
        description=u'',
        required=True,
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
    )
    departure = schema.Date(
        title=u'Day of departure',
        description=u'',
        required=False,
    )
    transport = schema.Choice(
        title=u'I will arrive by',
        description=u'',
        required=True,
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
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='yes', token='yes', title=_(u'yes')),
            SimpleTerm(value='no', token='no', title=_(u'no'))
        ))
    )
    smoker = schema.Choice(
        title=u'Do you smoke?',
        description=u'',
        required=False,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value='yes', token='yes', title=_(u'yes')),
            SimpleTerm(value='no', token='no', title=_(u'no'))
        ))
    )
    message = schema.Text(
        title=u'Message',
        description=u'',
        required=False,
    )
    terms_accept = schema.Bool(
        title=_(u"I confirm the correctness of my entries and acknowledge the "
                u"terms and conditions of ADK."),
        required=True,
        constraint=validateAcceptConstraint,
    )


class BookingForm(form.SchemaForm):
    grok.context(ISectionFolder)
    grok.require('zope2.View')
    grok.name('booking-form')

    schema = IBooking
    ignoreContext = True
    ignoreRequest = False

    label = _(u"Booking form")
    description = _(u"Register for the selected course by filling out the "
                    u"form below.")

    def updateActions(self):
        super(BookingForm, self).updateActions()
        self.actions['submit'].addClass("btn btn-primary btn-lg")
        self.actions['cancel'].addClass("btn btn-link")

    @button.buttonAndHandler(_(u'Book now'), name='submit')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.status = self.send_email(data)

    @button.buttonAndHandler(_(u"cancel"))
    def handleCancel(self, action):
        context = aq_inner(self.context)
        msg = _(u"Process has been cancelled."),
        api.portal.show_message(message=msg, request=self.request)
        return self.request.response.redirect(context.absolute_url())

    def send_email(self, data):
        """ Construct and send the registration request. """
        context_url = self.context.absolute_url()
        mto = 'info@augsburger-deutschkurse.de'
        envelope_from = 'anfrage@adk-german-courses.com'
        subject = 'Buchungsanfrage Sprachkurse'
        options = data
        body = ViewPageTemplateFile("booking_email.pt")(self, **options)
        # send email
        mailhost = api.portal.get_tool(name='MailHost')
        mailhost.send(body,
                      mto=mto,
                      mfrom=envelope_from,
                      subject=subject,
                      charset='utf-8')

        IStatusMessage(self.request).add(
            _(u"Thank you for your interest in this special. "
              u"Your Request has been forwarded to the hotel.")
        )
        return self.request.response.redirect(
            '%s/@@booking-form-success' % context_url)


class BookingFormSuccess(grok.View):
    grok.context(ISectionFolder)
    grok.require('zope2.View')
    grok.name('booking-form-success')
