# -*- coding: utf-8 -*-
"""
Tests of extended hints
"""


import unittest

from ddt import ddt, data, unpack

# With the use of ddt, some of the data expected_string cases below are naturally long stretches
# of text text without whitespace. I think it's best to leave such lines intact
# in the test code. Therefore:
# pylint: disable=line-too-long
# For out many ddt data cases, prefer a compact form of { .. }
# pylint: disable=bad-continuation

from . import new_loncapa_problem, load_fixture


class HintTest(unittest.TestCase):
    """Base class for tests of extended hinting functionality."""

    def correctness(self, problem_id, choice):
        """Grades the problem and returns the 'correctness' string from cmap."""
        student_answers = {problem_id: choice}
        cmap = self.problem.grade_answers(answers=student_answers)    # pylint: disable=no-member
        return cmap[problem_id]['correctness']

    def get_hint(self, problem_id, choice):
        """Grades the problem and returns its hint from cmap or the empty string."""
        student_answers = {problem_id: choice}
        cmap = self.problem.grade_answers(answers=student_answers)    # pylint: disable=no-member
        adict = cmap.cmap.get(problem_id)
        if adict:
            return adict['msg']
        else:
            return ''


# It is a little surprising how much more complicated TextInput is than all the other cases.
@ddt
class TextInputHintsTest(HintTest):
    """
    Test Text Input Hints Test
    """
    xml = load_fixture('extended_hints_text_input.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_2_1', u'choice': u'GermanyΩ',
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: I do not think so.Ω</div>'},
        {'problem_id': u'1_2_1', u'choice': u'franceΩ',
         'expected_string': u'<div class="feedback_hint_correct">Correct: Viva la France!Ω</div>'},
        {'problem_id': u'1_2_1', u'choice': u'FranceΩ',
         'expected_string': u'<div class="feedback_hint_correct">Correct: Viva la France!Ω</div>'},
        {'problem_id': u'1_2_1', u'choice': u'Mexico',
         'expected_string': ''},
        {'problem_id': u'1_2_1', u'choice': u'USAΩ',
         'expected_string': u'<div class="feedback_hint_correct">Correct: Less well known, but yes, there is a Paris, Texas.Ω</div>'},
        {'problem_id': u'1_2_1', u'choice': u'usaΩ',
         'expected_string': u'<div class="feedback_hint_correct">Correct: Less well known, but yes, there is a Paris, Texas.Ω</div>'},
        {'problem_id': u'1_2_1', u'choice': u'uSAxΩ',
         'expected_string': u''},
        {'problem_id': u'1_2_1', u'choice': u'NICKLANDΩ',
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: The country name does not end in LANDΩ</div>'},
        {'problem_id': u'1_3_1', u'choice': u'Blue',
         'expected_string': u'<div class="feedback_hint_correct">Correct: The red light is scattered by water molecules leaving only blue light.</div>'},
        {'problem_id': u'1_3_1', u'choice': u'blue',
         'expected_string': u''},
        {'problem_id': u'1_3_1', u'choice': u'b',
         'expected_string': u''},
    )
    @unpack
    def test_text_input_hints(self, problem_id, choice, expected_string):
        hint = self.get_hint(problem_id, choice)
        self.assertEqual(hint, expected_string)


@ddt
class TextInputExtendedHintsCaseInsensitive(HintTest):
    """Test Text Input Extended hints Case Insensitive"""
    xml = load_fixture('extended_hints_text_input.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_5_1', 'choice': 'abc', 'expected_string': ''},  # wrong answer yielding no hint
        {'problem_id': u'1_5_1', 'choice': 'A', 'expected_string': u'<div class="feedback_hint_correct">Woo Hoo: hint1</div>'},
        {'problem_id': u'1_5_1', 'choice': 'a', 'expected_string': u'<div class="feedback_hint_correct">Woo Hoo: hint1</div>'},
        {'problem_id': u'1_5_1', 'choice': 'B', 'expected_string': u'<div class="feedback_hint_correct">hint2</div>'},
        {'problem_id': u'1_5_1', 'choice': 'b', 'expected_string': u'<div class="feedback_hint_correct">hint2</div>'},
        {'problem_id': u'1_5_1', 'choice': 'C', 'expected_string': u'<div class="feedback_hint_incorrect">hint4</div>'},
        {'problem_id': u'1_5_1', 'choice': 'c', 'expected_string': u'<div class="feedback_hint_incorrect">hint4</div>'},
        # regexp cases
        {'problem_id': u'1_5_1', 'choice': 'FGGG', 'expected_string': u'<div class="feedback_hint_incorrect">hint6</div>'},
        {'problem_id': u'1_5_1', 'choice': 'fgG', 'expected_string': u'<div class="feedback_hint_incorrect">hint6</div>'},
    )
    @unpack
    def test_text_input_hints(self, problem_id, choice, expected_string):
        hint = self.get_hint(problem_id, choice)
        self.assertEqual(hint, expected_string)


