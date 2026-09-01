from app.ml.model import CreditRiskModel
from app.ml.preprocessing import prepare_data
from app.ml.model_persistence import save_model


def main():

    print("CreditLens Model Training")
    print("=" * 40)

    X_train, X_test, y_train, y_test = (
        
        prepare_data()
    )

    model = CreditRiskModel()

    model.train(
        X_train,
        y_train,
    )

    save_model(model)

    print()
    print("Model training completed.")
    print("Model saved successfully.")


if __name__ == "__main__":
    main()