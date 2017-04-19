var ReportModal = require('./ReportModal')
var React = require('react')
var ReactDOM = require('react-dom')
let django = require('django')

module.exports.ReportModal = ReportModal

module.exports.renderReports = function (mountpoint) {
  let el = document.getElementById(mountpoint)
  let props = JSON.parse(el.getAttribute('data-attributes'))

  el.setAttribute('href', '#' + props.modalName)
  el.setAttribute('data-toggle', 'modal')

  let container = document.createElement('div')
  document.body.appendChild(container)

  ReactDOM.render((
    <ReportModal
      name={props.modalName}
      title={django.gettext('Are you sure you want to report this item?')}
      btnStyle="cta"
      objectId={props.objectId}
      contentType={props.contentType} />
  ), container)
}
