from src.rag_app.generation.prompt_builder import PromptBuilder


def test_prompt_includes_question_context_and_source_reference():
    prompt = PromptBuilder.build_prompt(
        "What does the document say?",
        [{"filename": "architecture.pdf", "page_number": 2, "text": "The API has three layers."}],
    )
    assert "What does the document say?" in prompt
    assert "The API has three layers." in prompt
    assert "architecture.pdf" in prompt
    assert "Page 2" in prompt


def test_empty_context_prompt_requests_missing_information_acknowledgement():
    prompt = PromptBuilder.build_prompt("Question?", [])
    assert "information is missing" in prompt
