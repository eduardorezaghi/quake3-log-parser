import pytest


@pytest.fixture
def mock_file(tmp_path, content):
    file_path = tmp_path / "test.log"
    file_content = content
    file_path.write_text(file_content)
    yield file_path


@pytest.fixture
def create_mock_log_file(tmp_path):
    def _create_file(content):
        file_path = tmp_path / "test.log"
        file_path.write_text(content)
        return file_path

    yield _create_file


@pytest.fixture(
    params=[
        ("tests/fixtures/qlog_shard_1.log", 5),
        ("tests/fixtures/qlog_shard_2.log", 4),
        ("tests/fixtures/qlog_shard_3.log", 4),
    ]
)
# For each test file, we expect a different number of games
def log_file_fixture(request):
    file_path, expected_game_count = request.param
    with open(file_path, "r") as f:
        content = f.read()
    yield content, expected_game_count


@pytest.fixture(
    params=[
        (
            "tests/fixtures/qlog_shard_4.log",
            {
                "<world>": 2,
                "Isgalamido": -1,
                "Assasinu Credi": -1,
                "Dono da Bola": 1,
                "Mal": -1,
                "Oootsimo": 1,
                "Zeh": -1,
            },
        ),
        (
            "tests/fixtures/qlog_shard_5.log",
            {
                "<world>": 1,
                "Dono da Bola": 2,
                "Zeh": -3,
            }
        )
    ]
)
def kill_counts_fixture(request):
    file_path, expected_kill_counts = request.param
    yield file_path, expected_kill_counts
