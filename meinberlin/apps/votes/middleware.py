import datetime


class VotingTokenSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "token_expire_date" in request.session:
            if (
                request.session["token_expire_date"]
                <= datetime.datetime.now().timestamp()
            ):
                del request.session["token_expire_date"]
                del request.session["voting_tokens"]
        response = self.get_response(request)
        return response