@ddt
class TextInputExtendedHintsCaseSensitive(HintTest):
    """Sometimes the semantics can be encoded in the class name."""
    xml = load_fixture('extended_hints_text_input.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_6_1', 'choice': 'abc', 'expected_string': ''},
        {'problem_id': u'1_6_1', 'choice': 'A', 'expected_string': u'<div class="feedback_hint_correct">Correct: hint1</div>'},
        {'problem_id': u'1_6_1', 'choice': 'a', 'expected_string': u''},
        {'problem_id': u'1_6_1', 'choice': 'B', 'expected_string': u'<div class="feedback_hint_correct">Correct: hint2</div>'},
        {'problem_id': u'1_6_1', 'choice': 'b', 'expected_string': u''},
        {'problem_id': u'1_6_1', 'choice': 'C', 'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: hint4</div>'},
        {'problem_id': u'1_6_1', 'choice': 'c', 'expected_string': u''},
        # regexp cases
        {'problem_id': u'1_6_1', 'choice': 'FGG', 'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: hint6</div>'},
        {'problem_id': u'1_6_1', 'choice': 'fgG', 'expected_string': u''},
    )
    @unpack
    def test_text_input_hints(self, problem_id, choice, expected_string):
        message_text = self.get_hint(problem_id, choice)
        self.assertEqual(message_text, expected_string)


