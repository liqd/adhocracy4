/* eslint no-unused-vars: "off" */

// make jquery available for non-webpack js
var $ = window.jQuery = window.$ = require('jquery')
window.Tether = require('tether/dist/js/tether.js')

// load bootstrap components
var dropdown = require('bootstrap/js/src/dropdown.js')
var modal = require('bootstrap/js/src/modal.js')
var tab = require('bootstrap/js/src/tab.js')
var popover = require('bootstrap/js/src/popover.js')

// initialize moment locale
var moment = require('moment')
var django = require('django')
moment.locale(django.languageCode)

// enable bootstrap popover
$(function () {
  $('[data-toggle="popover"]').popover()
})

// expose react components
var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings

var ReactParagraphs = require('../../../apps/documents/assets/ParagraphBox.jsx')

module.exports = {
  'renderComment': ReactComments.renderComment,
  'renderRatings': ReactRatings.renderRatings,
  'renderParagraphs': ReactParagraphs.renderParagraphs
}
