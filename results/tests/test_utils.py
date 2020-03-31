from django.test import TestCase

from results.util import get_stores, first_team_wins, process_score
from results.constants import (
    TEST_SCORES,
    TEST_LINES,
    TEST_RESULTS,
    TEST_REQUEST_DATA,
    TEST_SCORES_RESULTS,
    THREAD_NAMES_DEFAULT,
)


class TestFunctions(TestCase):
    def setUp(self):
        self.values, self.threads_ran = get_stores(TEST_REQUEST_DATA)

    def test_first_team_wins(self):
        self.assertEqual(
            True,
            first_team_wins(TEST_SCORES['first'])
        )

    def test_second_team_wins(self):
        self.assertEqual(
            False,
            first_team_wins(TEST_SCORES['second'])
        )

    def test_first_team_wins_on_away_goals(self):
        self.assertEqual(
            True,
            first_team_wins(TEST_SCORES['third'])
        )

    def test_second_team_wins_on_away_goals(self):
        self.assertEqual(
            False,
            first_team_wins(TEST_SCORES['fourth'])
        )

    def test_process_score_first_team_wins(self):
        self.assertEqual(
            TEST_RESULTS['first'],
            process_score(TEST_LINES['first'])
        )

    def test_process_score_second_team_wins(self):
        self.assertEqual(
            TEST_RESULTS['second'],
            process_score(TEST_LINES['second'])
        )

    def test_get_scores_results(self):
        self.assertEqual(self.values, TEST_SCORES_RESULTS)

    def test_get_scores_threads_ran(self):
        thread_names_set = set([x.getName() for x in self.threads_ran])
        thread_names_default = set(THREAD_NAMES_DEFAULT)
        self.assertEqual(
            thread_names_default,
            thread_names_default & thread_names_set
        )
