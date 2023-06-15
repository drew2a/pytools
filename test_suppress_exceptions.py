from suppress_exceptions import suppress_exceptions


async def test_async_suppress_exceptions():
    """Test suppress exceptions for an async function."""

    @suppress_exceptions
    async def raise_an_exception():
        raise Exception

    assert not await raise_an_exception()  # no exceptions


def test_sync_suppress_exceptions():
    """Test suppress exceptions for a sync function."""

    @suppress_exceptions
    def raise_an_exception():
        raise Exception

    assert not raise_an_exception()  # no exceptions
