from django.test import TestCase

from tunobase.core import constants as core_constants
from tunobase.poll import models

class PollModelTestCase(TestCase):
    """Set up the poll model test cases."""

    question = 'Poll Model Question'
    answer = 'Answer'

    def setUp(self):
        """Create a Poll Model and 4 Answers."""

        self.poll_object = models.PollQuestion.objects.create(
            question=self.question,
        )

        for i in range(4):
            models.PollAnswer.objects.create(
                answer='%s %i' % (self.answer, i),
                poll=self.poll_object
            )

    def test_poll_model(self):
        """
        Test that the Poll Model was created with the 
        right question, state and has at least 4 Answers

        """
        poll_object = models.PollQuestion.objects.get(question=self.question)
        self.assertEqual(poll_object.question, self.question)
        self.assertEqual(poll_object.state, core_constants.STATE_PUBLISHED)
        self.assertGreaterEqual(poll_object.answers.count(), 4)

    def test_poll_answer_model(self):
        """
        Test that incrementing vote counts on the Poll Answer
        Model works as expected

        """
        poll_answer_object = models.PollAnswer.objects.get(pk=1)
        poll_answer_object.vote_count += 1
        poll_answer_object.save()
        self.assertGreaterEqual(poll_answer_object.vote_count, 1)
