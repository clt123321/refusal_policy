from scripts.reload_repair_artifact import build_parser


def test_reload_cli_has_no_implicit_development_paths():
    args = build_parser().parse_args([
        "--base", "/model", "--adapter", "/adapter", "--receipt", "/receipt.json",
    ])
    assert str(args.base) == "/model"
    assert str(args.adapter) == "/adapter"
    assert str(args.receipt) == "/receipt.json"
