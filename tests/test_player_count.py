import pytest

from src.parser import QuakeLogParser


@pytest.fixture
def mock_file(tmp_path):
    file_path = tmp_path / "test.log"
    file_content = r"""
0:00 ------------------------------------------------------------
0:00 InitGame: \sv_floodProtect\1\sv_maxPing\0\sv_minPing\0\sv_maxRate\10000\sv_minRate\0\sv_hostname\Code Miner Server\g_gametype\0\sv_privateClients\2\sv_maxclients\16\sv_allowDownload\0\dmflags\0\fraglimit\20\timelimit\15\g_maxGameClients\0\capturelimit\8\version\ioq3 1.36 linux-x86_64 Apr 12 2009\protocol\68\mapname\q3dm17\gamename\baseq3\g_needpass\0
14:00 ClientConnect: 2
15:00 ClientUserinfoChanged: 2 n\Isgalamido\t\0\model\xian/default\hmodel\xian/default\g_redteam\\g_blueteam\\c1\4\c2\5\hc\100\w\0\l\0\tt\0\tl\0
16:53 ClientUserinfoChanged: 7 n\Assasinu Credi\t\1\model\james\hmodel\*james\g_redteam\\g_blueteam\\c1\4\c2\5\hc\100\w\0\l\0\tt\0\tl\0
20:37 ClientBegin: 2
20:37 ShutdownGame:
20:37 ------------------------------------------------------------
"""
    file_path.write_text(file_content)
    return file_path


def test_parse_players_count(mock_file):
    # Arrange
    log_parser = QuakeLogParser(mock_file)

    # Act
    log_parser.parse()

    # Assert
    assert len(log_parser.games[0].players) == 2
    assert log_parser.games[0].players == ["Isgalamido", "Assasinu Credi"]
