export const hasValidAnswer = (question, answer) => {
  if (!answer) return false

  if (question?.is_open) {
    return !!answer.open_answer && answer.open_answer.trim() !== ''
  }

  const hasChoice = !!answer.choices && answer.choices.length > 0
  const hasOtherAnswer = !!answer.other_choice_answer && answer.other_choice_answer.trim() !== ''

  if (hasChoice && question?.choices) {
    const otherChoice = question.choices.find((choice) => choice.is_other_choice)
    if (otherChoice && answer.choices.includes(otherChoice.id)) {
      return hasOtherAnswer
    }
  }

  return hasChoice || hasOtherAnswer
}

export const buildVoteData = (userAnswers) => {
  const voteData = {}
  Object.entries(userAnswers).forEach(([questionId, answer]) => {
    voteData[Number(questionId)] = {
      choices: answer.choices || [],
      other_choice_answer: answer.other_choice_answer || '',
      open_answer: answer.open_answer || ''
    }
  })
  return voteData
}

export const getAnsweredCount = (questions, userAnswers) => {
  let count = 0
  questions.forEach((question) => {
    if (hasValidAnswer(question, userAnswers[question.id])) {
      count++
    }
  })
  return count
}
