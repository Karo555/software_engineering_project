import pytest
from pydantic import ValidationError

from app.config import Settings

VALID_ENV = {
    "POSTGRES_USER": "nodebook",
    "POSTGRES_PASSWORD": "pg-password",
    "POSTGRES_DB": "nodebook",
    "NEO4J_PASSWORD": "neo4j-password",
    "JWT_SECRET": "x" * 32,
}


@pytest.fixture
def env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    for key, value in VALID_ENV.items():
        monkeypatch.setenv(key, value)
    return monkeypatch


def test_loads_from_environment(env: pytest.MonkeyPatch) -> None:
    settings = Settings()
    assert settings.postgres_db == "nodebook"
    assert settings.neo4j_password.get_secret_value() == "neo4j-password"
    assert settings.llm_api_key is None


@pytest.mark.parametrize("missing", sorted(VALID_ENV))
def test_missing_required_value_fails(env: pytest.MonkeyPatch, missing: str) -> None:
    env.delenv(missing)
    with pytest.raises(ValidationError, match=missing.lower()):
        Settings()


def test_empty_value_counts_as_missing(env: pytest.MonkeyPatch) -> None:
    env.setenv("LLM_API_KEY", "")
    assert Settings().llm_api_key is None
    env.setenv("POSTGRES_PASSWORD", "")
    with pytest.raises(ValidationError, match="postgres_password"):
        Settings()


def test_short_jwt_secret_fails(env: pytest.MonkeyPatch) -> None:
    env.setenv("JWT_SECRET", "change-me")
    with pytest.raises(ValidationError, match="jwt_secret"):
        Settings()


def test_short_neo4j_password_fails(env: pytest.MonkeyPatch) -> None:
    env.setenv("NEO4J_PASSWORD", "seven77")
    with pytest.raises(ValidationError, match="neo4j_password"):
        Settings()


@pytest.mark.parametrize(
    ("change", "value"),
    [
        ("POSTGRES_DB", None),  # missing value: pydantic would print every input
        ("JWT_SECRET", "too-short-secret"),  # invalid value: pydantic would print it
    ],
)
def test_validation_errors_do_not_print_secrets(
    env: pytest.MonkeyPatch, change: str, value: str | None
) -> None:
    if value is None:
        env.delenv(change)
    else:
        env.setenv(change, value)
    with pytest.raises(ValidationError) as excinfo:
        Settings()
    message = str(excinfo.value)
    secrets = [VALID_ENV["POSTGRES_PASSWORD"], VALID_ENV["NEO4J_PASSWORD"], VALID_ENV["JWT_SECRET"]]
    for secret in [*secrets, "too-short-secret"]:
        assert secret not in message
    assert change.lower() in message  # still says which variable is wrong


def test_database_url_escapes_special_characters(env: pytest.MonkeyPatch) -> None:
    env.setenv("POSTGRES_PASSWORD", "p@ss:w/rd")
    env.setenv("POSTGRES_HOST", "postgres")
    url = Settings().database_url
    assert url == "postgresql+psycopg://nodebook:p%40ss%3Aw%2Frd@postgres:5432/nodebook"


def test_secrets_are_masked(env: pytest.MonkeyPatch) -> None:
    text = repr(Settings())
    assert "pg-password" not in text
    assert "neo4j-password" not in text
    assert "x" * 32 not in text


def test_cors_origin_list(env: pytest.MonkeyPatch) -> None:
    env.setenv("CORS_ORIGINS", "http://localhost:5173, https://nodebook.example ")
    assert Settings().cors_origin_list == ["http://localhost:5173", "https://nodebook.example"]
