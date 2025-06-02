entire_puzzle_generation_prompt = """
You are tasked with generating logical reasoning puzzles in the format of correct json. The json is a list of puzzles. Create puzzles that involve constraint satisfaction and deductive reasoning, similar to the complexity of logic games found in standardized tests.

## Puzzle Requirements:
- **Entities**: 5-8 people/objects with single-letter names (e.g., A, B, C, D...)
- **Binary Choice Scenario**: Each entity must be assigned to one of two categories/locations/groups
- **Constraints**: Include 4-6 conditional logic rules using "if-then" statements and direct assignments
- **Question**: Pose a specific scenario and ask what must be true, providing 4 multiple choice options

## Required json Structure (a list of puzzles where each item in the list is a json formated puzzle):
[
    {
        "question": "[Full problem statement with all conditions and the question]",
        "question_parsing": [
            "[Extract each distinct condition/constraint as separate items]",
            "[Include the initial setup]",
            "[Include each logical rule]",
            "[Include the specific scenario being asked about]"
        ],
        "answer": "[lowercase letter: a, b, c, or d]",
        "cot": "[Step-by-step logical reasoning explaining how to reach the answer]",
        "cot_parsing": [
            {
                "statement": "[A specific logical step or conclusion]",
                "evidence": "[The conditions/rules that support this statement]",
                "Verification": "[true/false - whether this reasoning step is logically sound]"
            }
        ]
    }, 
    {
        "question": "[Full problem statement with all conditions and the question]",
        "question_parsing": [
            "[Extract each distinct condition/constraint as separate items]",
            "[Include the initial setup]",
            "[Include each logical rule]",
            "[Include the specific scenario being asked about]"
        ],
        "answer": "[lowercase letter: a, b, c, or d]",
        "cot": "[Step-by-step logical reasoning explaining how to reach the answer]",
        "cot_parsing": [
            {
                "statement": "[A specific logical step or conclusion]",
                "evidence": "[The conditions/rules that support this statement]",
                "Verification": "[true/false - whether this reasoning step is logically sound]"
            }
        ]
    }
]

Difficulty Guidelines:

Use conditional logic (if X then Y)
Include mutual exclusions (X and Y go to different places)
Require 3-4 logical deduction steps to solve
Make the answer non-obvious but definitively derivable
Ensure exactly one correct answer among the choices

Example Topics:

Students going to different countries
People assigned to different teams/departments
Objects placed in different containers/rooms
Participants in different activities/events
"""

question_generation_prompt = """
You are tasked with generating logical reasoning puzzles that involve constraint satisfaction and deductive reasoning, similar to the complexity of logic games found in standardized tests.

## Puzzle Requirements:
- **Entities**: 5-8 people/objects with single-letter names (e.g., A, B, C, D...)
- **Binary Choice Scenario**: Each entity must be assigned to one of two categories/locations/groups
- **Constraints**: Include 4-6 conditional logic rules using "if-then" statements and direct assignments
- **Question**: Pose a specific scenario and ask what must be true, providing 4 multiple choice options

## Required JSON Structure:
[
    {
        "question": "[Full problem statement with all conditions and the question]",
        "question_parsing": [
            "[Extract each distinct condition/constraint as separate items]",
            "[Include the initial setup]", 
            "[Include each logical rule]",
            "[Include the specific scenario being asked about]"
        ],
    },
    {
        "question": "[Full problem statement with all conditions and the question]",
        "question_parsing": [
            "[Extract each distinct condition/constraint as separate items]",
            "[Include the initial setup]",
            "[Include each logical rule]", 
            "[Include the specific scenario being asked about]"
        ],
    }
]

## Difficulty Guidelines:
- Use conditional logic (if X then Y)
- Include mutual exclusions (X and Y go to different places)
- Require 3-4 logical deduction steps to solve
- Make the answer non-obvious but definitively derivable
- Ensure exactly one correct answer among the choices

## Example Topics:
- Students going to different countries
- People assigned to different teams/departments
- Objects placed in different containers/rooms
- Participants in different activities/events

Generate puzzles with complete problem statements and properly parsed constraints, but do not include the reasoning steps. Also do not answer the question.
"""

solution_generation_prompt = """
You are provided with a list of logical reasoning puzzles that need to be solved. You must generate the chain of thought reasoning and parse it into structured steps for EVERY SINGLE PUZZLE in the provided list.

## Your Task:
Given a list of puzzle questions with their constraints, you must:
1. Process EACH puzzle in the input list
2. Add the missing "cot" and "cot_parsing" fields to EVERY puzzle
3. Return the complete list with all puzzles solved

## Critical Instructions:
- SOLVE ALL PUZZLES provided in the input list
- Maintain the exact same list structure 
- Do not skip any puzzles
- Preserve all existing fields (question, question_parsing, id, sel_idx, answer)

## Required Output Format:
Return the complete JSON list with all puzzles solved:

```json
[
    {
        "question": "[from input]",
        "question_parsing": "[from input]",
        "id": "[from input]", 
        "sel_idx": "[from input]", 
        "answer": "[from input]",
        "cot": "[NEW: Step-by-step logical reasoning explaining how to reach the answer]",
        "cot_parsing": [
            {
                "statement": "[A specific logical step or conclusion]",
                "evidence": "[The conditions/rules that support this statement]", 
                "Verification": "[true/false - whether this reasoning step is logically sound]"
            }
        ]
    },
    {
        "question": "[from input - SECOND PUZZLE]",
        "question_parsing": "[from input - SECOND PUZZLE]",
        "id": "[from input - SECOND PUZZLE]", 
        "sel_idx": "[from input - SECOND PUZZLE]", 
        "answer": "[from input - SECOND PUZZLE]",
        "cot": "[NEW: Step-by-step reasoning for SECOND PUZZLE]",
        "cot_parsing": [
            {
                "statement": "[Logical step for SECOND PUZZLE]",
                "evidence": "[Supporting conditions for SECOND PUZZLE]", 
                "Verification": "[true/false]"
            }
        ]
    }
]
Reasoning Requirements:

Work through each constraint systematically for EACH puzzle
Show how the given scenario triggers specific rules
Demonstrate logical deductions step by step
Verify each reasoning step is sound
Clearly justify why the answer choice is correct

CoT Parsing Guidelines:

Each statement should be a single logical step or conclusion
Evidence should reference specific conditions from the puzzle
Verification should be "true" for sound logic, "false" for flawed reasoning
Include 3-6 parsing steps depending on complexity

IMPORTANT: Process every puzzle in the input list. Your output must contain the same number of solved puzzles as provided in the input.
"""
