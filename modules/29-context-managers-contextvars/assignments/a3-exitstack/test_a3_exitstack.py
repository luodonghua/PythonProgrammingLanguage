import pytest

from practice import load

m = load(__file__)


def make_files(tmp_path, count):
    paths = []
    for i in range(count):
        p = tmp_path / f"f{i}.txt"
        p.write_text(f"file {i}\n", encoding="utf-8")
        paths.append(p)
    return paths


def test_open_all_yields_open_files_in_order(tmp_path):
    paths = make_files(tmp_path, 3)
    with m.open_all(paths) as files:
        assert [f.read().strip() for f in files] == ["file 0", "file 1", "file 2"]
        assert not any(f.closed for f in files)
    assert all(f.closed for f in files)


def test_open_all_closes_after_error(tmp_path):
    paths = make_files(tmp_path, 2)
    with pytest.raises(RuntimeError):
        with m.open_all(paths) as files:
            raise RuntimeError("boom")
    assert all(f.closed for f in files)


def test_open_all_write_mode(tmp_path):
    paths = [tmp_path / "a.txt", tmp_path / "b.txt"]
    with m.open_all(paths, "w") as files:
        for f in files:
            f.write("hello")
    assert [p.read_text(encoding="utf-8") for p in paths] == ["hello", "hello"]


def test_open_all_missing_file_closes_the_others(tmp_path, monkeypatch):
    paths = make_files(tmp_path, 2) + [tmp_path / "missing.txt"]
    opened = []
    real_open = open

    def spy(*args, **kwargs):
        f = real_open(*args, **kwargs)
        opened.append(f)
        return f

    monkeypatch.setattr("builtins.open", spy)
    with pytest.raises(FileNotFoundError):
        with m.open_all(paths):
            pytest.fail("block must not run")
    assert len(opened) == 2
    assert all(f.closed for f in opened)


def test_open_all_empty_list():
    with m.open_all([]) as files:
        assert files == []


def test_capture_output():
    def noisy(a, b=1):
        print("hello", a)
        print("again")
        return a + b

    assert m.capture_output(noisy, 2, b=3) == (5, "hello 2\nagain\n")


def test_capture_output_does_not_leak(capsys):
    assert m.capture_output(print, "secret") == (None, "secret\n")
    assert capsys.readouterr().out == ""


def test_capture_output_restores_stdout_after_error(capsys):
    def fails():
        print("lost")
        raise ValueError

    with pytest.raises(ValueError):
        m.capture_output(fails)
    print("visible")
    assert capsys.readouterr().out == "visible\n"


class Closer:
    def __init__(self, name, log, fail=False):
        self.name, self.log, self.fail = name, log, fail

    def close(self):
        self.log.append(self.name)
        if self.fail:
            raise OSError(self.name)


def test_close_all_reverse_order():
    log = []
    m.close_all(Closer("a", log), Closer("b", log), Closer("c", log))
    assert log == ["c", "b", "a"]


def test_close_all_continues_after_failure():
    log = []
    with pytest.raises(OSError):
        m.close_all(Closer("a", log), Closer("b", log, fail=True), Closer("c", log))
    assert log == ["c", "b", "a"]
