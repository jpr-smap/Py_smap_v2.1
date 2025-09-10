from smap_python_tools.parity import (
    MatlabSignature,
    build_parity_map,
    parse_matlab_signature,
    summarize_parity_map,
)


def test_parse_matlab_signature_basic():
    src = "% Leading\n% Comment\nfunction out = foo(in)\n"
    sig = parse_matlab_signature(src)
    assert isinstance(sig, MatlabSignature)
    assert sig.name == "foo"
    assert sig.outputs == ["out"]
    assert sig.inputs == ["in"]
    assert sig.comments == ["Leading", "Comment"]


def test_parse_matlab_signature_multiple_outputs():
    src = "function [a, b] = bar(x, y)\n"
    sig = parse_matlab_signature(src)
    assert sig.name == "bar"
    assert sig.outputs == ["a", "b"]
    assert sig.inputs == ["x", "y"]
    assert sig.comments == []


def test_index_and_summarize(tmp_path):
    matlab_root = tmp_path / "matlab"
    python_root = tmp_path / "python"
    matlab_root.mkdir()
    python_root.mkdir()

    (matlab_root / "foo.m").write_text("function y = foo(x)\n")
    (python_root / "foo.py").write_text("def foo(x):\n    return x\n")
    (python_root / "bar.py").write_text("def bar():\n    pass\n")

    csv_path = tmp_path / "map.csv"
    build_parity_map(str(matlab_root), str(python_root), str(csv_path))
    counts = summarize_parity_map(str(csv_path))
    assert counts == {"matched": 1, "matlab_only": 0, "python_only": 1}
