def verify_title(response, title):
    expected_title = f"<title>{title}</title>"
    assert (
        expected_title in response.data.decode()
    ), f"Page title does not match: expected '{expected_title}' in page"
