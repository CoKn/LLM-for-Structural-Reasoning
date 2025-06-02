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
        "answer": "[lowercase letter: a, b, c, or d]"
    },
    {
        "question": "[Full problem statement with all conditions and the question]",
        "question_parsing": [
            "[Extract each distinct condition/constraint as separate items]",
            "[Include the initial setup]",
            "[Include each logical rule]", 
            "[Include the specific scenario being asked about]"
        ],
        "answer": "[lowercase letter: a, b, c, or d]"
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

Generate puzzles with complete problem statements and properly parsed constraints, but do not include the reasoning steps yet.
"""

solution_generation_prompt = """
You are provided with logical reasoning puzzles that need to be solved. For each puzzle, you must generate the chain of thought reasoning and parse it into structured steps.

## Your Task:
Given puzzle questions with their constraints, provide:
1. **cot**: Step-by-step logical reasoning explaining how to reach the answer
2. **cot_parsing**: Structured breakdown of each reasoning step with verification

## Required Output Format:
For each puzzle, add the missing "cot" and "cot_parsing" fields to complete this structure:

```json
{
    "question": "[existing]",
    "question_parsing": "[existing]", 
    "answer": "[existing]",
    "cot": "[Step-by-step logical reasoning explaining how to reach the answer]",
    "cot_parsing": [
        {
            "statement": "[A specific logical step or conclusion]",
            "evidence": "[The conditions/rules that support this statement]", 
            "Verification": "[true/false - whether this reasoning step is logically sound]"
        },
        {
            "statement": "[Next logical step]",
            "evidence": "[Supporting conditions/rules]",
            "Verification": "[true/false]"
        }
    ]
}
Reasoning Requirements:

Work through each constraint systematically
Show how the given scenario triggers specific rules
Demonstrate logical deductions step by step
Verify each reasoning step is sound
Clearly justify why the answer choice is correct

CoT Parsing Guidelines:

Each statement should be a single logical step or conclusion
Evidence should reference specific conditions from the puzzle
Verification should be "true" for sound logic, "false" for flawed reasoning
Include 3-6 parsing steps depending on complexity

Please solve the provided puzzles by adding the complete reasoning components.
"""

