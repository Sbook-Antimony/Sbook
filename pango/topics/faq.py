from djamago import QA
import faqs


class Faq(QA):
    data = []
    for faq in faqs.Faq.INSTANCES:
        data.append((faq.questions, [faq.answer]))

    def format_answer(node):
        node.response = (
            f"#***Faq:** `{node.score:05.2f}%`:* `\n"
            f"##{node.params['qa_qa_question_question']}`:\n\n"
            f"{node.response}"
        )
        node.topics = ((100, "faq"), (100, "main"), (100, "markdown"))
