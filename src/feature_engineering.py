
from sklearn.base import BaseEstimator, TransformerMixin
class LeadFeatureEngineeringTransformer(BaseEstimator, TransformerMixin):
    """
    Applies business-oriented feature engineering rules before
    column-based preprocessing.
    """

    def fit(self, X, y=None):
        """
        No parameters are learned from the data because the current
        transformations are based on predefined business rules.
        """
        return self

    def transform(self, X):
        """
        Apply category cleaning and create engineered features.
        """

        # Create a copy to avoid modifying the original input data
        X = X.copy()

        # ---------------------------------------------------------
        # 1. Lead Source Cleaning
        # ---------------------------------------------------------

        # Normalize inconsistent capitalization
        X["Lead Source"] = X["Lead Source"].replace({
            "google": "Google",
            "bing": "Bing"
        })

        # Group extremely rare Lead Source categories into "Other"
        rare_lead_sources = [
            "Click2call",
            "Social Media",
            "Live Chat",
            "Press_Release",
            "blog",
            "Pay per Click Ads",
            "WeLearn",
            "welearnblog_Home",
            "youtubechannel",
            "testone",
            "NC_EDM",
            "Bing"
        ]

        X["Lead Source"] = X["Lead Source"].replace(
            rare_lead_sources,
            "Other"
        )

        # ---------------------------------------------------------
        # 2. Current Occupation Cleaning
        # ---------------------------------------------------------

        # Consolidate very small occupation categories
        X["What is your current occupation"] = X[
            "What is your current occupation"
        ].replace({
            "Businessman": "Other",
            "Housewife": "Other"
        })

        # ---------------------------------------------------------
        # 3. Lead Profile Cleaning
        # ---------------------------------------------------------

        # Consolidate very small Lead Profile categories
        X["Lead Profile"] = X["Lead Profile"].replace({
            "Lateral Student": "Other",
            "Dual Specialization Student": "Other"
        })

        # ---------------------------------------------------------
        # 4. Website Engagement Missingness
        # ---------------------------------------------------------

        # Create a binary indicator because TotalVisits and
        # Page Views Per Visit were found to be missing together
        X["Website_Engagement_Missing"] = (
            X["TotalVisits"].isna()
            & X["Page Views Per Visit"].isna()
        ).astype(int)

        return X