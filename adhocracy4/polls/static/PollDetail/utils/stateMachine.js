// State machine states
export const STATES = {
  LOADING: 'loading',
  START_SCREEN: 'start_screen',
  ANSWERING: 'answering',
  SUBMITTING: 'submitting',
  RESULTS: 'results',
  ERROR: 'error'
}

// Action types
export const ACTIONS = {
  // Data loading
  DATA_LOADED: 'DATA_LOADED',
  DATA_ERROR: 'DATA_ERROR',

  // Navigation
  START_POLL: 'START_POLL',
  NEXT_QUESTION: 'NEXT_QUESTION',
  PREV_QUESTION: 'PREV_QUESTION',
  SKIP_QUESTION: 'SKIP_QUESTION',

  // Answer management
  UPDATE_ANSWER: 'UPDATE_ANSWER',

  // Submission
  SUBMIT_START: 'SUBMIT_START',
  SUBMIT_SUCCESS: 'SUBMIT_SUCCESS',
  SUBMIT_ERROR: 'SUBMIT_ERROR',

  // UI
  SET_ALERT: 'SET_ALERT',
  CLEAR_ALERT: 'CLEAR_ALERT',
  SET_CHECKED_TERMS: 'SET_CHECKED_TERMS',
  SET_CAPTCHA: 'SET_CAPTCHA',

  // Results navigation
  BACK_TO_POLL: 'BACK_TO_POLL',
  CHANGE_ANSWER: 'CHANGE_ANSWER',
  SHOW_RESULTS: 'SHOW_RESULTS'
}

// Helper to check if transition is valid
export const isValidTransition = (currentState, actionType) => {
  const validTransitions = {
    [STATES.LOADING]: [ACTIONS.DATA_LOADED, ACTIONS.DATA_ERROR],
    [STATES.START_SCREEN]: [ACTIONS.START_POLL, ACTIONS.SHOW_RESULTS],
    [STATES.ANSWERING]: [
      ACTIONS.NEXT_QUESTION,
      ACTIONS.PREV_QUESTION,
      ACTIONS.SKIP_QUESTION,
      ACTIONS.SUBMIT_START,
      ACTIONS.SET_ALERT,
      ACTIONS.CLEAR_ALERT,
      ACTIONS.UPDATE_ANSWER,
      ACTIONS.SET_CHECKED_TERMS,
      ACTIONS.SET_CAPTCHA
    ],
    [STATES.SUBMITTING]: [ACTIONS.SUBMIT_SUCCESS, ACTIONS.SUBMIT_ERROR],
    [STATES.RESULTS]: [ACTIONS.BACK_TO_POLL, ACTIONS.CHANGE_ANSWER],
    [STATES.ERROR]: []
  }

  return validTransitions[currentState]?.includes(actionType) || false
}
