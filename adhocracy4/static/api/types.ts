export interface UrlReplaces {
  [key: string]: string | number | undefined
}

export interface CommentRatings {
  positive_ratings: number
  negative_ratings: number
  current_user_rating_value: number | null
  current_user_rating_id: number | null
}

export interface CommentUserInfo {
  is_users_own_comment: boolean
  authenticated_user_pk: number | null
  has_viewing_permission: boolean
  has_rating_permission: boolean
  has_changing_permission: boolean
  has_deleting_permission: boolean
  has_moderating_permission: boolean
  has_comment_commenting_permission: boolean
}

export interface AiReport {
  label: Array<[string, string]>
  confidence: number[]
  explanation: Record<string, Array<[string, number]>>
  faq_url?: string
  show_in_discussion?: boolean
}

export interface ModeratorFeedback {
  last_edit: string
  feedback_text: string
}

export interface Comment {
  id: number
  comment: string
  created: string
  modified: string
  user_name: string
  user_pk: number
  user_profile_url: string
  user_image: string | null
  user_image_fallback: string | null
  user_info: CommentUserInfo
  child_comments: Comment[]
  ratings: CommentRatings
  content_type: number
  comment_content_type: number
  object_pk: number
  is_deleted: boolean
  is_removed: boolean
  is_censored: boolean
  is_blocked: boolean
  is_moderator_marked: boolean
  author_is_moderator: boolean
  is_moderator?: boolean
  moderator_feedback: ModeratorFeedback | null
  comment_categories: Record<string, string>
  ai_report: AiReport | null
  displayNotification?: boolean
  replyError?: boolean
  editError?: boolean
  errorMessage?: string | undefined
}

export interface CommentListResponse {
  results: Comment[]
  next: string | null
  comment_count: number
  has_commenting_permission: boolean
  would_have_commenting_permission: boolean
  project_is_public: boolean
  use_org_terms_of_use: boolean
  user_has_agreed: boolean
  org_terms_url: string
  categories: Record<string, string>
  comment_found: boolean
  comment_parent: number
}

export interface CommentQueryParams {
  ordering?: string
  search?: string
  comment_category?: string
  commentID?: string
  categories?: boolean
  urlReplaces?: UrlReplaces
  [key: string]: unknown
}

export interface CommentPayload {
  comment?: string
  urlReplaces?: UrlReplaces
  agreed_terms_of_use?: boolean
  comment_categories?: string
}

export interface RatingResponse {
  id: number
  meta_info: {
    positive_ratings_on_same_object: number
    negative_ratings_on_same_object: number
    user_rating_on_same_object_value: number | null
  }
}

export interface PollChoice {
  id: number
  label: string
  count: number
  is_other_choice: boolean
}

export interface PollAnswer {
  id?: number
  vote_id: number
  answer: string
}

export interface PollQuestion {
  id: number
  label: string
  help_text: string
  multiple_choice: boolean
  is_open: boolean
  is_confidential: boolean
  isReadOnly: boolean
  authenticated: boolean
  image_url: string | null
  image_alt_text: string
  image_help_text: string
  image_base64?: string | null
  choices: PollChoice[]
  userChoices: number[]
  answers: PollAnswer[]
  other_choice_answers: PollAnswer[]
  other_choice_user_answer: number | string
  userAnswer: number | string
  other_choice_answer?: string | null
  open_answer?: string | null
  modified?: boolean
  totalVoteCount: number
  totalVoteCountMulti: number
  totalAnswerCount: number
}

export interface Poll {
  questions: PollQuestion[]
  allow_unregistered_users: boolean
  hide_results_until_finished: boolean
  has_user_vote: boolean
  use_org_terms_of_use: boolean
  user_has_agreed: boolean
  org_terms_url: string
}

export interface PollQuestionEdit {
  id?: number
  key?: string | number
  label: string
  help_text: string
  multiple_choice: boolean
  is_confidential: boolean
  is_open: boolean
  isReadOnly?: boolean
  authenticated?: boolean
  image_url: string | null
  image_alt_text: string
  image_help_text?: string
  image_base64?: string | null
  choices: Array<PollChoice | PollChoiceEdit>
  answers: PollAnswer[]
  userChoices?: number[]
  other_choice_answers?: PollAnswer[]
  other_choice_user_answer?: number | string | null
  userAnswer?: number | string
  other_choice_answer?: string | null
  open_answer?: string | null
  totalVoteCount?: number
  totalVoteCountMulti?: number
  totalAnswerCount?: number
  modified?: boolean
}

export interface PollChoiceEdit {
  id?: number
  key?: string | number
  label: string
  is_other_choice: boolean
}

export interface PollVotePayload {
  votes: Record<number, {
    choices: number[]
    other_choice_answer: string
    open_answer: string
  }>
  captcha: string
  urlReplaces?: UrlReplaces
  agreed_terms_of_use?: boolean
}

export interface PollEditPayload {
  questions: Array<{
    id?: number
    label: string
    help_text: string
    multiple_choice: boolean
    is_confidential: boolean
    is_open: boolean
    choices: PollChoiceEdit[]
    image_base64?: string
    image_url?: string | null
    image_alt_text?: string
    key?: number
  }>
  allow_unregistered_users: boolean
  hide_results_until_finished: boolean
}

export interface FollowState {
  enabled: boolean
}

export interface ReportPayload {
  description: string
  content_type: number | string
  object_pk: number | string
  urlReplaces?: UrlReplaces
}