@ddt
class TextInputExtendedHintsCompatible(HintTest):
    """
    Compatibility test with mixed old and new style additional_answer tags.
    """
    xml = load_fixture('extended_hints_text_input.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_7_1', 'choice': 'A', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint1</div>'},
        {'problem_id': u'1_7_1', 'choice': 'B', 'correct': 'correct', 'expected_string': ''},
        {'problem_id': u'1_7_1', 'choice': 'C', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint2</div>'},
        {'problem_id': u'1_7_1', 'choice': 'D', 'correct': 'incorrect', 'expected_string': ''},
        # check going through conversion with difficult chars
        {'problem_id': u'1_7_1', 'choice': """<&"'>""", 'correct': 'correct', 'expected_string': ''},
    )
    @unpack
    def test_text_input_hints(self, problem_id, choice, correct, expected_string):
        message_text = self.get_hint(problem_id, choice)
        self.assertEqual(message_text, expected_string)
        self.assertEqual(self.correctness(problem_id, choice), correct)


@ddt
class TextInputExtendedHintsRegex(HintTest):
    """
    Extended hints where the answer is regex mode.
    """
    xml = load_fixture('extended_hints_text_input.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_8_1', 'choice': 'ABwrong', 'correct': 'incorrect', 'expected_string': ''},
        {'problem_id': u'1_8_1', 'choice': 'ABC', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint1</div>'},
        {'problem_id': u'1_8_1', 'choice': 'ABBBBC', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint1</div>'},
        {'problem_id': u'1_8_1', 'choice': 'aBc', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint1</div>'},
        {'problem_id': u'1_8_1', 'choice': 'BBBB', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint2</div>'},
        {'problem_id': u'1_8_1', 'choice': 'bbb', 'correct': 'correct',
         'expected_string': '<div class="feedback_hint_correct">Correct: hint2</div>'},
        {'problem_id': u'1_8_1', 'choice': 'C', 'correct': 'incorrect',
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: hint4</div>'},
        {'problem_id': u'1_8_1', 'choice': 'c', 'correct': 'incorrect',
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: hint4</div>'},
        {'problem_id': u'1_8_1', 'choice': 'D', 'correct': 'incorrect',
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: hint6</div>'},
        {'problem_id': u'1_8_1', 'choice': 'd', 'correct': 'incorrect',
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: hint6</div>'},
    )
    @unpack
    def test_text_input_hints(self, problem_id, choice, correct, expected_string):
        message_text = self.get_hint(problem_id, choice)
        self.assertEqual(message_text, expected_string)
        self.assertEqual(self.correctness(problem_id, choice), correct)


@ddt
class NumericInputHintsTest(HintTest):
    """
    This class consists of a suite of test cases to be run on the numeric input problem represented by the XML below.
    """
    xml = load_fixture('extended_hints_numeric_input.xml')
    problem = new_loncapa_problem(xml)          # this problem is properly constructed

    @data(
        {'problem_id': u'1_2_1', 'choice': '1.141',
         'expected_string': u'<div class="feedback_hint_correct">Nice: The square root of two turns up in the strangest places.</div>'},
        {'problem_id': u'1_3_1', 'choice': '4',
         'expected_string': u'<div class="feedback_hint_correct">Correct: Pretty easy, uh?.</div>'},
        # should get hint, when correct via numeric-tolerance
        {'problem_id': u'1_2_1', 'choice': '1.15',
         'expected_string': u'<div class="feedback_hint_correct">Nice: The square root of two turns up in the strangest places.</div>'},
        # when they answer wrong, nothing
        {'problem_id': u'1_2_1', 'choice': '2', 'expected_string': ''},

    )
    @unpack
    def test_numeric_input_hints(self, problem_id, choice, expected_string):
        hint = self.get_hint(problem_id, choice)
        self.assertEqual(hint, expected_string)


@ddt
class CheckboxHintsTest(HintTest):
    """
    This class consists of a suite of test cases to be run on the checkbox problem represented by the XML below.
    """
    xml = load_fixture('extended_hints_checkbox.xml')
    problem = new_loncapa_problem(xml)          # this problem is properly constructed

    @data(
        {'problem_id': u'1_2_1', 'choice': [u'choice_0'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">You are right that apple is a fruit.</div><div class="feedback_hint_text">You are right that mushrooms are not fruit</div><div class="feedback_hint_text">Remember that grape is also a fruit.</div><div class="feedback_hint_text">What is a camero anyway?</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_1'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">Remember that apple is also a fruit.</div><div class="feedback_hint_text">Mushroom is a fungus, not a fruit.</div><div class="feedback_hint_text">Remember that grape is also a fruit.</div><div class="feedback_hint_text">What is a camero anyway?</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_2'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">Remember that apple is also a fruit.</div><div class="feedback_hint_text">You are right that mushrooms are not fruit</div><div class="feedback_hint_text">You are right that grape is a fruit</div><div class="feedback_hint_text">What is a camero anyway?</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_3'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">Remember that apple is also a fruit.</div><div class="feedback_hint_text">You are right that mushrooms are not fruit</div><div class="feedback_hint_text">Remember that grape is also a fruit.</div><div class="feedback_hint_text">What is a camero anyway?</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_4'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">Remember that apple is also a fruit.</div><div class="feedback_hint_text">You are right that mushrooms are not fruit</div><div class="feedback_hint_text">Remember that grape is also a fruit.</div><div class="feedback_hint_text">I do not know what a Camero is but it is not a fruit.</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_0', u'choice_1'],
         'expected_string': u'<div class="feedback_hint_incorrect">Almost right: <div class="feedback_hint_text">You are right that apple is a fruit, but there is one you are missing. Also, mushroom is not a fruit.</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_1', u'choice_2'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">You are right that grape is a fruit, but there is one you are missing. Also, mushroom is not a fruit.</div></div>'},
        {'problem_id': u'1_2_1', 'choice': [u'choice_0', u'choice_2'],
         'expected_string': u'<div class="feedback_hint_correct">Correct: <div class="feedback_hint_text">You are right that apple is a fruit.</div><div class="feedback_hint_text">You are right that mushrooms are not fruit</div><div class="feedback_hint_text">You are right that grape is a fruit</div><div class="feedback_hint_text">What is a camero anyway?</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_0'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">No, sorry, a banana is a fruit.</div><div class="feedback_hint_text">You are right that mushrooms are not vegatbles</div><div class="feedback_hint_text">Brussel sprout is the only vegetable in this list.</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_1'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">poor banana.</div><div class="feedback_hint_text">You are right that mushrooms are not vegatbles</div><div class="feedback_hint_text">Brussel sprout is the only vegetable in this list.</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_2'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">poor banana.</div><div class="feedback_hint_text">Mushroom is a fungus, not a vegetable.</div><div class="feedback_hint_text">Brussel sprout is the only vegetable in this list.</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_3'],
         'expected_string': u'<div class="feedback_hint_correct">Correct: <div class="feedback_hint_text">poor banana.</div><div class="feedback_hint_text">You are right that mushrooms are not vegatbles</div><div class="feedback_hint_text">Brussel sprouts are vegetables.</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_0', u'choice_1'],
         'expected_string': u'<div class="feedback_hint_incorrect">Very funny: <div class="feedback_hint_text">Making a banana split?</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_1', u'choice_2'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">poor banana.</div><div class="feedback_hint_text">Mushroom is a fungus, not a vegetable.</div><div class="feedback_hint_text">Brussel sprout is the only vegetable in this list.</div></div>'},
        {'problem_id': u'1_3_1', 'choice': [u'choice_0', u'choice_2'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">No, sorry, a banana is a fruit.</div><div class="feedback_hint_text">Mushroom is a fungus, not a vegetable.</div><div class="feedback_hint_text">Brussel sprout is the only vegetable in this list.</div></div>'},

        # check for interaction between compoundhint and correct/incorrect
        {'problem_id': u'1_4_1', 'choice': [u'choice_0', u'choice_1'],
         'expected_string': u'<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">AB</div></div>'},
        {'problem_id': u'1_4_1', 'choice': [u'choice_0', u'choice_2'],
         'expected_string': u'<div class="feedback_hint_correct">Correct: <div class="feedback_hint_text">AC</div></div>'},

        # check for labeling where multiple child hints have labels
        # These are some tricky cases
        {'problem_id': '1_5_1', 'choice': ['choice_0', 'choice_1'],
         'expected_string': '<div class="feedback_hint_correct">AA: <div class="feedback_hint_text">aa</div></div>'},
        {'problem_id': '1_5_1', 'choice': ['choice_0'],
         'expected_string': '<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">aa</div><div class="feedback_hint_text">bb</div></div>'},
        {'problem_id': '1_5_1', 'choice': ['choice_1'],
         'expected_string': ''},
        {'problem_id': '1_5_1', 'choice': [],
         'expected_string': '<div class="feedback_hint_incorrect">BB: <div class="feedback_hint_text">bb</div></div>'},

        {'problem_id': '1_6_1', 'choice': ['choice_0'],
         'expected_string': '<div class="feedback_hint_incorrect"><div class="feedback_hint_text">aa</div></div>'},
        {'problem_id': '1_6_1', 'choice': ['choice_0', 'choice_1'],
         'expected_string': '<div class="feedback_hint_correct"><div class="feedback_hint_text">compoundo</div></div>'},

        # The user selects *nothing*, but can still get "unselected" feedback
        {'problem_id': '1_7_1', 'choice': [],
         'expected_string': '<div class="feedback_hint_incorrect">Incorrect: <div class="feedback_hint_text">bb</div></div>'},
        # 100% not match of sel/unsel feedback
        {'problem_id': '1_7_1', 'choice': ['choice_1'],
         'expected_string': ''},
        # Here we have the correct combination, and that makes feedback too
        {'problem_id': '1_7_1', 'choice': ['choice_0'],
         'expected_string': '<div class="feedback_hint_correct">Correct: <div class="feedback_hint_text">aa</div><div class="feedback_hint_text">bb</div></div>'},
    )
    @unpack
    def test_checkbox_hints(self, problem_id, choice, expected_string):
        hint = self.get_hint(problem_id, choice)
        self.assertEqual(hint, expected_string)


@ddt
class MultpleChoiceHintsTest(HintTest):
    """
    This class consists of a suite of test cases to be run on the multiple choice problem represented by the XML below.
    """
    xml = load_fixture('extended_hints_multiple_choice.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_2_1', 'choice': u'choice_0',
         'expected_string': '<div class="feedback_hint_incorrect">Mushroom is a fungus, not a fruit.</div>'},
        {'problem_id': u'1_2_1', 'choice': u'choice_1',
         'expected_string': ''},
        {'problem_id': u'1_3_1', 'choice': u'choice_1',
         'expected_string': '<div class="feedback_hint_correct">Correct: Potato is a root vegetable.</div>'},
        {'problem_id': u'1_2_1', 'choice': u'choice_2',
         'expected_string': '<div class="feedback_hint_correct">OUTSTANDING: Apple is indeed a fruit.</div>'},
        {'problem_id': u'1_3_1', 'choice': u'choice_2',
         'expected_string': '<div class="feedback_hint_incorrect">OOPS: Apple is a fruit.</div>'},
        {'problem_id': u'1_3_1', 'choice': u'choice_9',
         'expected_string': ''},
    )
    @unpack
    def test_multiplechoice_hints(self, problem_id, choice, expected_string):
        hint = self.get_hint(problem_id, choice)
        self.assertEqual(hint, expected_string)


@ddt
class DropdownHintsTest(HintTest):
    """
    This class consists of a suite of test cases to be run on the drop down problem represented by the XML below.
    """
    xml = load_fixture('extended_hints_dropdown.xml')
    problem = new_loncapa_problem(xml)

    @data(
        {'problem_id': u'1_2_1', 'choice': 'Multiple Choice',
         'expected_string': '<div class="feedback_hint_correct">Good Job: Yes, multiple choice is the right answer.</div>'},
        {'problem_id': u'1_2_1', 'choice': 'Text Input',
         'expected_string': '<div class="feedback_hint_incorrect">Incorrect: No, text input problems do not present options.</div>'},
        {'problem_id': u'1_2_1', 'choice': 'Numerical Input',
         'expected_string': '<div class="feedback_hint_incorrect">Incorrect: No, numerical input problems do not present options.</div>'},
        {'problem_id': u'1_3_1', 'choice': 'FACES',
         'expected_string': '<div class="feedback_hint_correct">Correct: With lots of makeup, doncha know?</div>'},
        {'problem_id': u'1_3_1', 'choice': 'dogs',
         'expected_string': '<div class="feedback_hint_incorrect">NOPE: Not dogs, not cats, not toads</div>'},
        {'problem_id': u'1_3_1', 'choice': 'wrongo',
         'expected_string': ''},

        # Regression case where feedback includes answer substring
        {'problem_id': u'1_4_1', 'choice': 'AAA',
         'expected_string': '<div class="feedback_hint_incorrect">Incorrect: AAABBB1</div>'},
        {'problem_id': u'1_4_1', 'choice': 'BBB',
         'expected_string': '<div class="feedback_hint_correct">Correct: AAABBB2</div>'},
        {'problem_id': u'1_4_1', 'choice': 'not going to match',
         'expected_string': ''},
    )
    @unpack
    def test_dropdown_hints(self, problem_id, choice, expected_string):
        hint = self.get_hint(problem_id, choice)
        self.assertEqual(hint, expected_string)


class ErrorConditionsTest(HintTest):
    """
    Erroneous xml should raise exception.
    """
    def test_error_conditions_illegal_element(self):
        xml_with_errors = load_fixture('extended_hints_with_errors.xml')
        with self.assertRaises(Exception):
            new_loncapa_problem(xml_with_errors)    # this problem is improperly constructed
