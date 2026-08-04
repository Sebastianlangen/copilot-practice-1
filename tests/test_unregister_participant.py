from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_participant_returns_404_for_unknown_participant():
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(email)}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_updates_activity_participants_list():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )
    activities_response = client.get("/activities")

    assert signup_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"]

    client.delete(f"/activities/{quote(activity_name)}/participants/{quote(email)}")
