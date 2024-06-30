from djamago import Expression


question = lambda re: (
    fr"(?:.*(?:please|question.?)? ?{re}\??)"
    fr"|(?:may )?i ask you {re}\??"
)

Expression.register("R", [
    (100, r"(.*)"),
])
Expression.register("whois", [
    (100, r"(?:who is) (.*)"),
    (30, r"(?:do you know) (.*)"),
])
Expression.register("whatis", [
    (100, r"(?:what is) (.*)"),
    (50, r"(?:tell me.? ?(?:djamago)? what is) (.*)"),
])
Expression.register("greetings", [
    (100, r"hello"),
    (100, r"good (?:morning|evening|night|after-?noon)"),
    (70, r"greetings"),
    (20, r"good day"),
])
Expression.register("callyou", [
    (100, question(r"how do you call yourself")),
    (100, fr"(?:tell me.? ?(?:djamago)? what is) (.*)"),
    (100, question(r"what is your name")),
    (100, question(r"how can I call you")),
])
Expression.register("askingMyname", [
    (100, question(
        r"(?:how can (?:i|we) call you|what is your name|who are you|"
        r"how (?:do you|can you|are)? (?:call you|called))"
    )),
])
Expression.register("username", [
    (100, question(r"(?:do you (?:know|remember))?(?: ?what is)? ?my name")),
])
Expression.register("whoMadeMe", [
    (100, question(r"who (?:created|programmed|made|coded|trained) you")),
])
Expression.register("name", [
    (100, r"[\w\d_\- \@]+"),
])

Expression.register("aboutAUser", [
    (50,
        question(
            r"(?:do you know(?: about)?|who is|tell me about"
            r"|are you familiar with) ([\w\-_]+)"
        )
    )
])
