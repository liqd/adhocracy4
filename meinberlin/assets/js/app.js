/* eslint no-unused-vars: "off", no-new: "off" */

// make jquery available for non-webpack js
var $ = window.jQuery = window.$ = require('jquery')
window.Tether = require('tether/dist/js/tether.js')

require('shariff')
var Shariff = window.Shariff

// load bootstrap components
require('bootstrap')

require('slick-carousel')
require('slick-carousel/slick/slick.css')

var django = require('django')

// expose react components
var ReactComments = require('adhocracy4').comments
var ReactRatings = require('adhocracy4').ratings
var ReactReports = require('adhocracy4').reports
var ReactFollows = require('adhocracy4').follows

var ReactDocuments = require('../../apps/documents/assets/react_documents.jsx')
var ReactPolls = require('../../apps/polls/assets/react_polls.jsx')
var ReactMapTeaser = require('../../apps/plans/assets/react_map_teaser.jsx')

require('../../apps/actions/assets/timestamps.js')
require('../../apps/maps/assets/map-address.js')
require('../../apps/moderatorremark/assets/idea_remarks.js')
require('../../apps/newsletters/assets/dynamic_fields.js')
require('../../apps/dashboard/assets/ajax_modal.js')
require('../../assets/js/unload_warning.js')
require('../../apps/dashboard/assets/init_accordeons_cookie.js')

// This function is overwritten with custom behavior in embed.js.
var getCurrentPath = function () {
  return location.pathname
}

var initialiseWidget = function (namespace, name, fn) {
  var key = 'data-' + namespace + '-widget'
  var selector = '[' + key + '=' + name + ']'
  $(selector).each(function (i, el) {
    fn(el)

    // avoid double-initialisation
    el.removeAttribute(key)
  })
}

var init = function () {
  var shariffs = $('.shariff')
  if (shariffs.length > 0) {
    new Shariff(shariffs, {
      services: '[&quot;twitter&quot;,&quot;facebook&quot;,&quot;info&quot;]',
      infoUrl: '/shariff'
    })
  }

  if ($.fn.select2) {
    $('.js-select2').select2()
  }

  initialiseWidget('a4', 'comment', ReactComments.renderComment)
  initialiseWidget('a4', 'follows', ReactFollows.renderFollow)
  initialiseWidget('a4', 'ratings', ReactRatings.renderRatings)
  initialiseWidget('a4', 'reports', ReactReports.renderReports)

  initialiseWidget('mb', 'document-management', ReactDocuments.renderDocumentManagement)
  initialiseWidget('mb', 'polls', ReactPolls.renderPolls)
  initialiseWidget('mb', 'mapTeaser', ReactMapTeaser.renderFilter)
  initialiseWidget('mb', 'poll-management', ReactPolls.renderPollManagement)

  // carousel
  function getInitialSlide () {
    return parseInt($('#timeline-carousel').attr('data-initial-slide'))
  }

  $('.timeline-carousel__item').slick({
    initialSlide: getInitialSlide(),
    focusOnSelect: false,
    centerMode: true,
    dots: false,
    arrows: true,
    centerPadding: 30,
    mobileFirst: true,
    infinite: false,
    variableWidth: true,
    slidesToShow: 1,
    slidesToScroll: 1
  })
}

$(init)
window.init_widgets = init

module.exports = {
  getCurrentPath: getCurrentPath
}

// Closes bootstrap collapse on click elsewhere
$(document).on('click', function () {
  $('.collapse').collapse('hide')
})
