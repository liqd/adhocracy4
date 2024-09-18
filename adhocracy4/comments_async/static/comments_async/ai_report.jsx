import React, { useState } from 'react'
import django from 'django'
import { SwitchButton } from '../../../static/SwitchButton'

const translated = {
  expandableBar: django.pgettext('defakts', 'The defakt AI has found evidence of disinformation.'),
  intro: django.pgettext('defakts', 'Defakts uses artificial intelligence to check content for disinformation based on certain linguistic characteristics.'),
  confidenceScore: django.pgettext('defakts', 'The AI considers some of the characteristics of disinformation to be fulfilled based on the following words in the comment. The probability is given in % for each characteristic.'),
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
      className="btn--link text-danger"
      type="button"
      onClick={toggleExpand}
      aria-label={isExpanded ? translated.ariaReadLess : translated.ariaReadMore}
    >
      {isExpanded ? translated.showLess : translated.readMore}
    </button>
  )

  const confidenceToPercent = (confidence) => {
    const percentFormat = new Intl.NumberFormat('default', {
      style: 'percent',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    })
    return percentFormat.format(confidence)
  }

  const extractLabelWords = (label) => {
    const words = report.explanation[label]
    return words.slice(0, 3).map(word => word[0]).join(', ')
  }

  const renderExplanation = (
    <ul>
      {report.label.map(([key, description], index) => (
        <li key={key}>
          <span>{description.charAt(0).toUpperCase() + description.slice(1)} </span>
          <span>({confidenceToPercent(report.confidence[index])}): </span>
          <span>{extractLabelWords(key)}</span>
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
                <span>{translated.confidenceScore}</span>
              </p>
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
