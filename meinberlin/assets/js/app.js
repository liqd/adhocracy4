/* eslint no-unused-vars: "off", no-new: "off" */
/* global location */

// make jquery available for non-webpack js
var $ = window.jQuery = window.$ = require('jquery')
window.Tether = require('tether/dist/js/tether.js')

// social share
var Shariff = require('shariff')

;(function (init) {
  $(init)
  $(document).on('a4.embed.ready', init)
})(function () {
  new Shariff($('.shariff'))
})

// load bootstrap components
var dropdown = require('bootstrap/js/src/dropdown.js')
var modal = require('bootstrap/js/src/modal.js')
var tab = require('bootstrap/js/src/tab.js')
var popover = require('bootstrap/js/src/popover.js')
var collapse = require('bootstrap/js/src/collapse.js')

// initialize moment locale
var moment = require('moment')
var django = require('django')
moment.locale(django.languageCode)

// expose react components
var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings
var ReactReports = require('adhocracy4').reports
var ReactFollows = require('adhocracy4').follows

var ReactDocuments = require('../../../apps/documents/assets/react_documents.jsx')
var ReactPolls = require('../../../apps/polls/assets/react_polls.jsx')

var relativeTimestamps = require('../../../apps/actions/assets/timestamps.js')

// This function is overwritten with custom behavior in embed.js.
var getCurrentHref = function () {
  return location.href
}

module.exports = {
  'renderComment': ReactComments.renderComment,
  'renderRatings': ReactRatings.renderRatings,
  'renderDocumentManagement': ReactDocuments.renderDocumentManagement,
  'renderPolls': ReactPolls.renderPolls,
  'renderPollManagement': ReactPolls.renderPollManagement,
  'renderReports': ReactReports.renderReports,
  'renderFollow': ReactFollows.renderFollow,
  'getCurrentHref': getCurrentHref
}
