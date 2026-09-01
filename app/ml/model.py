from sklearn.linear_model import LogisticRegression


class CreditRiskModel:
    """
    Reusable CreditLens credit-risk model.

    The model predicts the probability that an applicant
    will default.
    """

    def __init__(self):
        self.model = LogisticRegression(
            max_iter=1000
        )

    def train(self, X_train, y_train):
        """
        Train the credit-risk model.
        """

        self.model.fit(
            X_train,
            y_train,
        )

    def predict_probability(self, X):
        """
        Return probability of default.
        """

        return self.model.predict_proba(X)[:, 1]

    def predict(self, X, threshold=0.50):
        """
        Convert default probabilities into
        binary default predictions.
        """

        probabilities = self.predict_probability(X)

        return (
            probabilities >= threshold
        ).astype(int)

    def get_coefficients(self, feature_names):
        """
        Return model coefficients mapped
        to their feature names.
        """

        coefficients = self.model.coef_[0]

        return dict(
            sorted(
                zip(feature_names, coefficients),
                key=lambda item: abs(item[1]),
                reverse=True,
            )
        )

    def get_feature_contributions(
        self,
        X,
        feature_names,
    ):
        """
        Return individual feature contributions
        to the logistic regression linear score.

        Contribution = feature value * coefficient.
        """

        coefficients = self.model.coef_[0]

        contributions = X[0] * coefficients

        return dict(
            sorted(
                zip(
                    feature_names,
                    contributions,
                ),
                key=lambda item: abs(item[1]),
                reverse=True,
            )
        )