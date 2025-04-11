import React, { useState } from 'react'
import django from 'django'
import { SwitchButton } from '../../../static/SwitchButton'
import ConfidenceCircle, { cleanPercentage } from './confidence_circle'

const translated = {
  expandableBar: django.pgettext('defakts', 'The defakt AI has found evidence of disinformation.'),
  intro: django.pgettext('defakts', 'Defakts uses artificial intelligence to check content for disinformation based on certain linguistic characteristics.'),
  confidenceScore: django.pgettext('defakts', 'The AI is %(percentage)s% sure that this comment contains disinformation as some of its characteristics are being fulfilled.'),
  basedOn: django.pgettext('defakts', 'This estimation is based on the following words:'),
  cta: django.pgettext('defakts', 'If you want to know more about what the characteristics mean, please visit our [FAQs]. Here you will also find advice on how to respond constructively to disinformation.'),
  ariaReadMore: django.pgettext('defakts', 'Click to view the AI explanation for reporting this comment.'),
  ariaReadLess: django.pgettext('defakts', 'Click to hide the AI explanation for reporting this comment.'),
  readMore: django.pgettext('defakts', 'Read more'),
  showLess: django.pgettext('defakts', 'Show less'),
  showInfoSwitch: django.pgettext('defakts', 'Show AI info to users'),
  hideInfoSwitch: django.pgettext('defakts', 'Hide AI info from users')
}

export const AiReport = ({ report, notificationPk, toggleShowAiReport }) => {
  const [isExpanded, setIsExpanded] = useState()

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  const toggleReadMore = (
    <button
      className="btn--link text-danger strong"
      type="button"
      onClick={toggleExpand}
      aria-label={isExpanded ? translated.ariaReadLess : translated.ariaReadMore}
    >
      {isExpanded ? translated.showLess : translated.readMore}
    </button>
  )

  const extractLabelWords = (explanation) => {
    return explanation.slice(0, 3).map(word => word[0]).join(', ')
  }

  const renderExplanation = (
    <ul>
      {report.explanation.map(({ code, label, explanation }, index) => (
        <li key={code}>
          <strong>{label}:&nbsp;</strong>
          <span>{extractLabelWords(explanation)}</span>
        </li>
      ))}
    </ul>
  )

  const renderCTA = () => {
    // replace "[FAQs]" with anchor
    const [preText, placeholderText, postText] = translated.cta.split(/(\[.*?\])/)
    // remove square brackets
    const anchorText = placeholderText.replace(/\[|\]/g, '')
    return (
      <>
        {preText} <a href={report.faq_url} target="_blank" rel="noreferrer">{anchorText}</a> {postText}
      </>
    )
  }

  return (
    <div className="alert alert--danger mb-2 pb-0">
      <div className="d-flex text-start">
        <i
          className="fas fa-exclamation-circle text-danger pt-1 pe-2"
          aria-hidden="True"
        />

        {!isExpanded
          ? (
            <p className="pe-4">{translated.expandableBar} {toggleReadMore}</p>
            )
          : (
            <div className="pe-4">
              <p>{translated.expandableBar}</p>
              <p>
                <span>{translated.intro} </span>
              </p>
              <div className="d-flex">
                <ConfidenceCircle confidence={report.confidence} color="#DE4B31" defaultColor="#F6C9C2" />
                <p className="">{django.interpolate(translated.confidenceScore, { percentage: cleanPercentage(report.confidence) }, true)}</p>
              </div>
              <p className="mb-1">{translated.basedOn}</p>
              {renderExplanation}
              <p>
                {renderCTA()} {toggleReadMore}
              </p>
            </div>
            )}
      </div>
      {toggleShowAiReport &&
        <div className="d-flex text-start mt-3 mb-3">
          <SwitchButton
            id={notificationPk}
            onClickCallback={toggleShowAiReport}
            isChecked={report.show_in_discussion}
            switchLabelOn={translated.hideInfoSwitch}
            switchLabelOff={translated.showInfoSwitch}
          />
        </div>}
    </div>
  )
}

module.exports = AiReport
