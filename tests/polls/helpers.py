def setup_poll(poll, question, choice, vote):
    question.poll = poll
    choice.poll = poll
    vote.choice = choice
