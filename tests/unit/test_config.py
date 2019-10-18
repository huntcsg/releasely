def test_config():
    import releasely

    config = releasely.config.load_project_config()
    assert "filepaths" in config
    assert "repo" in config
