var ReportModal = require('./ReportModal')
var React = require('react')
var ReactDOM = require('react-dom')
const django = require('django')

module.exports.ReportModal = ReportModal

module.exports.renderReports = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))

  el.setAttribute('href', '#' + props.modalName)
  el.setAttribute('data-toggle', 'modal')

  const container = document.createElement('div')
  document.body.appendChild(container)

  ReactDOM.render((
    <ReportModal
      name={props.modalName}
      title={django.gettext('You want to report this content? Your message will be sent to the moderation. The moderation will look at the reported content. The content will be deleted if it does not meet our discussion rules (netiquette).')}
      btnStyle="cta"
      objectId={props.objectId}
      contentType={props.contentType}
    />
  ), container)
}
