export const QUESTION_OBJECT = {
  id: 6,
  label: 'Pick multiple options',
  help_text: '',
  multiple_choice: true,
  is_open: false,
  isReadOnly: false,
  authenticated: true,
  image_url: null,
  image_alt_text: '',
  image_help_text: 'The image will be shown with the question. It must be min. 1500 pixel wide and 500 pixel tall. Allowed file formats are jpeg, png, webp. The file size should be max. 10 MB.',
  choices: [
    {
      id: 1,
      label: 'Answer 1',
      count: 0,
      is_other_choice: false
    },
    {
      id: 2,
      label: 'Answer 2',
      count: 0,
      is_other_choice: false
    },
    {
      id: 3,
      label: 'Answer 3',
      count: 0,
      is_other_choice: false
    },
    {
      id: 4,
      label: 'other',
      count: 1,
      is_other_choice: true
    }
  ],
  userChoices: [4],
  answers: [],
  userAnswer: '',
  other_choice_answers: [
    {
      vote_id: 28,
      answer: 'question text'
    }
  ],
  other_choice_user_answer: 28,
  totalVoteCount: 1,
  totalVoteCountMulti: 1,
  totalAnswerCount: 0
}
