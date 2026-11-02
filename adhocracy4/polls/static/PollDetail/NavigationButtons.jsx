import React from 'react'
import django from 'django'

const NavigationButtons = ({
  currentIndex,
  isLastQuestion,
  isLoading,
  isSubmitDisabled,
  onBack,
  onSkip,
  onNext,
  onSubmit
}) => {
  return (
    <div className="poll-navigation-buttons">
      <div>
        <button
          type="button"
          className="btn btn--transparent-bordered"
          onClick={onBack}
          disabled={currentIndex === 0}
        >
          {django.gettext('Go Back')}
        </button>
      </div>
      <div>
        {!isLastQuestion
          ? (
            <>
              <button
                type="button"
                className="btn btn--transparent"
                onClick={onSkip}
              >
                {django.gettext('Skip')}
              </button>
              <button
                type="button"
                className="btn poll__btn--dark"
                onClick={onNext}
              >
                {django.gettext('Next')}
              </button>
            </>
            )
          : (
            <button
              type="button"
              className="btn poll__btn--dark"
              onClick={onSubmit}
              disabled={isLoading || isSubmitDisabled}
            >
              {isLoading ? django.gettext('Submitting...') : django.gettext('Submit All')}
            </button>
            )}
      </div>
    </div>
  )
}

export default NavigationButtons
