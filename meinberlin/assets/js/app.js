import 'bootstrap' // load bootstrap components
import 'django'
import 'select2' // used to select projects in containers
import 'shariff'
import 'slick-carousel'

import '../../apps/actions/assets/timestamps.js'
import '../../apps/maps/assets/map-address.js'
import '../../apps/moderatorremark/assets/idea_remarks.js'
import '../../apps/newsletters/assets/dynamic_fields.js'
import '../../apps/dashboard/assets/ajax_modal.js'
import '../../apps/dashboard/assets/init_accordeons_cookie.js'

// expose react components
import {
  comments as ReactComments,
  ratings as ReactRatings,
  reports as ReactReports,
  follows as ReactFollows,
  widget as ReactWidget
} from 'adhocracy4'

import * as ReactDocuments from '../../apps/documents/assets/react_documents.jsx'
import * as ReactPolls from '../../apps/polls/assets/react_polls.jsx'
import * as ReactMapTeaser from '../../apps/plans/assets/react_map_teaser.jsx'
import * as ReactQuestions from '../../apps/livequestions/assets/react_questions.jsx'
import * as ReactQuestionsPresent from '../../apps/livequestions/assets/react_questions_present.jsx'

import * as Tether from 'tether'

window.Tether = Tether

function init () {
  const shariffs = $('.shariff')
  if (shariffs.length > 0) {
    /* eslint-disable no-new */
    new window.Shariff(shariffs, {
      services: '[&quot;twitter&quot;,&quot;facebook&quot;,&quot;info&quot;]',
      infoUrl: '/shariff'
    })
  }

  ReactWidget.initialise('a4', 'comment', ReactComments.renderComment)
  ReactWidget.initialise('a4', 'follows', ReactFollows.renderFollow)
  ReactWidget.initialise('a4', 'ratings', ReactRatings.renderRatings)
  ReactWidget.initialise('a4', 'reports', ReactReports.renderReports)

  ReactWidget.initialise('mb', 'document-management', ReactDocuments.renderDocumentManagement)
  ReactWidget.initialise('mb', 'polls', ReactPolls.renderPolls)
  ReactWidget.initialise('mb', 'mapTeaser', ReactMapTeaser.renderFilter)
  ReactWidget.initialise('mb', 'poll-management', ReactPolls.renderPollManagement)

  ReactWidget.initialise('ie', 'questions', ReactQuestions.renderQuestions)
  ReactWidget.initialise('ie', 'present', ReactQuestionsPresent.renderData)

  $('.timeline-carousel__item').slick({
    initialSlide: parseInt($('#timeline-carousel').attr('data-initial-slide')),
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

  if ($.fn.select2) {
    $('.js-select2').select2()
    $('.select2__no-search').select2({
      minimumResultsForSearch: -1
    })
  }

  // This function adds required classes to iframes added by ckeditor
  $('.rich-text iframe').addClass('ck_embed_iframe')
  $('.ck_embed_iframe').parent('div').addClass('ck_embed_iframe__container')
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)

// Closes bootstrap collapse on click elsewhere
document.addEventListener('click', function () {
  $('.collapse').collapse('hide')
})

// This function is overwritten with custom behavior in embed.js.
window.adhocracy4 = {}
window.adhocracy4.getCurrentPath = function () {
  return location.pathname
}
