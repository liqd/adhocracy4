import React, { useState } from 'react'
import django from 'django'

import Alert from '../../../static/Alert'
import PollResults from './PollResults'

const ResultsView = ({
  results,
  totalParticipants,
  hasUserVote,
  votingEnded,
  canChangeAnswer,
  alert,
  onBackToPoll,
  onChangeAnswer,
  hideChangeButton
}) => {
  const [resultsCollapsed, setResultsCollapsed] = useState(false)

  const pollEndedStr = django.gettext('The poll has ended. Here are the results.')
  const pollCompletedStr = django.gettext('Here are the preliminary results.')

  return (
    <div className="poll__preliminary-results">
      <button
        type="button"
        className="poll__results-header"
        onClick={() => setResultsCollapsed(!resultsCollapsed)}
        aria-expanded={!resultsCollapsed}
      >
        <div className="poll__results-header-text">
          {totalParticipants > 0 && (
            <p
              className="poll__total-participants"
              dangerouslySetInnerHTML={{
                __html: django.interpolate(
                  django.ngettext(
                    '<strong>%s</strong> <strong>person</strong> has participated.',
                    '<strong>%s</strong> <strong>people</strong> have participated.',
                    totalParticipants
                  ),
                  [totalParticipants]
                )
              }}
            />
          )}
          <p className="lead poll__results-subtitle">
            {votingEnded
              ? pollEndedStr
              : pollCompletedStr}
          </p>
        </div>
        <i className={'fas fa-chevron-down' + (resultsCollapsed ? '' : ' open')} aria-hidden="true" />
      </button>

      <div className={'poll__results-content' + (resultsCollapsed ? ' poll__results-content--collapsed' : '')}>
        {results.map((question, idx) => (
          <PollResults key={'result-' + (question.id || idx)} question={question} />
        ))}

        {alert && <Alert {...alert} />}

        {!hideChangeButton && (
          <div className="poll poll__preliminary-results-buttons">
            {hasUserVote
              ? (
                <div className="text-end">
                  {!votingEnded && canChangeAnswer && (
                    <button
                      type="button"
                      className="btn btn--transparent-bordered"
                      onClick={onChangeAnswer}
                    >
                      {django.gettext('Change my answers')}
                    </button>
                  )}
                </div>
                )
              : !votingEnded && (
                <button
                  type="button"
                  className="btn poll__btn--link"
                  onClick={onBackToPoll}
                >
                  {django.gettext('To poll')}
                </button>
              )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ResultsView
