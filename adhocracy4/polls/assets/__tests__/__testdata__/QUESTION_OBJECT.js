export const QUESTION_OBJECT = {
  id: 1,
  label: 'My Question',
  help_text: '',
  multiple_choice: false,
  is_open: false,
  isReadOnly: false,
  authenticated: true,
  choices: [
    {
      id: 1,
      label: 'cool1',
      count: 0,
      is_other_choice: false
    },
    {
      id: 2,
      label: 'yeah',
      count: 0,
      is_other_choice: false
    }
  ],
  userChoices: [],
  answers: [],
  userAnswer: '',
  other_choice_answers: [],
  other_choice_user_answer: '',
  totalVoteCount: 0,
  totalVoteCountMulti: 0,
  totalAnswerCount: 0
}
