let maxLocalKey = 0

export const getNextLocalKey = () => 'local_' + (maxLocalKey++)

/** Only used in tests to make generated keys deterministic. */
export const resetLocalKeys = () => {
  maxLocalKey = 0
}

export const createEmptyChoice = (isOther = false) => ({
  key: getNextLocalKey(),
  label: isOther ? 'other' : '',
  is_other_choice: isOther
})

export const createEmptyQuestion = (isOpen, multipleChoice = false) => ({
  key: getNextLocalKey(),
  label: '',
  help_text: '',
  multiple_choice: multipleChoice,
  is_open: isOpen,
  is_confidential: false,
  choices: isOpen ? [] : [createEmptyChoice(), createEmptyChoice()],
  image_base64: null,
  image_url: null,
  image_alt_text: ''
})

/**
 * Questions returned by the poll API are enriched with read-only fields
 * (userChoices, vote counts, ...). Attach stable local keys so the
 * management UI can track items (also unsaved ones) without ids.
 */
export const normalizeQuestion = (question) => ({
  ...question,
  key: question.id != null ? 'q_' + question.id : getNextLocalKey(),
  choices: (question.choices || []).map((choice) => ({
    ...choice,
    key: choice.id != null ? 'c_' + choice.id : getNextLocalKey()
  }))
})

const READ_ONLY_QUESTION_FIELDS = [
  'key',
  'answers',
  'image_url',
  'image_help_text',
  'userChoices',
  'userAnswer',
  'other_choice_answers',
  'other_choice_user_answer',
  'totalVoteCount',
  'totalVoteCountMulti',
  'totalAnswerCount',
  'isReadOnly',
  'authenticated',
  'count'
]

const READ_ONLY_CHOICE_FIELDS = ['key', 'count']

const omit = (object, fields) =>
  Object.keys(object).reduce((result, field) => {
    if (!fields.includes(field)) {
      result[field] = object[field]
    }
    return result
  }, {})

/**
 * Build the questions payload for the poll update API.
 * Read-only fields coming from the API are stripped so the request body
 * only contains what the backend serializer/service understands.
 */
export const buildQuestionsPayload = (questions) =>
  questions.map((question) => {
    const payload = omit(question, READ_ONLY_QUESTION_FIELDS)

    payload.choices = (question.choices || []).map((choice) =>
      omit(choice, READ_ONLY_CHOICE_FIELDS)
    )

    if (question.image_base64 !== undefined) {
      payload.image_base64 = question.image_base64
    }
    payload.image_alt_text = question.image_alt_text || ''
    return payload
  })

export const moveItem = (items, from, to) => {
  if (from === to || from < 0 || to < 0 || from >= items.length || to >= items.length) {
    return items
  }
  const result = [...items]
  const [moved] = result.splice(from, 1)
  result.splice(to, 0, moved)
  return result
}
