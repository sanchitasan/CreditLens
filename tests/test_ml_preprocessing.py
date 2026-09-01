from app.ml.preprocessing import (
    FEATURES,
    TARGET,
    prepare_data,
)


def test_prepare_data():

    X_train, X_test, y_train, y_test = prepare_data()

    # Verify number of rows.
    assert len(X_train) == 8000
    assert len(X_test) == 2000

    # Verify feature count.
    assert X_train.shape[1] == 8
    assert X_test.shape[1] == 8

    # Verify target sizes.
    assert len(y_train) == 8000
    assert len(y_test) == 2000

    # Verify feature names.
    assert list(X_train.columns) == FEATURES
    assert list(X_test.columns) == FEATURES

    # Verify target name.
    assert y_train.name == TARGET
    assert y_test.name == TARGET

    # Verify target contains only binary classes.
    assert set(y_train.unique()).issubset({0, 1})
    assert set(y_test.unique()).issubset({0, 1})


def test_stratified_split():

    X_train, X_test, y_train, y_test = prepare_data()

    train_default_rate = y_train.mean()
    test_default_rate = y_test.mean()

    # The two distributions should be very close.
    assert abs(train_default_rate - test_default_rate) < 0.01