import QuestionModerator from './QuestionModerator'
import QuestionUser from './QuestionUser'
import React from 'react'

const QuestionList = (props) => {
  if (props.isModerator) {
    return (
      <div>
        {
          props.questions.map((question, index) => {
            return (
              <QuestionModerator
                key={question.id}
                displayIsOnShortlist={!question.is_hidden}
                displayIsLive={!question.is_hidden}
                displayIsHidden
                displayIsAnswered={!question.is_hidden}
                removeFromList={props.removeFromList.bind(this)}
                updateQuestion={props.updateQuestion.bind(this)}
                handleLike={props.handleLike.bind(this)}
                isModerator={props.isModerator}
                hasLikingPermission={props.hasLikingPermission}
                id={question.id}
                is_answered={question.is_answered}
                is_on_shortlist={question.is_on_shortlist}
                is_live={question.is_live}
                is_hidden={question.is_hidden}
                category={question.category}
                likes={question.likes}
                togglePollingPaused={props.togglePollingPaused}
              >
                {question.text}
              </QuestionModerator>
            )
          })
        }
      </div>
    )
  } else {
    return (
      <div>
        {
          props.questions.map((question, index) => {
            return (
              <QuestionUser
                key={question.id}
                updateQuestion={props.updateQuestion.bind(this)}
                handleLike={props.handleLike.bind(this)}
                isModerator={props.isModerator}
                hasLikingPermission={props.hasLikingPermission}
                id={question.id}
                is_answered={question.is_answered}
                is_on_shortlist={question.is_on_shortlist}
                is_live={question.is_live}
                is_hidden={question.is_hidden}
                category={question.category}
                likes={question.likes}
              >
                {question.text}
              </QuestionUser>
            )
          })
        }
      </div>
    )
  }
}

export default QuestionList
