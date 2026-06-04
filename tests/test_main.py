import pytest
import httpx
from app.base.untility import settings

@pytest.mark.asyncio
async def test_smartquiz_user_flow():
    # We use a single AsyncClient instance to maintain headers/session settings if needed
    async with httpx.AsyncClient(base_url=settings.TEST_BASE_URL) as client:
        
        # -------------------------------------------------------------------------
        # 1. TEST LIST ENDPOINTS (Category, Quiz, Question, Answer)
        # -------------------------------------------------------------------------
        
        # Category list
        cat_resp = await client.get("/smartquizs/category/lists", params={"page": 1, "page_size": 5})
        assert cat_resp.status_code == 200, f"List categories failed: {cat_resp.text}"
        print(f"Categories sample: {cat_resp.json()}")

        # Quiz list
        quiz_resp = await client.get("/smartquizs/quizs/lists", params={"page": 1, "page_size": 5})
        assert quiz_resp.status_code == 200, f"List quizzes failed: {quiz_resp.text}"
        print(f"Quizzes sample: {quiz_resp.json()}")

        # Question list
        question_resp = await client.get("/smartquizs/question/lists", params={"page": 1, "page_size": 5})
        assert question_resp.status_code == 200, f"List questions failed: {question_resp.text}"

        # Answer list
        answer_resp = await client.get("/smartquizs/answers/lists", params={"page": 1, "page_size": 5})
        assert answer_resp.status_code == 200, f"List answers failed: {answer_resp.text}"


        # -------------------------------------------------------------------------
        # 2. TEST QUIZ ATTEMPT (Create & View My Attempts)
        # -------------------------------------------------------------------------
        
        # Since your endpoints use `.as_form` (Form data instead of JSON payload), 
        # we must pass data using the `data=` parameter rather than `json=`.
        attempt_payload = {
            "quiz_id": 1, # Replace with a valid quiz_id present in your test database
            "score": 0,
            "status": "started"
        }
        
        create_attempt_resp = await client.post(
            "/smartquizs/quiz_attempt/create", 
            data=attempt_payload
        )
        assert create_attempt_resp.status_code == 200, f"Create quiz attempt failed: {create_attempt_resp.text}"
        
        attempt_data = create_attempt_resp.json().get("data", {})
        quiz_attempt_id = attempt_data.get("id")
        print(f"Created Quiz Attempt ID: {quiz_attempt_id}")

        # Fetch my attempts
        my_attempts_resp = await client.get("/smartquizs/quiz_attempt/my-attempts", params={"page": 1, "page_size": 10})
        assert my_attempts_resp.status_code == 200, f"Fetch my attempts failed: {my_attempts_resp.text}"
        print(f"My attempts list: {my_attempts_resp.json()}")


        # -------------------------------------------------------------------------
        # 3. TEST QUIZ ATTEMPT ANSWER (Create & View My Answers)
        # -------------------------------------------------------------------------
        
        # Also using `data=` here because of .as_form implementation
        attempt_answer_payload = {
            "quiz_attempt_id": quiz_attempt_id, # Link dynamically to the attempt we just created above
            "question_id": 1,
            "answer_id": 1,
            "is_correct": True
        }

        create_ans_resp = await client.post(
            "/smartquizs/quiz_attempt_answer/create",
            data=attempt_answer_payload
        )
        assert create_ans_resp.status_code == 200, f"Create attempt answer failed: {create_ans_resp.text}"
        print(f"Created Attempt Answer details: {create_ans_resp.json()}")

        # Fetch my answers filtered by the specific quiz_attempt_id
        my_answers_resp = await client.get(
            "/smartquizs/quiz_attempt_answer/my-answers", 
            params={"quiz_attempt_id": quiz_attempt_id}
        )
        assert my_answers_resp.status_code == 200, f"Fetch my answers failed: {my_answers_resp.text}"
        print(f"My answers list for attempt {quiz_attempt_id}: {my_answers_resp.json()}")